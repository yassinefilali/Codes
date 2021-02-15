#ifndef INDEXEUR_H_INCLUDED
#define INDEXEUR_H_INCLUDED
#include "lecteur.h"
#include "fichier.h"
#include "analyseur.h"
#include <map>
using namespace std;

class indexeur{
    private:
        ana *A;
        map<string,map<string,int> > index;
        string indextxt="C:/Users/Yassine/Desktop/Moteur de recherche/index.txt";
        int counted(string input);



    public:
        indexeur(ana *Ana);
        void indexer(fichier f);
        void indexreset();
        map<string,map<string,int> > getindex();
        void loadindex();
        void saveindex();
        string getindextxt();








};

#endif // INDEXEUR_H_INCLUDED
