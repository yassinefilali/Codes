from numpy import *
import os
from PIL import Image

#a est le chemin d'un fichier image
def imgtomtrx(a):
    wd=os.getcwd()
    name=(a[a.rfind("\\")+1:len(a)])
    print(name)
    I=asarray(Image.open(a).convert('L'))
    fl=open(wd+"\\temp.txt","w")
    fl.write(wd+"\\textfiles\\"+name+".txt")
    fl.close()
    txt=wd+"\\textfiles\\"+name+'.txt'
    f=open(txt,"w")
    f.write(str(I.shape[0])+'-'+str(I.shape[1])+"\n")

    for i in range(I.shape[0]):
        line=''
        for j in range(I.shape[1]):
            line=line+str(I[i][j])+' '
        f.write(line+"\n")
    f.close()

a=input("saisir le chemin de l'image :")
im=a;
imgtomtrx(im)








