import os
import glob
from main import *
import random
import shutil
from sklearn.model_selection import train_test_split

class transformation:
    def __init__(self,state=False,scale=False,rot=False,acc=False):
        self.state=state
        self.scale=False
        self.rot=False
        self.acc=False
        if (state==True):
            
            self.scale=scale
            self.rot=rot
            self.acc=acc

class data_split:
    def __init__(self):
        self.train=[]
        self.test=[]
    

def codes_list(directory):
    files=[]
    for i in range(1,231):
        for j in range(1,25):
            file=directory+"\\"+str(i)+"-"+str(j)+".csv"
            if (str(i)+"-"+str(j)+".csv" in listdir(directory)):
                files.append((i,j))
            else:
                break
    return(files)
                
def train_test(directory,proportion_train):
    data=data_split()
    files=codes_list(directory)
    n=len(files)
    indexes=[i for i in range(n)]
    indexes_train, indexes_test,= train_test_split(indexes, train_size=proportion_train)
    data.train=[files[i] for i in indexes_train]
    data.test=[files[i] for i in indexes_test]
    return(data)

def data_per_type(directory,n_files):

    n_indiv=230
    n_try=20
    files_pathology=dict()
    directory=directory
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
    files_per_type=n_files
    files_selected=[]
    for i in files_pathology:
        files=files_pathology[i]
        picked=[]
        k=0
        for j in range(files_per_type):
            while(k in picked):
                k=random.randint(0,len(files)-1)
            picked.append(k)
            files_selected.append(files[k])
    return(files_selected)
    
def train_test_div(n_files_type,directory):
    direct = "C:/Users/Yassine/Desktop/Train_data/*"
    r = glob.glob(direct)
    for i in r:
        os.remove(i)
    direct = "C:/Users/Yassine/Desktop/Test_data/*"
    r = glob.glob(direct)
    for i in r:
        os.remove(i)
    files=data_per_type(directory,n_files_type)
    all_files=listdir(directory)
    n=len(all_files)
    print(n)
    train=[]
    test=[]
    for i in files:
        train.append(i+"csv")
        train.append(i+"json")
    print(len(train))
    for k in all_files:
        code=k[0:k.find(".")].split("-")
        i=int(code[0])
        j=int(code[1])
        csv=directory+"\\"+str(i)+"-"+str(j)+".csv"
        json=directory+"\\"+str(i)+"-"+str(j)+".json"
        if csv not in train:
            test.append(csv)
            test.append(json)
    print(len(test))
    
    for f in train:
        shutil.copy(f, r'C:\Users\Yassine\Desktop\train_data')
    for f in test:
        shutil.copy(f, r'C:\Users\Yassine\Desktop\test_data')
    
    
        
    

    