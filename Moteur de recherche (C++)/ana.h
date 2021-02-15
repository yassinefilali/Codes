#ifndef ANA_H_INCLUDED
#define ANA_H_INCLUDED
#include <map>
#include "fichier.h"
#include "lecteur.h"
using namespace std;
class ana{
protected:
    lecteur L;
public:
    virtual map<string,int> analyser(fichier f)=0;
    ana(lecteur L);





};

#endif // ANA_H_INCLUDED
