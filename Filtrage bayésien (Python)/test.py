import numpy as np # calcul numerique
import numpy.random as rnd # fonctions pseudo-aleatoires
import matplotlib.pyplot as plt # fonctions graphiques a la MATLAB
import matplotlib.animation as anim # fonctions d'animation
import scipy.io as io # fonctions pour l'ouverture des fichiers .mat de MATLAB
import math
X1MIN=-10000
X1MAX=10000
X2MIN=-10000
X2MAX=10000
r0=(-6000,2000)
v0=(120, 0)
nmax=100
delta=1



folder="C:/Users/Yassine/Desktop/tp filtrage/"
map=io.loadmat(folder+'mnt.mat')['map']
N1 = map.shape[1]
N2 = map.shape[0]
#plt.imshow(map,cmap='jet',extent=[X1MIN,X1MAX,X2MIN,X2MAX])
traj = io.loadmat(folder+'traj.mat')
rtrue = traj['rtrue']
vtrue = traj['vtrue']
#plt.plot(rtrue[0,:],rtrue[1,:],'r-')


a_INS = io.loadmat(folder+'ins.mat')['a_INS']
r_INS = np.zeros(rtrue.shape)
v_INS = np.zeros(vtrue.shape)
r_INS[:,0] = r0
v_INS[:,0] = v0
for k in range(1,nmax):
    r_INS[:,k] = r_INS[:,k-1]+delta*v_INS[:,k-1]
    v_INS[:,k] = v_INS[:,k-1]+delta*a_INS[:,k-1]
#plt.plot(r_INS[0,:],r_INS[1,:],'m-')

Rtrue = io.loadmat(folder+'traj.mat')['rtrue']
x=Rtrue[0,:]
y=Rtrue[1,:]
H=np.zeros(101,)
for i in range(nmax+1):
    xi=x[i]
    yi=y[i]
    a=int(((X2MAX-yi)/(X2MAX-X2MIN))*N2)
    b=int(((xi-X1MAX)/(X1MAX-X1MIN))*N1)
    H[i,]=map[a,b]

    

    
h_ALT = io.loadmat(folder+'alt.mat')['h_ALT'][0]
#plt.plot(np.linspace(0,100,101),h_ALT)
plt.plot(np.linspace(0,100,101),H)
plt.scatter(np.linspace(0,100,101),h_ALT, s=40,c = 'red', marker='+')
