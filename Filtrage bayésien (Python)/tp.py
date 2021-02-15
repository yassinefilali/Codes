########################################################################
#### TP SOD333 : Recalage altimetrique de navigation inertielle #######
########################################################################
########################################################################
########################################################################
########################################################################
#Importation des bibliothèques nécessaires
import numpy as np # calcul numerique
import numpy.random as rnd # fonctions pseudo-aleatoires
import matplotlib.pyplot as plt # fonctions graphiques a la MATLAB
import matplotlib.animation as anim # fonctions d'animation
import scipy.io as io # fonctions pour l'ouverture des fichiers .mat de MATLAB
import math
###############################################################
#Initialisation des données
X1MIN=-10000
X1MAX=10000
X2MIN=-10000
X2MAX=10000
r0=(-6000,2000)
v0=(120, 0)
nmax=101
delta=1
T=100
###############################################################
#Importation des données relatives au problème
#Preciser le chemin du dossier danslequel se trouvent les fichiers
folder='C:/Users/Yassine/Desktop/paprasse/tp filtrage/'
Rtrue = io.loadmat(folder+'traj.mat')['rtrue']
h_ALT = io.loadmat(folder+'alt.mat')['h_ALT'][0]
traj = io.loadmat(folder+'traj.mat')
###############################################################


#Question 1
map=io.loadmat(folder+'mnt.mat')['map']
N1 = map.shape[1]
N2 = map.shape[0]
plt.imshow(map,cmap='jet',extent=[X1MIN,X1MAX,X2MIN,X2MAX])
rtrue = traj['rtrue']
vtrue = traj['vtrue']
plt.plot(rtrue[0,:T],rtrue[1,:T],'r-')


#Question 2
a_INS = io.loadmat(folder+'ins.mat')['a_INS']
r_INS = np.zeros(rtrue.shape)
v_INS = np.zeros(vtrue.shape)
r_INS[:,0] = r0
v_INS[:,0] = v0
for k in range(1,T):
    r_INS[:,k] = r_INS[:,k-1]+delta*v_INS[:,k-1]
    v_INS[:,k] = v_INS[:,k-1]+delta*a_INS[:,k-1]
plt.plot(r_INS[0,:T],r_INS[1,:T],'m-')


#Question 3
deltark=np.zeros(rtrue.shape)
deltavk=np.zeros(vtrue.shape)
deltark[:,0] = (0,0)
deltavk[:,0] = (0,0)
mean=[0,0]
cov= [[49, 0], [0,49]]

for k in range(1,nmax):
    wkINS=np.random.multivariate_normal(mean,cov)
    deltark[:,k] = deltark[:,k-1]+delta*deltavk[:,k-1]
    deltavk[:,k] = deltavk[:,k-1]-delta*wkINS
plt.imshow(map,cmap='jet',extent=[X1MIN,X1MAX,X2MIN,X2MAX])
plt.plot(r_INS[0,:T],r_INS[1,:T],'m-',label ="r_INS")
plt.plot(rtrue[0,:T],rtrue[1,:T],'r-',label ="r_true")
plt.plot(r_INS[0,:T]+deltark[0,:T],r_INS[1,:T]+deltark[1,:T],'g-',label ="r_INS + delta_rk")
plt.legend()
#Question 4
X=[]
Y=[]
H=[]
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for j in range(N1):
    for i in range(N2):
        xi=((X2MAX-i)/(X2MAX-X2MIN))/N2
        xj=((X1MAX-j)/(X1MAX-X1MIN))/N1
        X.append(xi)
        Y.append(xj)
        H.append(map[i,j])
ax.scatter(X, Y, H)
ax.set_xlabel('r_horizontale')
ax.set_ylabel('r_verticale')
ax.set_zlabel('h(r)')
plt.show()

#Question 5
x=Rtrue[0,:]
y=Rtrue[1,:]
H=np.zeros(T+1,)
for i in range(nmax):
    xi=x[i]
    yi=y[i]
    a=int(((X2MAX-yi)/(X2MAX-X2MIN))*N2)
    b=int(((xi-X1MAX)/(X1MAX-X1MIN))*N1)
    H[i,]=map[a,b]
    
#plt.plot(np.linspace(0,100,101),h_ALT)
plt.plot(np.linspace(0,T,T+1),H,label ="profill exact")
plt.scatter(np.linspace(0,T,T+1),h_ALT, s=40,c = 'red', marker='+',label ="profil estimé")
plt.legend()



#Question 6
sigma_barre=20
sigma_ALT=10
sigma_tot=np.sqrt(sigma_barre**2+sigma_ALT**2)
#définition de la fonction de vraisemblance
def vraisemblance(ksi,k):
    r=ksi[0:2]
    a=int(((X2MAX-r[1])/(X2MAX-X2MIN))*N2)
    b=int(((r[0]-X1MAX)/(X1MAX-X1MIN))*N1)
    if (a+1,b+1) < map.shape:
        hr=map[a,b]
        alpha = np.exp( (-0.5*(h_ALT[k]-hr)**2)/(sigma_tot)**2)
        return(alpha)
    else:
        a=map.shape[0]-1
        b=map.shape[1]-1
        hr=map[a,b]
        alpha = np.exp( (-0.5*(h_ALT[k]-hr)**2)/(sigma_tot)**2)
        return(alpha)


#Question 7 et 8
##############################################################################################
# definition d'une fonction donnant les indices des ancetres dans la redistribution multinomiale
def resampling_multi(w,N):
    u_tild = np.zeros((N))
    expo = np.zeros((N))
    alpha = np.zeros((N))
    u_ord = np.zeros((N))
    uu = np.zeros((N+1))
    s = np.zeros((N))
