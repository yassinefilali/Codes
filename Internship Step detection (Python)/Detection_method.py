import pandas as pd
import numpy as np
from scipy.stats import multivariate_normal
from scipy.signal import argrelmax
from math import log
from ruptures.base import BaseCost
import ruptures as rpt

class MyCost(BaseCost):

    """Custom cost for exponential signals."""

    # The 2 following attributes must be specified for compatibility.
    model = "gaussian"
    min_size = 2

    def fit(self, signal):
        """Set the internal parameter."""
        self.signal = signal
        self.cumsum = np.cumsum(signal,axis=0)
        cumsum1=[0]
        for i in range(signal.shape[0]):
            y=signal[i].reshape((signal.shape[1],1))
            cumsum1.append(cumsum1[i]+y.dot(np.transpose(y)))
        self.cumsum1=cumsum1
            
            
        return self

    def error(self, start, end):
        sub = self.signal[start:end,:]
        mean=1/len(sub)*(self.cumsum[end-2,:]-self.cumsum[max(0,start-1),:])
        term1=1/len(sub)*(self.cumsum1[end-1]-self.cumsum1[start-1])
        term2=mean.dot(np.transpose(mean))
        var=term1-term2
        #var = pd.DataFrame(sub).cov()
        cost=(end-start)*np.linalg.slogdet(var)[1]
        return cost

class kernel_linear(BaseCost):

    """Custom cost for exponential signals."""

    # The 2 following attributes must be specified for compatibility.
    model = "lin ker"
    min_size = 2


    def fit(self, signal):
        """Set the internal parameter."""
        self.signal = signal
        self.cumsum = np.cumsum(signal,axis=0)
        norm=np.linalg.norm(signal,axis=1)
        self.cumsum1 = np.cumsum(norm*norm)
        return self

    def error(self, start, end):
        sub = self.signal[start:end,:]
        first = self.cumsum1[end-1]-self.cumsum1[start]
        vect= self.cumsum[end-1]-self.cumsum[start]
        second = np.linalg.norm(vect)
        cost= first-(1/len(sub))*second*second
        return cost
    

    
def cost_mld(df,u,v):
    data=df.iloc[u:v]
    #mean_estimate=(M[v]-M[u])/(v-u)
    mean_estimate=data.mean()
    var_estimate=data.cov()
    
    cost=0
    if(abs(np.linalg.det(var_estimate))>1e-5):
         for i in range(data.shape[0]):
             temp=np.log(multivariate_normal.pdf(data.iloc[i,:],mean_estimate,var_estimate,allow_singular=True))
             cost=cost+temp
    return -cost

def cost_simp(df,u,v):
    data=df.iloc[u:v,:]
    #mean_estimate=data.mean()
    var_estimate=data.cov()
    
    #cost=0
    #if(abs(np.linalg.det(var_estimate))>1e-5):
         #inv=np.linalg.inv(var_estimate)
    cost=(v-u)*np.linalg.slogdet(var_estimate)[1]
# =============================================================================
#          for i in range(data.shape[0]):
#              temp=np.transpose(np.asarray(data.iloc[i,:])).dot(inv.dot(np.asarray(data.iloc[i,:])))
#              
#              cost=cost+temp
# =============================================================================
    return cost


    
def adjust_segment(seg):
    S=seg
    i=0
    while (i<len(S)-1):
        L=seg[i][1]-seg[i][0]
        actual=L
        
        if (L<20):
            k=i
            actual_segment=S[i]
            chain=[]
            chain.append(seg[i])
            while(seg[k+1][1]-seg[k+1][0]<20)and(k+1<len(seg)-1):
                chain.append(seg[k+1])
                k=k+1
            if (len(chain)>=2):
                for p in range(1,len(chain)):
                    S.remove(chain[p])
                actual_segment=[chain[0][0],chain[len(chain)-1][1]]
            elif len(chain)==1:
                actual_segment=[chain[0][0],S[k][0]]
                S.remove(S[k])
            S[i]=actual_segment  
        #while (S[i][1]-S[i][0])<50:
        #   S[i][0]=S[i][0]-10
        #   S[i-1][1]=S[i-1][1]-10
        i=i+1
    my_bkps=[i for i in set(np.asarray(S).flatten()) if i>0]
    my_bkps.sort()
    segs1=[]
    segs1.append([0,my_bkps[0]])
    for i in range(len(my_bkps)-1):
        segs1.append([my_bkps[i],my_bkps[i+1]])
        
    return(segs1)
        

def solve_segmentation_window(df,width,cost):
    print("running solve_segmentation_window")
    n=df.shape[0]
    cost_list1=list()
    cost_list_adj=list()
    for i in range(width,n-width):
        print(i)
        cost_list1.append(cost(df,i-width,i)+cost(df,i,min(i+width,n)))
        cost_list_adj.append(cost(df,i-width,i+width))
    cost_index=[i for i in range(width,n-width)]
    L=abs(np.asarray(cost_list_adj)-np.asarray(cost_list1))
    indexes=list() 
    begin=0
    end=0
    test=0
    count=0
    for i in range(len(L)):
        
        
        if (L[i]>0)&(test==0):
            begin=cost_index[i]
            test=1
        if (L[i]==0)&(test==1):
            test=0
            end=cost_index[i-1]
            indexes.append((begin,end))
            count=count+1
        
    return (L,cost_index,indexes)






