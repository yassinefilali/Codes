#ifndef EXTRACTEUR_H_INCLUDED
#define EXTRACTEUR_H_INCLUDED
#include "Point.h"

class extracteur{
public:
    virtual vector<Point > extractpix(image I,int nombrePoints)=0;





};


#endif // EXTRACTEUR_H_INCLUDED
