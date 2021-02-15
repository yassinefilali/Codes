#include "Point.h"

Point::Point() : x(0), y(0), val(0) {}

Point::Point(double x, double y, double val) : x(x), y(y), val(val) {}

Point::Point(const Point &p) : x(p.x), y(p.y), val(p.val) {}

//distance au carré
double Point::distance2(const Point &p) const {
    double dx = this->x - p.x;
    double dy = this->y - p.y;
    return dx * dx + dy * dy;
}

double Point::distance(const Point &p) const {
    return sqrt(distance2(p));
}
//norme au carré
double Point::norm2() const {
    return x * x + y * y;
}

double Point::norm() const {
    return sqrt(norm2());
}
//surcharge des opérateurs
bool Point::operator==(const Point &p) const {
    return this->x == p.x && this->y == p.y;
}

bool Point::operator!=(const Point &p) const {
    return !(*this == p);
}

bool Point::operator<(const Point &rhs) const {
    if (x < rhs.x)
        return true;
    if (rhs.x < x)
        return false;
    return y < rhs.y;
}

Point &Point::operator+=(const Point &p) {
    this->x += p.x;
    this->y += p.y;
    return *this;
}

Point &Point::operator-=(const Point &p) {
    *this += (-p);
    return *this;
}

Point Point::operator-() const {
    return Point(-x, -y);
}

Point &Point::operator*=(double a) {
    this->x *= a;
    this->y *= a;
    return *this;
}

Point Point::operator*(double a) const {
    Point point(*this);
    point *= a;
    return point;
}


std::ostream &operator<<(std::ostream &os, const Point &p) {
    os << "Point(x=" << p.x << ", y=" << p.y << ")";
    return os;
}
//determinant
double det(double a, double b, double c, double d) {
    return a * d - b * c;
}

double det(const Point &p1, const Point &p2) {
    return det(p1.x, p2.x, p1.y, p2.y);
}
//surcharge des ppérateurs
Point operator+(const Point &p1, const Point &p2) {
    Point point(p1);
    point += p2;
    return point;
}

Point operator-(const Point &p1, const Point &p2) {
    Point point(p1);
    point -= p2;
    return point;
}

Point operator*(double a, const Point &p) {
    return p * a;
}


