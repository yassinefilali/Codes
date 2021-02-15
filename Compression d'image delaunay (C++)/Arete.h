#ifndef PROJET_ARETE_H
#define PROJET_ARETE_H


#include <ostream>
#include "Point.h"

class Arete {
public:
    Point p0, p1;

    Arete(const Point &p0, const Point &p1);

    bool operator==(const Arete &rhs) const;

    bool operator!=(const Arete &rhs) const;

    bool operator<(const Arete &rhs) const;

    friend std::ostream &operator<<(std::ostream &os, const Arete &arete);
};


struct AreteHash {
    std::hash<double> h1;

    unsigned hashDouble(double d) const {
        unsigned a = (unsigned)d;
        d -= a;
        while(d > 0) {
            a *= 10;
            d *= 10;
            a += (unsigned) d;
            d -= a;
        }
        return a;
    }

    std::size_t operator()(Arete const &a) const noexcept {
        /*unsigned h1 = (unsigned) a.p0.norm2() % 4096;
        unsigned h2 = (unsigned) a.p1.norm2() % 4096;
        return h1 ^ (h2 << 2);*/
        //return 1;

        Point min = a.p0, max = a.p1;
        if(max < min) {
            min = a.p1;
            max = a.p0;
        }
        unsigned hashCode = 0;
        hashCode = (hashCode * 397) ^ h1(min.x);
        hashCode = (hashCode * 397) ^ h1(min.y);
        hashCode = (hashCode * 397) ^ h1(max.x);
        hashCode = (hashCode * 397) ^ h1(max.y);
        return hashCode;
    }
};


#endif //PROJET_ARETE_H
