#include <iostream>
#include <iomanip>
#include <fstream>
#include <dirent.h>
#include <cstring>
#include <sstream>
#include <algorithm>
#include <string>
#include <sys/types.h>
#include "analyseur.h"
#include "analyseurbis.h"
#include "fichier.h"
#include "lecteur.h"
#include "directory.h"
#include "indexeur.h"
#include "MdR.h"
#include "ana.h"
#include "MdRone.h"
#include "MdRtwo.h"

#include<bits/stdc++.h>

using namespace std;



int main()
{

















    lecteur *L;
    L=new lecteur();
    ana *A;
    cout << "------------Choisir l analyseur a utiliser:                                  ------------" << endl;
    cout << "------------Pour utiliser l analyseur 1 (Sans aucun test) taper 1            ------------" << endl;
    cout << "------------Pour utiliser l analyseur 2 (test mots d'arret) taper 2          ------------" << endl;
    int a=0;
    while ((a!=1)&&(a!=2)){
            cout << "## ";
            cin >> a;
            cout << endl;}
    if (a==2){
    A=new analyseur(*L); }
    else {
    A=new analyseurbis(*L); }
    indexeur *I;
    MdR *M;
    I=new indexeur(A);
    cout << "------------Choisir la methode de recherche:                                 ------------" << endl;
    cout << "------------Pour utiliser la methode 1 (passage par une structure intermediaire) taper 1-" << endl;
    cout << "------------Pour utiliser la methode 2 (utilisation directe du fichier index) taper 2----" << endl;
    int m=0;
    while ((m!=1)&&(m!=2)){cout << "## ";
        cin >> m;
        cout << endl;}
    if (m==1){
    M=new MdRone(*I); }
    else {
    M=new MdRtwo(*I); }

    M->loaddir();

    int j;

    cout << "------------Repertoires de recherche:                                        ------------" << endl;
    vector<directory> dir=M->getdir();
    int n=dir.size();
    cout << "nombre de repertoires: " << n << endl;
    if (n==0){
        cout << "Veuillez ajouter le chemin d'un repertoire (Aucun repertoire de recherche):";
        string k;
        cin.ignore();
        getline(cin,k);
        directory rep(k);
        M->adddir(rep);
        M->loaddir();

    }
    dir=M->getdir();
    n=dir.size();
    for (j=0;j<n;j++){cout << dir[j].getpath() << endl;}
    int q=5;

    do {
    cout << "------------Taper le nombre correspondant pour effectuer l'action souhaitee: ------------" << endl;
    cout << "------------0: Quitter                                                       ------------" << endl;
    cout << "------------1: Indexer                                                       ------------" << endl;
    cout << "------------2: Effectuer une recherche                                       ------------" << endl;
    cout << "------------3: Ajouter/supprimer un repertoire                               ------------" << endl;
    cout << endl;
    cout << "## " ;
    cin >> q;
    if (q!=0){
    M->loaddir();
    dir=M->getdir();
    n=dir.size();

    if (q==1){
        clock_t start, ending;
        start = clock();
        M->indexer();
        ending = clock();
        cout << "temp d'indexation = " << double(ending-start)/ double(CLOCKS_PER_SEC)<< setprecision(5) << " secondes" << endl;
    }
    else if (q==2){
            M->getindex().loadindex();

            cout << "Taper l'expression de la recherche:" << endl;
            cout << "## ";

            string k;
            cin.ignore();
            getline (cin,k);
            vector<pair <string,int> > classement= M->rechercher(k);
            int siz=classement.size();
            for (j=0;j<min(5,siz);j++){
                    cout << classement[j].first << "      " << classement[j].second << endl;
            }
            cout << "recherche effectuee" << endl;
            cout << q << endl;



    }
    else if (q==3) {
        cout << "------------Ajout : Taper 1                              Suppression : Taper 2------------" << endl;
        int mod;
        cout << "## ";
        cin >> mod;
        if (mod==2){string path;
        cin.ignore();
        if(n!=0){
        cout << "Liste des repertoire" << endl;
        for (j=0;j<n;j++){cout << dir[j].getpath() << endl;}}
        cout << endl;
        cout << "Saisir le chemin du repertoire a supprimer" << endl;
        cout << "## ";
        getline(cin,path);
        directory k(path);
        M->deletedir(k);
        M->loaddir();}
        else if (mod==1) {string path;
        cout << "Saisir le chemin du repertoire a ajouter" << endl;
        cout << endl;
        cin.ignore();

        cout << "## " ;
        getline(cin,path);
        directory k(path);
        M->adddir(k);
        M->loaddir();}
         }






    }}while(q!=0);}
