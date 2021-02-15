from main import *
from test_code import *
from train import *
from os import listdir
import os
import shutil
import glob

import random


def get_data_type():
    n_indiv=230
    n_try=20
    files_pathology=dict()
    directory="C:\\Users\\Yassine\\Desktop\\GaitData"
    for i in range(1,n_indiv+1):
        for j in range(1,n_try+1):
            
            
            file=directory+"\\"+str(i)+"-"+str(j)+"."
            if (str(i)+"-"+str(j)+".csv" in listdir(directory)):
                print(i,"--",j)
                data=data_acquisition(file+"csv")
                meta_data=data[1]
                type_illness=meta_data["PathologyGroup"]
                if type_illness in files_pathology:
                    files_pathology[type_illness].append(file)
                else:
                    files_pathology[type_illness]=[]
                    files_pathology[type_illness].append(file)
            else:
                break
    return(files_pathology)
def split(L,n):
    splits=[]
    p=len(L)//n
    if (len(L)%n!=0):
        p=p+1
    start=0
    while (len(splits)<n):
        splits.append(L[start:min(len(L),start+p)])
        start=start+p
    return splits

def cross_validation(n_split,method,cost,tr,side,pen):
    data_per_type=get_data_type()
    splits=dict()
    results_list=[]
    for i in data_per_type:
        random.shuffle(data_per_type[i])
        splits[i]=split(data_per_type[i],n_split)
    
    directory="C:\\Users\\Yassine\\Desktop\\GaitData"
    all_files=listdir("C:\\Users\\Yassine\\Desktop\\GaitData")
    for i in range(n_split):
        train=[]
        direct = "C:/Users/Yassine/Desktop/Train_data/*"
        r = glob.glob(direct)
        for ip in r:
            os.remove(ip)
        direct = "C:/Users/Yassine/Desktop/Test_data/*"
        r = glob.glob(direct)
        for ip in r:
            os.remove(ip)
        print("split number ",i+1)
        print("splitting train and test data ...")
        for j in splits:
            train=train+splits[j][i]
        for f in all_files:
            code=f[0:f.find(".")].split("-")
            i=int(code[0])
            j=int(code[1])
            csv=directory+"\\"+str(i)+"-"+str(j)+".csv"
            json=directory+"\\"+str(i)+"-"+str(j)+".json"
            X=directory+"\\"+str(i)+"-"+str(j)+"."
            if X in train:
                shutil.copy(csv, r'C:\Users\Yassine\Desktop\Train_data')
                shutil.copy(json, r'C:\Users\Yassine\Desktop\Train_data')
                
            else:
                shutil.copy(csv, r'C:\Users\Yassine\Desktop\Test_data')
                shutil.copy(json, r'C:\Users\Yassine\Desktop\Test_data')
        print(len(listdir(r'C:\Users\Yassine\Desktop\Test_data')))
        print(len(listdir(r'C:\Users\Yassine\Desktop\Train_data')))
        results_list.append(pipeline(method,cost,tr,side,pen))        
    return results_list        
    
    
    
    
method=rpt.BottomUp
cost='lin ker'
tr=transformation(True,True,False,True)
side='right'   
pen=True 
n_splits=1
#res=pipeline(method,cost,tr,side)
res=cross_validation(n_splits,method,cost,tr,side,pen)
    
    
    
    
    



    