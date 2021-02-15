#include <iostream>
#include <stdlib.h>
#include <fstream>
#include <sstream>
#include "fichier.h"
#include "indexeur.h"
#include "lecteur.h"
#include "analyseur.h"
#include <iterator>
#include <algorithm>
#include <string>



int indexeur::counted(string input)
{
    if ( index.find(input) == index.end() )
    {
        return 0;
    }
    else
    {
        return 1;
    }
    /*map<string,map<string,int> >::iterator itr;
    string strtwo=input;
    transform(strtwo.begin(), strtwo.end(), strtwo.begin(), ::toupper);
    for (itr=index.begin(); itr != index.end(); ++itr)
    {
        string strone=itr->first;

        transform(strone.begin(), strone.end(), strone.begin(), ::toupper);
        if (strone==strtwo)
        {
            return 1;
        }
    }
    return 0; */
}

void indexeur::indexreset()
{
    ofstream file;
    file.open(indextxt.c_str());
    file.close();





};

void indexeur::loadindex()
{
    ifstream file(indextxt.c_str());
    string word;
    if (file.is_open())
    {
        string line;
        while (getline(file, line))
        {
            if (line.find('--') == string::npos)
            {
                word = line;
            }
            else
            {
                int n=line.find('--');
                string file=line.substr(0,n);

                string p=string(line.substr(n+2,line.size()));
                stringstream steam(p);
                int occur=0;
                steam >> occur;
                index[word].insert(pair<string,int>(file,occur));

            }
        }
        file.close();









    }
}

void indexeur::saveindex()
{
    ofstream f;
    f.open(indextxt.c_str());
    if (f.is_open()){
    map<string,map<string,int> >::iterator itr;
    for (itr=index.begin(); itr != index.end(); ++itr)
    {
        string mot=itr->first;
        f << mot << endl;
        map<string,int> desc=itr->second;
        map<string,int>::iterator i;
        for (i=desc.begin(); i != desc.end(); ++i)
        {
            string fichier=i->first;
            int occur=i->second;
            f << fichier << "--" << occur << endl;
        }

    }
    f.close();
    }




}
indexeur::indexeur(ana *Ana):A(Ana){};



void indexeur::indexer(fichier f)
{
    map<string,int> detail=A->analyser(f);
    map<string,int>::iterator itr;
    for (itr=detail.begin(); itr != detail.end(); ++itr)
    {
        string mot=itr->first;
        int occur=itr->second;
        transform(mot.begin(), mot.end(), mot.begin(), ::toupper);
       /* if (counted(mot)==0)
        {
            map<string,int> g;
            g.insert(pair<string,int>(f.getpath(),occur));
            index.insert(pair<string,map<string,int> >(mot,g));
        }
        else
        {
            index[mot].insert(pair <string,int>(f.getpath(),occur));
        }*/
        index[mot][f.getpath()]=occur;



    }




}

map<string,map<string,int> > indexeur::getindex()
{
    return index;

};
string indexeur::getindextxt()
{
    return indextxt;


}