#
    w = w/w.sum()
    s = np.cumsum(w)
    u_tild = rnd.uniform(0,1,N)
#
    for i in range(N):
        alpha[i] = u_tild[i]**(1/float(i+1))
    alpha = np.cumprod(alpha)
    u_ord = alpha[N-1]/alpha
    u = np.append(u_ord,float("inf"))
#
    ancestor = np.zeros(N,dtype=int)
    offsprings = np.zeros(N,dtype=int)
    i = 0
    for j in range(N):
        o = 0
        while u[i]<=s[j]:
            ancestor[i] = j
            i = i+1
            o = o+1
        offsprings[j] = o
    return ancestor
##############################################################################################
#Choix du nombre de particules
N=1000
#Initialisation
cov= [[10000, 0,0,0],[0,10000,0,0] ,[0,0,100, 0],[0,0,0,100]]
mean=[0,0,0,0]
cov1= [[49, 0], [0,49]]
mean1=[0,0]

Ksi=[]
W=[]
Ksi_hat=[]
Y0=h_ALT[0]
W0=[]
#Initialisation des poids à l'instant initial
X_INS_0=np.asarray([r_INS[:,0],v_INS[:,0]]).reshape(4)
X0=np.random.multivariate_normal(mean,cov,size=N)
Ksi.append(X0)
for i in range(N):
    Xi0=X0[i]
    Wi0=vraisemblance(X_INS_0+Xi0,0)/sum([vraisemblance(X_INS_0+r, 0) for r in X0 ])
    W0.append(Wi0) 
W0=np.array(W0)    
W.append(W0)  


#Choix de la constante c: 0 ==> algorithme SIS // 1 ==> algorithme SIR
c=1

#Début de l'algorithme
for k in range(1,T):
    print("Avancement en % : ",k*100/T,"%")

    Neff=1/sum([e**2 for e in W[k-1]])    
    if Neff<=c*N: #Debut de l'algorithme SIR
        #l'étape de rééchantillonnage
        indices = resampling_multi(np.asarray(W[k-1]),N)
        Ksi_hat_k=np.asarray([Ksi[k-1][i] for i in indices])
        #l'étape de prédiction
        X_INS_k=np.asarray([r_INS[:,k],v_INS[:,k]]).reshape(4)
        L=[]
        for i in range(N):
            Wins=np.random.multivariate_normal(mean1,cov1)
            r= Ksi_hat_k[i,0:2]+delta* Ksi_hat_k[i,2:4]
            v= Ksi_hat_k[i,2:4]-delta*Wins
            L.append(np.asarray([r,v]).reshape(4))
            #X0[indices[i]]=X_hat
            #print("after  ",X_hat)
        Ksi.append(L)
        #L'étape de correction
        L=[]
        s=sum([vraisemblance(X_INS_k+p, k) for p in Ksi[k] ])
        for l in range(N):
            r=Ksi[k][l]
            L.append(vraisemblance(X_INS_k+r,k)/s)
        W.append(L)
        
    else: #Debut de l'algorithme SIS
        #l'étape de prédiction
        Ksi_hat_k=np.asarray(Ksi[k-1])
        X_INS_k=np.asarray([r_INS[:,k],v_INS[:,k]]).reshape(4)
        L=[]
        for i in range(N):
        
            Wins=np.random.multivariate_normal(mean1,cov1)
            r= Ksi_hat_k[i,0:2]+delta* Ksi_hat_k[i,2:4]
            v= Ksi_hat_k[i,2:4]-delta*Wins
            L.append(np.asarray([r,v]).reshape(4))
            #X0[indices[i]]=X_hat
            #print("after  ",X_hat)
        Ksi.append(L)
        #L'étape de correction
        L=[]
        s=sum([W[k-1][i]*vraisemblance(X_INS_k+Ksi[k][i], k) for i in range(1,N)])
        for i in range(N):
            r=np.asarray(Ksi[k][i])
            L.append(W[k-1][i]*vraisemblance(X_INS_k+r,k)/s)
        W.append(L)
        

#Définition de le distribution empirique pondérée
correction_t=[]
for i in range(T):
    W_t=W[i]
    corr_t=Ksi[i]
    corr_final=np.zeros(4)
    for j in range(N):
        corr_final=corr_final+W_t[j]*corr_t[j]
    correction_t.append(corr_final)
dt=np.asarray(correction_t)    

#Affichage des résultats obtenus
#plt.plot(r_INS[0,:100]+dt[:,0],r_INS[1,:100]+dt[:,1],'y-')
#from os import path
for i in range(T):
    fig,ax= plt.subplots()
    plt.clf()
    plt.imshow(map,cmap='jet',extent=[X1MIN,X1MAX,X2MIN,X2MAX])
    arr1=plt.plot(r_INS[0,:],r_INS[1,:],'m-',label='Traj INS')
    arr2=plt.plot(rtrue[0,:],rtrue[1,:],'r-',label='Traj reélle')
    arr3=plt.plot(r_INS[0,:100]+dt[:,0],r_INS[1,:100]+dt[:,1],'y-',label='traj en moyenne des particules')
    arr4=plt.plot(r_INS[0,i]+np.asarray(Ksi[i])[:,0],r_INS[1,i]+np.asarray(Ksi[i])[:,1],
                  'k-',
                  label='Nuage des particules',
                  marker='o')
    plt.legend(loc ="lower left")
    plt.draw()
    # outpath="C:/Users/Mohamed El Khames/Desktop/KHAMES-TA/KHAMES-TA(3eme année)/Cours/SOD333/tp"
    # fig.savefig(path.join(outpath,"{0}.png".format(i)))
    plt.pause(0.1)
   

plt.close()
########################################################################
############################## FIN #####################################