/*    cout << "Souhaitez-vous indexer les fichiers ?" << endl;
    cout << "Oui: tapez 1              Non: tapez 0" << endl;
    int i;
    cin >> i;
    if (i==1) {M->indexer();}
    M->getindex().loadindex();
    int r=1;
    while (r==1){
        cout << "Souhaitez vous effectuer une recherche ?" << endl;
        cout << "Oui: tapez 1              Non: tapez 0" << endl;
        cin >> r;
        if (r==1) {
            cout << "Tapez l'expression de recherche:" << endl;

            string k;
            cin.ignore();
            getline (cin,k);
            cout << k << endl;
            vector<pair <string,int> > classement= M->rechercher(k);
            for (j=0;j<6;j++){
                    cout << classement[j].first << "      " << classement[j].second << endl; */






/*








/*    fichier *f;
    fichier *d;
    fichier *g;
    directory *dir;
    dir=new directory("C:/Users/Asus/Desktop/test");
    vector<fichier> liste=dir->getfiles();
    int n=liste.size();
    int i;
    for (i=0;i<n;i++){
        I->indexer(liste[i]);
        cout << i << endl;
    }
    I->saveindex();  */

    /*fichier f("123");
   fichier d("456");
   map<fichier,int> classement;
   classement[f]+=3;
   classement[d]=2;
   map<fichier,int>::iterator i;
   for (i=classement.begin(); i != classement.end(); ++i)
        {
            fichier file=i->first;
            int occur=i->second;
            cout << file.getpath() << "--" << occur << endl;
        }  /*





/*
   directory *d;
   directory *p;
   d=new directory("directory 1");
   p=new directory("directory 2");
   vector<directory> L;
   L.push_back(*d);
   L.push_back(*p);
   vector<directory>::iterator it;
   it = find (L.begin(), L.end(), *d);
  if ( it==L.end() )
    {
        cout << "directory not found." << endl;
    }
    else
    {
        L.erase(it);
        cout << d->getpath() << " deleted." << endl;
    }
*/






/*
    indexeur *I;

    analyseur *A;
    lecteur *L;
    MdR *yassine;
    L=new lecteur();
    A=new analyseur(*L);
    I=new indexeur(*A);
    yassine=new MdR(*I);
    directory *d;
    directory *dp;
    d=new directory("C:/Users/Asus/Desktop/Projet c++/Moteur de recherche/test");
    dp=new directory("C:/Users/Asus/Desktop/Projet c++/Moteur de recherche/test1");
    yassine->adddir(*d);
    yassine->adddir(*dp);
    yassine->deletedir(*d);
    yassine->indexer();
*/




/*
    directory *d;
    d=new directory("C:/Users/Asus/Desktop/Projet c++/Moteur de recherche/test");

    vector<fichier> liste=d->getfiles();
    int z;
    i->indexreset();
    for (z=0;z<liste.size();z++){
    i->indexer(liste[z]); }
    i->saveindex();
    delete i;
    delete A;
    delete L;  */














   /* fichier *f;
    lecteur *L;
    analyseur *An;
    L=new lecteur();
    f=new fichier("C:/Users/Asus/Desktop/Projet c++/Moteur de recherche/test.txt");
    An=new analyseur();
    vector<string> l=L->readfile(*f);
    map<string,int> detail=An->analyser(l);
    map<string,int>::iterator itr;
    for (itr=detail.begin(); itr != detail.end(); ++itr) {
        cout << itr->first << "     " << itr->second << endl;
    }
    delete An;
    delete f;
    delete L; */


