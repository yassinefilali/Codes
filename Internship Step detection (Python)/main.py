from Detection_method import *
from metrics import *
from Data_op import *
from os import listdir
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering

def process_data(link,method,cost,side,corr_sel=False,seuil=1,PCA_t=False):
    print("initiating process for: ",link)
    data=get_side_data(data_acquisition(link),side)
    meta_data=data[1]
    df=data[0]
    data=df
    if (corr_sel==True):
        df=corr_selection(df,seuil)
    if (PCA_t==True):
        data=pd.DataFrame(preprocessing.scale(df))
        test=PCA()
        res=test.fit(data)
        var=np.cumsum(res.explained_variance_ratio_)<0.95
        i=[*var].index(False)
        PCA1=PCA(i)
        res=PCA1.fit(data)
        #comp=res.components_
        #var=np.cumsum(res.explained_variance_ratio_)
        #inert=res.singular_values_
        data=pd.DataFrame(res.transform(data))
    

    signals=np.asarray(data)
    steps=meta_data
    bkps=np.asarray(steps)
    bkps=bkps.reshape(bkps.shape[1]*bkps.shape[0])
    algo = method(custom_cost=cost).fit(signals)
    my_bkps = np.asarray(algo.predict(n_bkps=len(bkps)+1))[0:]
    segs=[]
    detected_steps=[]
    data=pd.DataFrame(preprocessing.scale(data))
    for i in range(len(my_bkps)-1):
        segs.append((my_bkps[i],my_bkps[i+1]))
    L=[]
    for s in segs:
        chunk=data.iloc[s[0]:s[1],:]
        scaled=chunk
        #scaled=pd.DataFrame(preprocessing.scale(chunk,axis=0))
        summ=scaled.describe().iloc[1:8,]
        #vector=np.asarray(summ).flatten()
        vector=np.linalg.norm(summ,axis=1)
        L.append(vector)
    L=np.asarray(L)
    L=pd.DataFrame(L)
    
# =============================================================================
# =============================================================================
#      L=preprocessing.scale(L)
#      test=PCA()
#      res=test.fit(L)
#      var=np.cumsum(res.explained_variance_ratio_)<0.95
#      i=[*var].index(False)
#      PCA1=PCA(i)
#      res=PCA1.fit(L)
#          #comp=res.components_
#          #var=np.cumsum(res.explained_variance_ratio_)
#          #inert=res.singular_values_
# =============================================================================
#    L=res.transform(L)
    print(L.shape)
     
     #AgglomerativeClustering(n_clusters=2).fit(L)
    kmeans = KMeans(n_clusters=2, random_state=0).fit(L)
    label_init=kmeans.labels_[0]
    dup=[]
    for i in range(len(segs)):
        if (kmeans.labels_[i]!=label_init):
            detected_steps.append(segs[i])
        else:
            dup.append(segs[i])
    p1=precision(detected_steps,steps)
    p2=precision(dup,steps)
    r1=recall(detected_steps,steps)
    r2=recall(dup,steps)
    f1=0
    f2=0
    if (p1+r1!=0):
        f1=f_score(detected_steps,steps)
    if (p2+r2!=0):
        f2=f_score(dup,steps)
    #print(f_score(dup,steps),"  ",f_score(detected_steps,steps))
    if (f1>f2):
        return (f1,detected_steps,precision(detected_steps,steps),recall(detected_steps,steps))
    else:
        return (f2,dup,precision(dup,steps),recall(dup,steps))

        
# =============================================================================
#     limit=np.linalg.norm(data[0].cov())
#     for s in segs:
#         chunk=data[0].iloc[s[0]:s[1],:]
#         x=pd.DataFrame(preprocessing.scale(chunk,with_std=False))
#         if(np.linalg.norm(x.cov())>limit):
#             detected_steps.append(s)
# =============================================================================   
        
    
    

# =============================================================================
# def process(link,width,cost):
#     print("initiating process for: ",link)
#     data=data_acquisition(link)
#     side="right"
#     data=get_side_data(data,side)
#     df=data[0]
#     true_steps=data[1]
#     res=solve_segmentation_window(df,width,cost)
#     detected_steps=res[2]
#     return(f_score(detected_steps,true_steps),res)
# =============================================================================

def score_illness(directory,method,cost,side,n_indiv,n_try):
    count_pathology=dict()
    score_pathology=dict()
    precision_pathology=dict()
    recall_pathology=dict()
    rec=dict()
    pre=dict()
    scores=dict()
    for i in range(1,n_indiv+1):
        for j in range(1,n_try+1):
        

            file=directory+"\\"+str(i)+"-"+str(j)+".csv"
            if (str(i)+"-"+str(j)+".csv" in listdir(directory)):
                data=data_acquisition(file)
                meta_data=data[1]
                type_illness=meta_data["PathologyGroup"]
                print(type_illness)
                if (not(type_illness in score_pathology)):
                    score_pathology[type_illness]=0
                    recall_pathology[type_illness]=0
                    precision_pathology[type_illness]=0
                    count_pathology[type_illness]=0
                
                count_pathology[type_illness]+=1
                res=process_data(file,method,cost,side)
                score_pathology[type_illness]+=res[0]
                scores[file]=res[0]
                
                rec[file]=res[3]
                pre[file]=res[2]
                precision_pathology[type_illness]+=res[2]
                recall_pathology[type_illness]+=res[3]
                print(res[0])
            else:
                break
    for i in score_pathology:
        score_pathology[i]=score_pathology[i]/count_pathology[i]
        precision_pathology[i]=precision_pathology[i]/count_pathology[i]
        recall_pathology[i]=recall_pathology[i]/count_pathology[i]
    return(score_pathology,precision_pathology,recall_pathology,scores,pre,rec)

def chain_process(directory,width,n,cost):
    files=listdir(directory)
    count=0
    scores=[]
    for i in files:
        if (count<n):
            
            if (i[-3:]=='csv'):
                clear()
                print("file number ",count)
                clear()
                scores[i]=process(directory+'\\'+i,width,cost)
                count=count+1
        else:
            break
    return(scores,scores.mean())
#results=score_illness("C:\\Users\\Yassine\\Desktop\\GaitData",rpt.BottomUp,MyCost(),'right',230,20)

    




    