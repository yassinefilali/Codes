#ifndef ANALYSEURBIS_H_INCLUDED
#define ANALYSEURBIS_H_INCLUDED

#include <map>
#include "fichier.h"
#include "lecteur.h"
#include "ana.h"

using namespace std;
class analyseurbis:public ana{
private:
    lecteur L;



public:
    analyseurbis(lecteur L);
    map<string,int> analyser(fichier f);


};

#endif // ANALYSEURBIS_H_INCLUDED
