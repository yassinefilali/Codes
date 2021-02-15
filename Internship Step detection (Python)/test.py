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
            print(i,"  ",j)
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


def segmentation(link,method,cost,tr,side):
    print("initiating process for: ",link)
    data=data_acquisition(link)
    
    subject=int(link[link.rindex('\\')+1:link.rindex('-')])
    trial=int(link[link.rindex('-')+1:link.rindex('.')])
    data=get_side_data(data,side)
    tbis=transformation(tr.state,False,tr.rot,tr.acc)
    databis=transform_data(tbis,data)
    
    df=databis[0]

    steps=databis[1]
    signals=np.asarray(df)
    bkps=np.asarray(steps)
    bkps=bkps.reshape(bkps.shape[1]*bkps.shape[0])
    algo = method(model=cost).fit(signals)
    #my_bkps = np.asarray(algo.predict(n_bkps=len(bkps)+10))[0:]
    my_bkps = np.asarray(algo.predict(pen=1))
    segs=[]
    detected_steps=[]
    L=[]
    databis=transform_data(tr,data)
    df=databis[0]
    segs.append([0,my_bkps[0]])
    for i in range(len(my_bkps)-1):
        segs.append([my_bkps[i],my_bkps[i+1]])
    #segs.append([my_bkps[len(my_bkps)-1],df.shape[0]])
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
def list_segmentation(method,cost,transformation,side):
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
            result=segmentation(file,method,cost,transformation,side)
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
    score_pathology=dict()
    for i in dict_labels:
        print(i)
        seg=info[i][1]
        pathology=info[i][0]
        
        steps=info[i][2]
        
        labels=dict_labels[i]
        
        detected_steps=[]
        for j in range(len(labels)):
            if (labels[j]==1):
                detected_steps.append(seg[j])
        print(detected_steps)
        print(steps)
        results[i]=f_score(detected_steps,steps)
        #print(i,"     ",results[i])
        if (pathology in score_pathology):
            score_pathology[pathology]=score_pathology[pathology]+results[i]
        else:
            score_pathology[pathology]=results[i]
    for i in score_pathology:
        score_pathology[i]=score_pathology[i]/len(pathology_group[i])
    mean=np.asarray([*results.values()]).mean()
    return(results,score_pathology,mean)

def pipeline(method,cost,tr,side):
    df=load_segments(tr)  
    s=train_test_segments(df) 
    res=train_model_rf(s)
    
    pack=list_segmentation(method,cost,tr,side)
    lab=classify_segments(pack,res)
    results=compute_score(lab,pack)
    return(results)

# =============================================================================
# =============================================================================
method=rpt.BottomUp
cost='rbf'
tr=transformation(True,True,False,True)
side='left'
df=load_segments(tr)  
s=train_test_segments(df) 
res=train_model_rf(s)
# #     
pack=list_segmentation(method,cost,tr,side)
# # 
lab=classify_segments(pack,res)
results=compute_score(lab,pack)    
# =============================================================================
# =============================================================================

#res=pipeline(method,cost,tr,side)