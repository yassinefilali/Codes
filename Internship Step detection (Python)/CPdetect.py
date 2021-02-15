import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import multivariate_normal
from scipy.signal import argrelmax
import random

df=pd.read_csv(r"C:\Users\Yassine\Desktop\GaitData\1-1.csv")
# =============================================================================
#df=df.iloc[0:1000,:]
# =============================================================================
x=df.describe()
fig,ax=plt.subplots(4,4)
fig.suptitle('Signals')
names=df.columns
count=0
for i in range(4):
    for j in range(4):
        data=df.iloc[:,count]
        ax[i,j].plot(data)
        ax[i,j].set_title(names[count])
        count=count+1

# =============================================================================
# 
# import ruptures as rpt
# # creation of data
# # =============================================================================
# #n, dim = 1400, 1  # number of samples, dimension
# #n_bkps, sigma = 4, 5  # number of change points, noise standart deviation
# #signal, bkps = rpt.pw_constant(n, dim, n_bkps, noise_std=sigma)
# #df=pd.DataFrame(data=signal)
# # =============================================================================
# 
# 
# def get_side(df,side):
#     if (side=="left"):
#         return(df.iloc[:,0:8])
#     elif(side=="right"):
#         return(df.iloc[:,8:16])
#     else:
#         return(df)
#     
# 
# def cost_mld(df,u,v):
#     data=get_side(df,side).iloc[u:v,:]
#     #####Estimation de l'espérance par max_vrais=moyenne empirique
#     mean_estimate=data.mean()
#     #mean_estimate=[0]*data.shape[0]
#     #mean_estimate=[0 for i in range(data.shape[1])]
#     
#     ###### Estimation de la variance
#     var_estimate=data.cov()
#     
#     cost=0
# # =============================================================================
# #     cost1=0
# #     for i in range(data.shape[0]):
# #         cost1=cost1+np.linalg.norm(np.asarray(data.iloc[i,:])-mean_estimate)
# # =============================================================================
# # =============================================================================
# # # =============================================================================
#     if(abs(np.linalg.det(var_estimate))>1e-5):
#          #inv=np.linalg.inv(var_estimate)
#          #cost=cost+(v-u)*np.log((np.linalg.det(var_estimate)))
#          for i in range(data.shape[0]):
#              #temp=np.transpose(np.asarray(data.iloc[i,:])).dot(inv.dot(np.asarray(data.iloc[i,:])))
#              temp=np.log(multivariate_normal.pdf(np.asarray(data.iloc[i,:]),np.asarray(mean_estimate),var_estimate,allow_singular=True))
#              cost=cost+temp
# 
# 
#             
#     return -cost
# 
# 
# 
#         
# def solve_segmentation(df,side,width,nsteps,cost):
#     n=df.shape[0]
#     cost_list1=list()
#     cost_list2=list()
#     cost_list_adj=list()
#     for i in range(width,n-width):
#         print("i = ",i)
#         cost_list1.append(cost(df,i-width,i,side)+cost(df,i,min(i+width,n),side))
#         #cost_list2.append(cost(df,i+size,min(i+2*size,n),side))
#         cost_list_adj.append(cost(df,i-width,i+width,side))
# 
#     #L=list_diff(cost_list1,cost_list_adj)
#     cost_index=[i for i in range(width,n-width)]
#     L=abs(np.asarray(cost_list_adj)-np.asarray(cost_list1))
#     # for i in range(len(L)):
#     #     if L[i]<(L.max()/4):
#     #         L[i]=0
# 
#     indexes=list() 
#     begin=0
#     end=0
#     test=0
#     count=0
#     for i in range(len(L)):
#         
#         
#         if (L[i]>0)&(test==0):
#             begin=cost_index[i]
#             test=1
#         if (L[i]==0)&(test==1):
#             test=0
#             end=cost_index[i-1]
#             indexes.append((begin,end))
#             count=count+1
#         
#     return (L,cost_index,indexes)
# 
# 
#     
# # res=solve_segmentation(df,"right",20,5,cost_mld)
# # index=res[2]
# # plt.cla()
# # plt.clf()
# # fig, axs = plt.subplots(2,1)
# # axs[0].plot(df.iloc[:,1])
# # axs[1].plot(res[1],res[0])
# 
# # for i in index:
# #      axs[0].axvline(x=i[0],color='red',ls='--')
# #      axs[0].axvline(x=i[1],color='green',ls='--')
#     
# 
# =============================================================================
