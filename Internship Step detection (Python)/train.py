from division import *
from Data_op import *


def load_train():
    list_of_files=listdir(r"C:\Users\Yassine\Desktop\Train_data")
    d=dict()
    for file in list_of_files:
        extension=file[file.find(".")+1:len(file)]
        if (extension=="csv")and(file.find("-")!=-1):
            code=file[0:file.find(".")].split("-")
            i=int(code[0])
            j=int(code[1])
            link="C:\\Users\\Yassine\\Desktop\\train_data\\"+str(i)+"-"+str(j)+".csv"
            d[(i,j)]=data_acquisition(link)
    return(d)   

def extract_segments(transformation,file_name=None):
    print("Extracting segments from train data ...")
    d=load_train()
    data_steps=[]
    count=0
    n=len(d)
    for i in d:
        count=count+1
        print(count,"---",n)
        data=d[i]
        meta_data=data[1]
        right=meta_data['RightFootActivity']
        left=meta_data['LeftFootActivity']
        if (transformation.scale==True):
            signal=pd.DataFrame(preprocessing.scale(data[0]))
        else:
            signal=pd.DataFrame(data[0])
        if (transformation.rot==False)and(transformation.acc==False):
            left_signal=signal.iloc[:,0:8]
            right_signal=signal.iloc[:,8:16]
        elif (transformation.acc==True):
            left_signal=signal.iloc[:,0:8].iloc[:,0:4]
            right_signal=signal.iloc[:,8:16].iloc[:,0:4]
        else:
            left_signal=signal.iloc[:,0:8].iloc[:,4:8]
            right_signal=signal.iloc[:,8:16].iloc[:,4:8]
        right_cp=np.asarray(right).reshape(len(right)*2)
        left_cp=np.asarray(left).reshape(len(left)*2)
        right_segments=[]
        left_segments=[]
        e=signal.shape[0]
        right_segments.append([0,right_cp[0]])
        left_segments.append([0,left_cp[0]])
        for i in range(len(right_cp)-1):
            right_segments.append([right_cp[i],right_cp[i+1]])
        right_segments.append([right_cp[len(right_cp)-1],e])
        for i in range(len(left_cp)-1):
            left_segments.append([left_cp[i],left_cp[i+1]])
        left_segments.append([left_cp[len(left_cp)-1],e])
        for s in right_segments:
            chunk=right_signal.iloc[s[0]:s[1],:]
            summ=chunk.describe().iloc[1:8,]
            vector=np.asarray(summ).flatten().tolist()
            #vector=np.linalg.norm(summ,axis=1).tolist()
            if s in right:
                vector.append(1)
            else:
                vector.append(0)
            data_steps.append(vector)
            
        for s in left_segments:
            chunk=left_signal.iloc[s[0]:s[1],:]
            summ=chunk.describe().iloc[1:8,]
            vector=np.asarray(summ).flatten().tolist()
            #vector=np.linalg.norm(summ,axis=1).tolist()
            if s in left:
                vector.append(1)
            else:
                vector.append(0)
            data_steps.append(vector)
    df=pd.DataFrame(data_steps)
    if (file_name!=None):
        df.to_csv("C:\\Users\\Yassine\\Desktop\\train_data\\"+file_name+'.csv', index=False)
    return(df)

class segments_split:
    def __init__(self,X_train, X_test, Y_train, Y_test):
        self.train_val=X_train
        self.test_val=X_test
        self.train_lab=Y_train
        self.test_lab=Y_test
        

        
def train_test_segments(df,train_prop=0.5):
    X=df.iloc[:,0:df.shape[1]-1]
    Y=df.iloc[:,df.shape[1]-1]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, train_size=train_prop)
    print
    s=segments_split(X_train, X_test, Y_train, Y_test)
    return s

def load_segments(transformation):
    file_name=str(int(transformation.state))+str(int(transformation.scale))+str(int(transformation.rot))+str(int(transformation.acc))
    if (file_name+".csv" in listdir("C:\\Users\\Yassine\\Desktop\\train_data")):
        df=pd.read_csv("C:\\Users\\Yassine\\Desktop\\train_data\\"+file_name+".csv")
    else:
        df=extract_segments(transformation,file_name)
    to_del=[i for i in set(np.where(np.isnan(df))[0])]
    df=df.drop(to_del)
    return(df)

def train_model_rf(s):
    clf=RandomForestClassifier(n_estimators=100)
    clf.fit(s.train_val,s.train_lab)
    return clf
    
def eval_model_rf(clf,s):
    Y_test=clf.predict(s.test_val)
    print(1-abs(sum(Y_test-s.test_lab))/len(Y_test))
    
    


#t=transformation(True,True,False,True)   
#df=load_segments(t)  
#s=train_test_segments(df) 
#res=train_model_rf(s)
    
    
    

            
        
    
    

