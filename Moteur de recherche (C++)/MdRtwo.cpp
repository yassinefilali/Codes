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
#include "MdRtwo.h"
#include <iterator>
#include <algorithm>
#include <string>
#include <vector>
#include<bits/stdc++.h>


using namespace std;

bool sortbyse(const pair<string,int> &a,
              const pair<string,int> &b)
{
    return (a.second > b.second);
}


vector<pair <string,int> > MdRtwo::rechercher(string str){
    I.loadindex();
   string recherche=str;
   transform(recherche.begin(), recherche.end(), recherche.begin(), ::toupper);
   map<string,int> classement;
   vector<pair <string,int> > classing;
   vector<string> mots;
   int n=recherche.size();
   cout << n << endl;
   int i;
   string temp="";
   for (i=0;i<n;i++){
        if(recherche[i]==' '){
            mots.push_back(temp);
            temp="";
        }
        else if (i==n-1) {
            temp=temp+recherche[i];

        mots.push_back(temp);}
        else {temp=temp+recherche[i];
        }

   }
   n=mots.size();

   for (i=0;i<n;i++){
   ifstream file("C:/Users/Yassine/Desktop/Moteur de recherche/index.txt");

   string word=mots[i];
   if (file.is_open())
    {
        string line;
        int t=0;
        while (getline(file, line))
        {
            if ((line.find(word)!=string::npos)&&(line.find('/')==string::npos))
            {
                t=1;
           }
            else if ((line.find('/') == string::npos)&&(line.find(word)==string::npos)){t=0;}
            else if ((t==1)){

                    int n=line.find('--');
                    string file=line.substr(0,n);
                    string p=string(line.substr(n+2,line.size()));
                    stringstream steam(p);
                    int occur=0;


                    steam >> occur;

                    classement[file]=classement[file]+occur; }

            else {}

                }
            }


        file.close(); }
        map<string,int>::iterator it;
        for (it=classement.begin(); it != classement.end(); ++it)
        {
            string f=it->first;
            int occ=it->second;
            classing.push_back( make_pair(f,occ) );

        }
        sort(classing.begin(), classing.end(), sortbyse);
        return classing;

};
MdRtwo::MdRtwo(indexeur Ind):MdR(Ind) {cout << "moteur de recherche 2 cree" << endl;}
