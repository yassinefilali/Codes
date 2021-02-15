


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
    signals=np.asarray(data)
    bkps=np.asarray(steps)
    bkps=bkps.reshape(bkps.shape[1]*bkps.shape[0])
    algo = method(custom_cost=cost).fit(signals)
    my_bkps = np.asarray(algo.predict(n_bkps=len(bkps)+1))[0:]
    segs=[]
    detected_steps=[]
    L=[]
    for i in range(len(my_bkps)-1):
        segs.append((my_bkps[i],my_bkps[i+1]))
    for s in segs:
        chunk=data.iloc[s[0]:s[1],:]
        #scaled=chunk
        scaled=pd.DataFrame(preprocessing.scale(chunk))
        summ=scaled.describe().iloc[1:8,]
        vector=np.asarray(summ).flatten()
        #vector=np.linalg.norm(summ,axis=1)
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
    kmeans =KMeans(n_clusters=2, random_state=0).fit(L[:,0:L.shape[1]-2])
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
    for i in dict_labels:
        print(i)
        seg=info[i][1]
        
        steps=info[i][2]
        
        labels=dict_labels[i]
        
        detected_steps=[]
        dup=[]
        for j in range(len(labels)):
            if (labels[j]!=labels[0]):
                detected_steps.append(seg[j])
            else:
                dup.append(seg[j])
        print(detected_step,"\n",dup)
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
            results[i]=(f1)
        else:
            results[i]=(f2)
        print(results[i])
        
        
    return(results)

link=r"C:\Users\Yassine\Desktop\GaitData\230-5.csv"
side="right"
res=chain(r"C:\Users\Yassine\Desktop\GaitData",rpt.BottomUp,MyCost(),side,230,10)

