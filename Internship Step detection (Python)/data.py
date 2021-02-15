import pandas as pd
import json
import matplotlib.pyplot as plt

def data_acquisition(f):
    data=pd.read_csv(f)
    json_link=f[0:-3]+"json"
    f=open(json_link)
    meta_data=json.load(f)
    return(data,meta_data)
    

def get_side_data(res,side):
    if (side=="left"):
        return(res[0].iloc[:,0:8],res[1]['LeftFootActivity'])
    elif(side=="right"):
        return(res[0].iloc[:,8:16],res[1]['RightFootActivity'])
    else:
        return(res)


def plot_signal_steps(df,steps,cost=False):
    plt.cla()
    plt.clf()
    plt.plot(df)
    for i in steps:
        plt.axvline(x=i[0],color='red',ls='--')
        plt.axvline(x=i[1],color='green',ls='--')
        
link=r"C:\Users\Yassine\Desktop\GaitData\1-1.csv"
label=get_side_data(data_acquisition(link),"right")
data=label[0]
steps=label[1]

plot_signal_steps(data,steps)