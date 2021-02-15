#ifndef VECTEUR_H
#define VECTEUR_H

#include "Point.h"


class Vecteur {
private :
    double vx;
    double vy;

public :
    Vecteur();
    Vecteur (const Point &p1, const Point &p2);
    double ProduitScalaire(const Vecteur &V1);

    };
#endif // VECTEUR_H
