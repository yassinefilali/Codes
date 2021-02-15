#ifndef ANALYSEUR_H_INCLUDED
#define ANALYSEUR_H_INCLUDED
#include <map>
#include "fichier.h"
#include "lecteur.h"
#include "ana.h"

using namespace std;
class analyseur:public ana{
private:
    vector<string> stopwords=L.readfile(fichier("C:/Users/Yassine/Desktop/Moteur de recherche/stopwords.txt"));
    int occur(vector<string> texte,string mot);
    int counted(map<string,int> detail, string mot);


public:
    analyseur(lecteur L);
    map<string,int> analyser(fichier f);


};


#endif // ANALYSEUR_H_INCLUDED
