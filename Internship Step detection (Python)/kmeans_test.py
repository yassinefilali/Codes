# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 14:52:57 2020

@author: Yassine
"""
from main import *
from sklearn.cluster import KMeans
from sklearn.cluster import SpectralClustering


link=r"C:\Users\Yassine\Desktop\GaitData\214-1.csv"
side="right"
data=get_side_data(data_acquisition(link),side)
meta_data=data[1]
df=data[0]
data=df
# =============================================================================
# =============================================================================
#data=pd.DataFrame(preprocessing.scale(df))
# test=PCA()
# res=test.fit(data)
# var=np.cumsum(res.explained_variance_ratio_)<0.95
# i=[*var].index(False)
# PCA=PCA(8)
# res=PCA.fit(data)
# comp=res.components_
# var=np.cumsum(res.explained_variance_ratio_)
# inert=res.singular_values_
# data=res.transform(data)
# 
# =============================================================================

signals=np.asarray(data)
steps=meta_data
bkps=np.asarray(steps)
bkps=bkps.reshape(bkps.shape[1]*bkps.shape[0])
algo = rpt.BottomUp(custom_cost=MyCost()).fit(signals)
my_bkps = np.asarray(algo.predict(n_bkps=len(bkps)+1))[0:]
rpt.show.display(signals, bkps, my_bkps, figsize=(10, 6))
plt.show()
segs=[]
detected_steps=[]
for i in range(len(my_bkps)-1):
    segs.append((my_bkps[i],my_bkps[i+1]))
L=[]
for s in segs:
    chunk=df.iloc[s[0]:s[1],:]
    scaled=chunk
    scaled=pd.DataFrame(preprocessing.scale(chunk))
    summ=scaled.describe().iloc[1:8,]
    
    vector=np.linalg.norm(summ,axis=1)
    vector=np.asarray(summ).flatten()
    L.append(vector)

L=np.asarray(L)
#kmeans = SpectralClustering(n_clusters=2, random_state=0).fit(L)
#kmeans =KMeans(n_clusters=2, random_state=0).fit(L)
kmeans =AgglomerativeClustering(n_clusters=2).fit(L)

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
    print (f1,detected_steps)
else:
    print (f2,dup)
    
    
