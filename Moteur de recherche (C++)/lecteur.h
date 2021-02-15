#ifndef LECTEUR_H_INCLUDED
#define LECTEUR_H_INCLUDED
#include <vector>
#include "fichier.h"

using namespace std;


class lecteur{

public:
    vector<string> readfile(fichier f);

};

#endif // LECTEUR_H_INCLUDED
