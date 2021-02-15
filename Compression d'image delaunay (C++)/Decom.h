#ifndef DECOM_H
#define DECOM_H
#include <iostream>
#include <fstream>
#include "Point.h"
#include "Triangle.h"
#include"Maillage.h"
#include<map>
using std::vector;
using std::map;

class Decom {
private :
    Maillage *m;
public :
    Decom (Maillage *m1);

    map<int,map<int,int> > decompresser();
};
#endif // DECOM_H
