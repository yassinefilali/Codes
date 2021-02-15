from main import *


def process(link,method,cost,side):
    print("initiating process for: ",link)
    data=data_acquisition(link)
    meta_data=data[1]
    subject=int(meta_data['Subject'])
    trial=int(meta_data['Trial'])
    data=get_side_data(data,side)
    df=data[0].iloc[:,:]
    
    steps=data[1]
    data=df
    data=pd.DataFrame(preprocessing.scale(df))
# =============================================================================
#     test=PCA()
#     res=test.fit(data)
#     var=np.cumsum(res.explained_variance_ratio_)<0.95
#     i=[*var].index(False)
#     PCA1=PCA(i)
#     res=PCA1.fit(data)
#     data=pd.DataFrame(res.transform(data))
#     print(data)
#     print(i)
# =============================================================================
    signals=np.asarray(data)
    bkps=np.asarray(steps)
    bkps=bkps.reshape(bkps.shape[1]*bkps.shape[0])
    algo = method(model='gaussian').fit(signals)
    my_bkps = np.asarray(algo.predict(n_bkps=len(bkps)+1))[0:]
    rpt.show.display(signals,[], my_bkps, figsize=(10, 6))
    plt.show()
    segs=[]
    detected_steps=[]
    L=[]
    #data=pd.DataFrame(preprocessing.scale(data))
    for i in range(len(my_bkps)-1):
        segs.append((my_bkps[i],my_bkps[i+1]))
    for s in segs:
        chunk=data.iloc[s[0]:s[1],:]
        scaled=chunk
        #scaled=pd.DataFrame(preprocessing.scale(chunk))
        summ=scaled.describe().iloc[1:8,]
        #vector=np.asarray(summ).flatten()
        vector=np.linalg.norm(summ,axis=1)
        vector=np.append(vector,[subject,trial])
        L.append(vector)
    L=np.asarray(L)
    return (L,segs)

def chain(directory,method,cost,side,n_indiv,n_try):
  ### Dict that associates each type of pathology to it's files   
    pathology_group=dict()
   ### Dict that associates each file it's info     
    info=dict()
 
    L=[]
  ### List of each vector describing a segment + the file code ####  
    for i in range(1,n_indiv+1):
        for j in range(1,n_try+1):

        

            file=directory+"\\"+str(i)+"-"+str(j)+".csv"
            if (str(i)+"-"+str(j)+".csv" in listdir(directory)):
                data=data_acquisition(file)
                meta_data=data[1]
                type_illness=meta_data["PathologyGroup"]
                print(type_illness)
   ##### Assign each file to illness type to keep count ######             
                if (not(type_illness in pathology_group)):
                    pathology_group[type_illness]=[]
                    pathology_group[type_illness].append((i,j))
                else:
                    pathology_group[type_illness].append((i,j))
                    
                
   ##### Construction of a dict to keep track of information in the file ######
                result=process(file,method,cost,side)
                steps=get_side_data(data,side)[1]
                res=result[0]
                segments=result[1]
                info[(i,j)]=(type_illness,segments,steps)
                for k in res:
                    L.append(k)
              
            
        
            else:
                break
    L=np.asarray(L)
    X=L[:,0:L.shape[1]-2]
    kmeans =KMeans(n_clusters=2, random_state=0).fit(X)
    labels=kmeans.labels_
    dict_labels=dict()
#### Storing segments labels for each file ########
    for i in range(len(labels)):
        code=(L[i,L.shape[1]-2],L[i,L.shape[1]-1])
        if (code not in dict_labels):
            dict_labels[code]=[]
            dict_labels[code].append(labels[i])
        else:
            dict_labels[code].append(labels[i])
##### Construction of a dict containing detected_steps + f_score for each file
    results=dict()
    prec=dict()
    rec=dict()
    score_pathology=dict()
    precision_pathology=dict()
    recall_pathology=dict()
    for i in dict_labels:
        seg=info[i][1]
        pathology=info[i][0]
        
        steps=info[i][2]
        
        labels=dict_labels[i]
        
        detected_steps=[]
        dup=[]
        for j in range(len(labels)):
            if (labels[j]!=labels[0]):
                detected_steps.append(seg[j])
            else:
                dup.append(seg[j])
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

        if (f1>f2):
            results[i]=f1
            prec[i]=p1
            rec[i]=r1
        else:
            results[i]=f2
            prec[i]=p2
            rec[i]=r2
        if (pathology in score_pathology):
            score_pathology[pathology]=score_pathology[pathology]+results[i]
            precision_pathology[pathology]=precision_pathology[pathology]+prec[i]
            recall_pathology[pathology]=recall_pathology[pathology]+rec[i]
        else:
            score_pathology[pathology]=results[i]
            precision_pathology[pathology]=prec[i]
            recall_pathology[pathology]=rec[i]
    for i in score_pathology:
        score_pathology[i]=score_pathology[i]/len(pathology_group[i])
        precision_pathology[i]=precision_pathology[i]/len(pathology_group[i])
        recall_pathology[i]=recall_pathology[i]/len(pathology_group[i])
    
    
    
    return(results,prec,rec,score_pathology,precision_pathology,recall_pathology)

link=r"C:\Users\Yassine\Desktop\GaitData\230-5.csv"
side="right"
res=chain(r"C:\Users\Yassine\Desktop\GaitData",rpt.BottomUp,MyCost(),side,1,1)