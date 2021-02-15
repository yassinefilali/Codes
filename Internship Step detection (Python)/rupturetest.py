import numpy as np
import matplotlib.pylab as plt
import ruptures as rpt
from Data_op import *
from Detection_method import *
from metrics import *
from os import listdir
from sklearn import preprocessing
import random
# creation of data
# =============================================================================
random.seed(30)
n = 1000  # number of samples
n_bkps, sigma = 5, 5  # number of change points, noise standart deviation
signal, bkpss = rpt.pw_constant(n, 1, n_bkps, noise_std=sigma)

class MyCost(BaseCost):

    """Custom cost for exponential signals."""

    # The 2 following attributes must be specified for compatibility.
    model = "simp"
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
        return cost/1000
# =============================================================================
# =============================================================================
data=get_side_data(data_acquisition(r"C:\Users\Yassine\Desktop\Datacamp\challenge\data\test\4-58.csv"),'left')
meta_data=data[1]
steps=meta_data
d=np.abs((data[0].iloc[:,0:4]))

d=pd.DataFrame(preprocessing.scale(d))
left_right=(data[0].iloc[:,0:4]).apply(lambda x: np.abs(x)).rolling(20).mean().fillna(0)
right_left=(data[0].iloc[::-1,0:4]).apply(lambda x: np.abs(x)).rolling(20).mean().fillna(0)
t=((right_left+left_right)/2)
t1=t.iloc[::-1].rolling(20).sum().fillna(0)
t2=t.rolling(20).sum().fillna(0)
t=((t1+t2)/2)
zebi=d.rolling(10, win_type='triang').mean()
signals=np.asarray(d)

n=len(signals)
#dim=signals.shape[1]

signal=signals
signal=np.asarray(t)
#signal=preprocessing.scale(t)
sigma=signal.std()
#sigma=signals.std()
#signals=signals.reshape(signals.shape)

bkps=np.asarray(steps)
bkps=bkps.reshape(bkps.shape[1]*bkps.shape[0])
# =============================================================================
# =============================================================================
 # "l1", "rbf", "linear", "normal", "ar"

algo = rpt.BottomUp(model='rbf',jump=1).fit(signals)
#my_bkps1 = np.asarray(algo.predict(n_bkps=len(bkps)))
my_bkps1 = np.asarray(algo.predict(pen=1))

segs1=[]
segs1.append([0,my_bkps1[0]])
for i in range(len(my_bkps1)-1):
    segs1.append([my_bkps1[i],my_bkps1[i+1]])
segs=segs1
segs=adjust_segment(segs1)

signal=np.asarray(t)
maximum,file=argrelmax(signal, order=50)
L=[]
for stk in range(4):
    ind=[i for i in range(len(maximum)) if file[i]==0]
    L.append([maximum[i] for i in ind])
inter=pd.DataFrame(L)
z = list(inter.mean())
my_bkps=[i for i in set(np.asarray(segs).flatten()) if i>0]
print(len(my_bkps))

#my_bkps = np.asarray(algo.predict(pen=10000000000))
# show results
rpt.show.display(signals,bkps, my_bkps , figsize=(10, 6))
plt.show()
