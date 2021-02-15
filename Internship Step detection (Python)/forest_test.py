from main import *
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

# =============================================================================
# 
df=pd.read_csv("data_label.csv").iloc[0:40000,:]
to_del=[i for i in set(np.where(np.isnan(df))[0])]
df=df.drop(to_del)
X=df.iloc[:,0:df.shape[1]-1]
Y=df.iloc[:,df.shape[1]-1]
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.7)
print("fitting model ...")
clf=RandomForestClassifier(n_estimators=100)
clf.fit(X_train,Y_train)




link=r"C:\Users\Yassine\Desktop\GaitData\1-1.csv"
side="right"
print("initiating process for: ",link)
data=get_side_data(data_acquisition(link),side)
meta_data=data[1]
df=data[0]
data=df



signals=np.asarray(data)
steps=meta_data
bkps=np.asarray(steps)
bkps=bkps.reshape(bkps.shape[1]*bkps.shape[0])
algo = rpt.BottomUp(custom_cost=MyCost()).fit(signals)
my_bkps = np.asarray(algo.predict(n_bkps=len(bkps)+1))[0:]
segs=[]
detected_steps=[]
for i in range(len(my_bkps)-1):
    segs.append((my_bkps[i],my_bkps[i+1]))
L=[]
for s in segs:
    chunk=data.iloc[s[0]:s[1],:]
    scaled=chunk
    #scaled=pd.DataFrame(preprocessing.scale(chunk,axis=0))
    summ=scaled.describe().iloc[1:8,]
    vector=np.asarray(summ).flatten()
    #vector=np.linalg.norm(summ,axis=1)
    L.append(vector)
L=np.asarray(L)
L=pd.DataFrame(L)
labels=clf.predict(L)
for i in range(len(segs)):
    if(labels[i]==1):
        detected_steps.append(segs[i])
print(f_score(detected_steps,steps))
    


