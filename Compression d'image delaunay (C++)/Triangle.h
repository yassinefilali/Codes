#ifndef PROJET_TRIANGLE_H
#define PROJET_TRIANGLE_H

#include "Point.h"

class Triangle {
private:
    /**
     * Sommets du triangle
     */
    Point _p0, _p1, _p2;

    /**
     * Centre et rayon du cercle circonscrit au triangle
     */
    Point _centreCercle;
    double _rayonCercle;

    /**
     * Calcule centre et rayon du cercle circonscrit au triangle
     */
    void calculCercle();

public:
    Triangle(const Point &p0, const Point &p1, const Point &p2);

    Triangle(const Triangle &tri);

    void CoordBary(const Point &point, double *alpha, double *beta, double *gamma) const;

    bool EstDansCercle(const Point &p);

    const Point &getP0() const;

    void setP0(const Point &p0);

    const Point &getP1() const;

    void setP1(const Point &p1);

    const Point &getP2() const;

    void setP2(const Point &p2);

    bool operator==(const Triangle &rhs) const;

    bool operator!=(const Triangle &rhs) const;

    double Aire();

    friend std::ostream &operator<<(std::ostream &os, const Triangle &t);

    bool EstDansTriangle(const Point &point) const;
    bool TriangleTrue();



}

;


#endif //PROJET_TRIANGLE_H
