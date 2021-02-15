from main import *
import pickle
import csv

n_indiv=230
n_try=20
directory=r"C:\Users\Yassine\Desktop\GaitData"
data_steps=[]
label=[]

  
for k in range(1,n_indiv+1):
        #print(i)
    for j in range(1,n_try+1):
        
        file=directory+"\\"+str(k)+"-"+str(j)+".csv"
        if (str(k)+"-"+str(j)+".csv" in listdir(directory)):
            print(k,"--",j)
            data=data_acquisition(file)
            meta_data=data[1]
            right=meta_data['RightFootActivity']
            left=meta_data['LeftFootActivity']
            signal=pd.DataFrame(preprocessing.scale(data[0]))
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
                vector=np.asarray(chunk.describe().iloc[1:8,]).flatten().tolist()
                if s in right:
                    vector.append(1)
                else:
                    vector.append(0)
                data_steps.append(vector)
                
            for s in left_segments:
                chunk=left_signal.iloc[s[0]:s[1],:]
                vector=np.asarray(chunk.describe().iloc[1:8,]).flatten().tolist()
                if s in left:
                    vector.append(1)
                else:
                    vector.append(0)
                data_steps.append(vector)
        
df=pd.DataFrame(data_steps)
df.to_csv('data_label_scaled_rot.csv', index=False)
                

                


