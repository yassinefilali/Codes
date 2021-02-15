#include <iostream>
#include <stdlib.h>
#include <fstream>
#include <sstream>
#include "fichier.h"
#include "indexeur.h"
#include "lecteur.h"
#include "analyseur.h"
#include "directory.h"
#include "MdR.h"
#include "MdRone.h"
#include <iterator>
#include <algorithm>
#include <string>
#include <vector>
#include<bits/stdc++.h>

bool sortbysec(const pair<string,int> &a,
              const pair<string,int> &b)
{
    return (a.second > b.second);
}

vector<pair <string,int> > MdRone::rechercher(string str){
   I.loadindex();
   string recherche=str;
   transform(recherche.begin(), recherche.end(), recherche.begin(), ::toupper);
   map<fichier,int> classement;
   vector<pair <string,int> > classing;
   vector<string> mots;
   int n=recherche.size();
   int i;
   string temp;
   for (i=0;i<n;i++){
        if(recherche[i]==' '){
            mots.push_back(temp);
            temp="";
        }
        else if (i==n-1) {
            temp=temp+recherche[i];
        mots.push_back(temp);}
        else {temp=temp+recherche[i];}

   }
   n=mots.size();
   map<string,map<string,int> > index=I.getindex();
   for (i=0;i<n;i++){
        map<string,int> detail=index[mots[i]];
        map<string,int>::iterator i;
        for (i=detail.begin(); i != detail.end(); ++i)
        {
            string path=i->first;
            fichier f(path.c_str());
            int occur=i->second;
            classement[f]+= occur;
        }

    }
    map<fichier,int>::iterator it;
        for (it=classement.begin(); it != classement.end(); ++it)
        {
            fichier f=it->first;
            int occ=it->second;
            string p=f.getpath();
            classing.push_back( make_pair(p,occ) );

        }
        sort(classing.begin(), classing.end(), sortbysec);
        return classing;





};



MdRone::MdRone(indexeur Ind):MdR(Ind) {cout << "moteur de recherche 1 cree" << endl;}
