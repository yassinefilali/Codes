#include"Vecteur.h"

Vecteur::Vecteur() : vx(0), vy(0) {}

Vecteur::Vecteur(const Point &p1, const Point &p2) {
    vx = p2.x - p1.x;
    vy = p2.y - p1.y;

}

double Vecteur::ProduitScalaire(const Vecteur &V1) {
    double s;
    s = V1.vx * this->vx + V1.vy * this->vy;
    return (s);
}

