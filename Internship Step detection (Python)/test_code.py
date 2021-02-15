import os
from main import *
from train import *

def load_test_segments():
    list_of_files=listdir(r"C:\Users\Yassine\Desktop\test_data")
    d=dict()
    for file in list_of_files:
        extension=file[file.find(".")+1:len(file)]
        if (extension=="csv"):
            code=file[0:file.find(".")].split("-")
            i=int(code[0])
            j=int(code[1])
            #print(i,"  ",j)
            link="C:\\Users\\Yassine\\Desktop\\test_data\\"+str(i)+"-"+str(j)+".csv"
            d[(i,j)]=data_acquisition(link)
    return(d) 

def transform_data(transformation,d):
    col=d[0].columns.tolist()
    if (transformation.scale==True):
        d[0]=pd.DataFrame(preprocessing.scale(d[0]),columns=col)
    cols=d[0].columns
    if (transformation.acc==True):
        acc_features=['LAV','LAX','LAY','LAZ','RAV','RAX','RAY','RAZ']
        kept=[value for value in cols if value in acc_features] 
        d[0]=d[0][kept]
    elif (transformation.rot==True):
        
        rot_features=['LRV','LRX','LRY','LRZ','RRV','RRX','RRY','RRZ']
        kept=[value for value in cols if value in rot_features]
        d[0]=d[0][kept]
    
      
    return d


def segmentation(link,method,cost,tr,side,pen=False):
    print("initiating process for: ",link)
    data=data_acquisition(link)
    
    meta_data=data[1]
    subject=int(meta_data['Subject'])
    trial=int(meta_data['Trial'])
    data=get_side_data(data,side)
    if (pen==False):
        tbis=transformation(tr.state,False,tr.rot,tr.acc)
    else:
        tbis=transformation(tr.state,True,tr.rot,tr.acc)
    
    databis=transform_data(tbis,data)
    df=databis[0]

    steps=databis[1]
    signals=np.asarray(df)
    bkps=np.asarray(steps)
    bkps=bkps.reshape(bkps.shape[1]*bkps.shape[0])
    algo = method(model=cost).fit(signals)
    if (pen==False):
        my_bkps = np.asarray(algo.predict(n_bkps=len(bkps)+1))[0:]
    else:
        val=1
        if (cost=="gaussian"):
            val=200
        my_bkps = np.asarray(algo.predict(pen=val))
    #print(my_bkps)
    segs=[]
    detected_steps=[]
    L=[]
    if (pen==False):
        databis=transform_data(tr,data)
    df=databis[0]
    segs.append([0,my_bkps[0]])
    for i in range(len(my_bkps)-1):
        segs.append([my_bkps[i],my_bkps[i+1]])
    #segs.append([my_bkps[len(my_bkps)-1],df.shape[0]])
    if (pen==True):
        segs=adjust_segment(segs)
    for s in segs:
        chunk=df.iloc[s[0]:s[1],:]
        summ=chunk.describe().iloc[1:8,]
        vector=np.asarray(summ).flatten()
        #vector=np.linalg.norm(summ,axis=1)
        vector=np.append(vector,[subject,trial])

        L.append(vector)
    L=np.asarray(L)
    return (L,segs)


'Returns a list of segment descriptor for each file and files by pathology type, and info for each file'
def list_segmentation(method,cost,transformation,side,pen=False):
    pathology_group=dict()   
    info=dict() 
    L=[]
    for f in listdir(r"C:\Users\Yassine\Desktop\Test_data"):
        extension=f[f.find('.')+1:len(f)]
        i=int(f[0:f.find('-')])
        j=int(f[f.find('-')+1:f.find('.')])
        if (extension=="csv"):
            file="C:\\Users\\Yassine\\Desktop\\Test_data\\"+str(f)
            data=data_acquisition(file)
            meta_data=data[1]
            type_illness=meta_data["PathologyGroup"]           
            if (not(type_illness in pathology_group)):
                pathology_group[type_illness]=[]
                pathology_group[type_illness].append((i,j))
            else:
                pathology_group[type_illness].append((i,j))
            result=segmentation(file,method,cost,transformation,side,pen)
            steps=get_side_data(data,side)[1]
            res=result[0]
            segments=result[1]
            info[(i,j)]=(type_illness,segments,steps)
            for k in res:
                L.append(k)
    L=np.asarray(L) 
    return(L,pathology_group,info)       
