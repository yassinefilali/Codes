#ifndef PROJET_POINT_H
#define PROJET_POINT_H

#include <iostream>
#include <cmath>

class Point {
public:
    double x, y;
    double val;

    Point();

    Point(double x, double y, double val = 0);

    Point(const Point &p);

    /**
     * Distance euclidienne au carrée
     * @param p
     * @return
     */
    double distance2(const Point &p) const;

    /**
     * Distance euclidienne
     * @param p
     * @return
     */
    double distance(const Point &p) const;

    /**
     * Norme euclidienne au carré
     */
    double norm2() const;

    /**
     * Norme euclidienne
     */
    double norm() const;

    Point &operator+=(const Point &p);

    Point &operator-=(const Point &p);

    Point &operator*=(double a);

    Point operator*(double a) const;

    Point operator-() const;

    bool operator==(const Point &p) const;

    bool operator!=(const Point &p) const;

    bool operator<(const Point &rhs) const;

};

/**
 * Calcule un déterminant 2x2
 */
double det(double a, double b, double c, double d);

double det(const Point &p1, const Point &p2);

Point operator+(const Point&p1, const Point&p2);
Point operator-(const Point&p1, const Point&p2);
Point operator*(double a, const Point& p);

std::ostream &operator<<(std::ostream &os, const Point &p);


#endif //PROJET_POINT_H
