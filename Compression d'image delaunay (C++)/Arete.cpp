#include "Arete.h"

Arete::Arete(const Point &p0, const Point &p1) : p0(p0), p1(p1) {}

bool Arete::operator==(const Arete &rhs) const {
    return (p0 == rhs.p0 &&
            p1 == rhs.p1) || (p0 == rhs.p1 && p1 == rhs.p0);
}

bool Arete::operator!=(const Arete &rhs) const {
    return !(rhs == *this);
}

bool Arete::operator<(const Arete &rhs) const {
    Point min0 = p0, max0 = p1, min1 = rhs.p0, max1 = rhs.p1;
    if (!(min0 < max0)) {
        min0 = p1;
        max0 = p0;
    }
    if (!(min1 < max1)) {
        min1 = rhs.p1;
        max1 = rhs.p0;
    }
    if (min0 < min1)
        return true;
    if (min1 < min0)
        return false;
    return max0 < max1;
}

std::ostream &operator<<(std::ostream &os, const Arete &arete) {
    os << "p0: " << arete.p0 << " p1: " << arete.p1;
    return os;
}
