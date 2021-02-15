import numpy as np # calcul numerique
import numpy.random as rnd # fonctions pseudo-aleatoires
import matplotlib.pyplot as plt # fonctions graphiques a la MATLAB
import matplotlib.animation as anim # fonctions d’animation
import scipy.io as io # fonctions pour l’ouverture des fichiers .mat de MATLAB
import math
d="C:/Users/Yassine/Desktop/tp filtrage/"
map = io.loadmat(d+'mnt.mat')['map']
N1 = map.shape[1]
N2 = map.shape[0]
X1MIN=-10000
X2MIN=-10000
X1MAX=10000
X2MAX=10000
r0=(-6000,2000)
v0=(120,0)
delta=1
T=100
nmax= T
#plt.imshow(map,cmap='jet',extent=[X1MIN,X1MAX,X2MIN,X2MAX])
traj = io.loadmat(d+'traj.mat')
rtrue = traj['rtrue']
vtrue = traj['vtrue']
#plt.plot(rtrue[0,:],rtrue[1,:],'r-')

a_INS = io.loadmat(d+'ins.mat')['a_INS']
r_INS = np.zeros(rtrue.shape)
v_INS = np.zeros(vtrue.shape)
r_INS[:,0] = r0
v_INS[:,0] = v0
for k in range(1,nmax+1):
    r_INS[:,k] = r_INS[:,k-1]+delta*v_INS[:,k-1]
    v_INS[:,k] = v_INS[:,k-1]+delta*a_INS[:,k-1]
#plt.plot(r_INS[0,:],r_INS[1,:],'m-')


w_INS = np.zeros(a_INS.shape)
delta_r_INS = np.zeros(rtrue.shape)
delta_v_INS = np.zeros(vtrue.shape)
delta_r_INS[:,0] = 0
delta_v_INS[:,0] = 0
sigma_INS=7
mean=np.asarray([0,0])
for k in range(1,nmax+1):
    delta_r_INS[:,k] = delta_r_INS[:,k-1]+delta*delta_v_INS[:,k-1]
    var=(sigma_INS**2)*np.diag((1,1))
    w_INS[:,k-1]=np.random.multivariate_normal(mean,var)
    delta_v_INS[:,k] = delta_v_INS[:,k-1]-delta*w_INS[:,k-1]
   
#plt.plot(delta_r_INS[0,:],delta_r_INS[1,:],'m-')

r=r_INS+delta_r_INS
v=v_INS+delta_r_INS
#plt.plot(r[0,:],r[1,:],'m-',color="green")
## l'axe des Y
I=[ int((X2MAX-x2)*N2/(X2MAX-X2MIN)) for x2 in rtrue[0,:]]


J=[ int((x1-X1MIN)*N2/(X1MAX-X1MIN)) for x1 in rtrue[1,:]]

T_grid=[i for i in range(T+1)]
h_ALT = io.loadmat('alt.mat')['h_ALT']
x=rtrue[0,:]
y=rtrue[1,:]
VALS=[]
for i in range(nmax+1):
    xi=x[i]
    yi=y[i]
    a=int(((X2MAX-yi)/(X2MAX-X2MIN))*N2)
    b=int(((xi-X1MAX)/(X1MAX-X1MIN))*N1)
    VALS.append(map[a,b])
    



        
plt.plot(T_grid,VALS)
plt.scatter(T_grid,h_ALT,c = 'red', marker='+')
        