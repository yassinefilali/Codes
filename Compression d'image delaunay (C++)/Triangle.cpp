#include "Triangle.h"

Triangle::Triangle(const Point &p0, const Point &p1, const Point &p2)
        : _p0(p0), _p1(p1), _p2(p2) {
    calculCercle();
}

Triangle::Triangle(const Triangle &tri) : _p0(tri.getP0()), _p1(tri.getP1()), _p2(tri.getP2()) {
    calculCercle();
}

void Triangle::calculCercle() {
    double a, b, cx, cy;
    cx = 0.5 * (det(_p1.norm2(), _p1.y, _p2.norm2(), _p2.y) - det(_p0.norm2(), _p0.y, _p2.norm2(), _p2.y) +
                det(_p0.norm2(), _p0.y, _p1.norm2(), _p1.y));
    cy = 0.5 * (-_p0.norm2() * (_p1.x - _p2.x) + _p1.norm2() * (_p0.x - _p2.x) - _p2.norm2() * (_p0.x - _p1.x));

    a = det(_p1.x, _p1.y, _p2.x, _p2.y) - det(_p0.x, _p0.y, _p2.x, _p2.y) + det(_p0.x, _p0.y, _p1.x, _p1.y);
    b = _p0.norm2() * det(_p1.x, _p1.y, _p2.x, _p2.y) - _p1.norm2() * det(_p0.x, _p0.y, _p2.x, _p2.y) +
        _p2.norm2() * det(_p0.x, _p0.y, _p1.x, _p1.y);

    _centreCercle = Point(cx / a, cy / a);
    _rayonCercle = sqrt(b / a + _centreCercle.norm2());
}

std::ostream &operator<<(std::ostream &os, const Triangle &t) {
    os << "Triangle : " << std::endl;
    os << t._p0 << ", " << t._p1 << ", " << t._p2 << std::endl;
    // os << "Cercle circonscrit : " << t._centreCercle << " rayon : " << t._rayonCercle << std::endl;
    return os;
}

bool Triangle::EstDansCercle(const Point &p) {
    return p.distance(_centreCercle) <= _rayonCercle;
}

const Point &Triangle::getP0() const {
    return _p0;
}

void Triangle::setP0(const Point &p0) {
    _p0 = p0;
    calculCercle();
}

const Point &Triangle::getP1() const {
    return _p1;
}

void Triangle::setP1(const Point &p1) {
    _p1 = p1;
    calculCercle();
}

const Point &Triangle::getP2() const {
    return _p2;
}

void Triangle::setP2(const Point &p2) {
    _p2 = p2;
    calculCercle();
}

bool Triangle::EstDansTriangle(const Point &point) const {


    double alpha, beta, gamma;
    CoordBary(point, &alpha, &beta, &gamma);
    return alpha >= 0 && beta >= 0 && gamma >= 0;

}

double Triangle::Aire() {
    double S;
    S = 0.5 * ((_p1.x - _p0.x) * (_p2.y - _p0.y) - (_p2.x - _p0.x) * (_p1.y - _p0.y));
    if (S < 0)
        return (-S);
    else return (S);
}

bool Triangle::operator==(const Triangle &rhs) const {
    return _p0 == rhs._p0 &&
           _p1 == rhs._p1 &&
           _p2 == rhs._p2;
}

bool Triangle::operator!=(const Triangle &rhs) const {
    return !(rhs == *this);
}

void Triangle::CoordBary(const Point &point, double *alpha, double *beta, double *gamma) const {
    double aire;
    double alp, bet, gam;
    aire = fabs(det(_p1 - _p0, _p2 - _p0));
    alp = det(_p0 - point, _p1 - point) / aire;
    bet = det(_p1 - point, _p2 - point) / aire;
    gam = 1 - alp - bet;

    if (alpha != nullptr) {
        *alpha = alp;
    }
    if (beta != nullptr) {
        *beta = bet;
    }
    if (gamma != nullptr) {
        *gamma = gam;
    }
}
bool Triangle::TriangleTrue(){
    bool ttx=true;
    bool tty=true;
if ((this->getP0().x==this->getP1().x)&&(this->getP0().x==this->getP2().x))
    ttx=false;
if ((this->getP0().y==this->getP1().y)&&(this->getP0().y==this->getP2().y))
    tty=false;
return(tty&&ttx);


}



