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
#include <iterator>
#include <algorithm>
#include <string>
#include <vector>
#include<bits/stdc++.h>
/*
bool sortbysec(const pair<string,int> &a,
              const pair<string,int> &b)
{
    return (a.second > b.second);
}
*/

MdR::MdR(indexeur Ind):I(Ind) {}

indexeur MdR::getindex(){return I;};

void MdR::savedir()
{
    ofstream f;
    f.open(filedir.c_str(),ios::out);
    int n=dir.size();
    int i;
    for(i=0; i<n; i++)
    {
        f << dir[i].getpath() << endl;
    }
    f.close();

}

void MdR::adddir(directory d)
{   vector<directory>::iterator it;
    it = find (dir.begin(), dir.end(), d);
    if ( it==dir.end() )
    {
        dir.push_back(d);
        cout << d.getpath() << " a ete ajoute." << endl;
    }
    else
    {
        cout << "Repertoire deja present." << endl;
    }
    savedir();

}

void MdR::deletedir(directory d)
{   vector<directory>::iterator it;
    it = find (dir.begin(), dir.end(), d);
    if ( it==dir.end() )
    {
        cout << "Repertoire non existant." << endl;
    }
    else
    {
        dir.erase(it);
        cout << d.getpath() << " a ete supprime." << endl;
    }
    savedir();

}

vector<directory> MdR::getdir()
{
    return dir;

}

void MdR::loaddir()
{   vector<directory> d;
    dir=d;
    ifstream file(filedir.c_str());
    string word;
    if (file.is_open())
    {
        string line;
        while (getline(file, line))
        {
            directory d(line);
            dir.push_back(d);
        }
        file.close();


}}
void MdR::indexer()
{
    int n=dir.size();
    int i;
    for (i=0;i<n;i++){

        cout << "Indexation dans " << dir[i].getpath() << endl;
        vector<fichier> liste=dir[i].getfiles();
        int j;
        int m=liste.size();
        for (j=0;j<m;j++){
            cout << j << endl;
            I.indexer(liste[j]);
        }
    }
    I.saveindex();





};

void MdR::dirreset(){ofstream file;
    file.open(filedir.c_str());
    file.close();};
/*
vector<pair <string,int> > MdR::rechercher(string str){
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














}; */










