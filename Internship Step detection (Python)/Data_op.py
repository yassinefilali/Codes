import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt


def corr_selection(df,seuil):
    corr=df.corr()
    test=corr>seuil
    groups=dict()
    grouped=dict()
    group=0
    for i in test.columns:
        if (i not in grouped):
            grouped[i]=group
            groups[group]=[i]
            group=group+1
        
        for j in test.columns:
            
            if (i!=j)and(test[i][j]==True)and(j not in grouped):
                grouped[j]=grouped[i]
                groups[grouped[i]].append(j)
            
# =============================================================================
            elif (i!=j)and(test[i][j]==True)and(j in grouped)and(len(groups[grouped[i]])==1):
                del groups[grouped[i]]
                grouped[i]=grouped[j]
                
                groups[grouped[j]].append(i)
    select=[]
    for i in groups:
        select.append(groups[i][0])

    return df[select]
    

def data_acquisition(f):
    data=pd.read_csv(f)
    json_link=f[0:-3]+"json"
    f=open(json_link)
    meta_data=json.load(f)
    return[data,meta_data]
    

def get_side_data(res,side):
    if (side=="left"):
        return[res[0].iloc[:,0:8],res[1]['LeftFootActivity']]
    elif(side=="right"):
        return[res[0].iloc[:,8:16],res[1]['RightFootActivity']]
    else:
        return(res)


def plot_signal_steps(df,res,cost=False):
    plt.cla()
    plt.clf()
    steps=res[2]
    if (cost==True):
        fig, axs = plt.subplots(2,1)
        axs[0].plot(df)
        axs[1].plot(res[1],res[0])
        for i in steps:
            axs[0].axvline(x=i[0],color='red',ls='--')
            axs[0].axvline(x=i[1],color='green',ls='--')
        
    else:    
        plt.plot(df)
        for i in steps:
            plt.axvline(x=i[0],color='red',ls='--')
            plt.axvline(x=i[1],color='green',ls='--')
        