'Does the clustering for the list of segments, a dict where the key '
'is the file and the value is its segments labels'
def classify_segments(P,clf):
    L=np.asarray(P[0])
    to_del=[i for i in set(np.where(np.isnan(L))[0])]
    L=np.delete(L, to_del,axis=0)
    X=L[:,0:L.shape[1]-2]
    X=pd.DataFrame(X)

    
    Y_pred =clf.predict(X)
    labels=Y_pred
    dict_labels=dict()
    for i in range(len(labels)):
        code=(L[i,L.shape[1]-2],L[i,L.shape[1]-1])
        if (code not in dict_labels):
            dict_labels[code]=[]
            dict_labels[code].append(labels[i])
        else:
            dict_labels[code].append(labels[i]) 
    return(dict_labels)
    
'Computes the scores'
def compute_score(dict_labels,P):
    pathology_group=P[1]
    info=P[2]
    results=dict()
    prec=dict()
    rec=dict()
    score_pathology=dict()
    precision_pathology=dict()
    recall_pathology=dict()
    for i in dict_labels:
        #print(i)
        seg=info[i][1]
        pathology=info[i][0]
        
        steps=info[i][2]
        
        labels=dict_labels[i]
        
        detected_steps=[]
        for j in range(len(labels)):
            if (labels[j]==1):
                detected_steps.append(seg[j])
        #print(detected_steps)
        results[i]=f_score(detected_steps,steps)
        prec[i]=precision(detected_steps,steps)
        rec[i]=recall(detected_steps,steps)
        #print(i,"     ",results[i])
        if (pathology in score_pathology):
            score_pathology[pathology]=score_pathology[pathology]+results[i]
            precision_pathology[pathology]=precision_pathology[pathology]+precision(detected_steps,steps)
            recall_pathology[pathology]=recall_pathology[pathology]+recall(detected_steps,steps)
        else:
            score_pathology[pathology]=results[i]
            precision_pathology[pathology]=precision(detected_steps,steps)
            recall_pathology[pathology]=recall(detected_steps,steps)
    for i in score_pathology:
        score_pathology[i]=score_pathology[i]/len(pathology_group[i])
        precision_pathology[i]=precision_pathology[i]/len(pathology_group[i])
        recall_pathology[i]=recall_pathology[i]/len(pathology_group[i])
    mean_score=np.asarray([*results.values()]).mean()
    mean_precision=np.asarray([*prec.values()]).mean()
    mean_recall=np.asarray([*rec.values()]).mean()
    return(results,prec,rec,score_pathology,precision_pathology,recall_pathology,mean_score,mean_precision,mean_recall)

def pipeline(method,cost,tr,side,pen):
    df=load_segments(tr)  
    s=train_test_segments(df) 
    res=train_model_rf(s)
    print(eval_model_rf(res,s))
    pack=list_segmentation(method,cost,tr,side,pen)
    lab=classify_segments(pack,res)
    results=compute_score(lab,pack)
    return(results)

# =============================================================================
# =============================================================================
method=rpt.BottomUp
cost='lin ker'
tr=transformation(True,True,False,True)
side='right'
pen=False
# df=load_segments(tr)  
# s=train_test_segments(df) 
# res=train_model_rf(s)
# #     
# pack=list_segmentation(method,cost,tr,side)
# # 
# lab=classify_segments(pack,res)
# results=compute_score(lab,pack)    
# =============================================================================
# =============================================================================

res=pipeline(method,cost,tr,side,pen)