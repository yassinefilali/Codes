#include "Decom.h"
#include<algorithm>
#include <iostream>
#include <fstream>

using std::vector;
using std::min;
using std::max;
using namespace std;

Decom::Decom(Maillage *m1) : m(m1) {}


map<int,map<int,int>> Decom::decompresser() {


    vector<Point> pt;

    double mx, my, mxx, myy;



map<int,map<int,int>> matrice;

//méthode naive

  /*  for (int y = 0; y < (int)m->getHauteur(); y++) {
        for (int x = 0; x < (int)m->getLargeur(); x++) {
            Point pp(x, y);
            Triangle *triangle = m->triangleContenant(pp);
            if(triangle == nullptr) {
                cout << "nullptr pour le point " << pp << endl;
            }
            double alpha, beta, gamma;
            triangle->CoordBary(pp, &alpha, &beta, &gamma);
            matrice[y][x]=beta * triangle->getP0().val + gamma * triangle->getP1().val +alpha * triangle->getP2().val;
            cout<<x<<","<<y<<":"<<matrice[x][y]<<endl;*/
//méthode rapide
for (Triangle *tri: m->getTriangles()) {
        mx=min(min(tri->getP0().x,tri->getP1().x),min(tri->getP1().x, tri->getP2().x));
        mxx=max(max(tri->getP0().x,tri->getP1().x),max(tri->getP1().x, tri->getP2().x));
        my=min(min(tri->getP0().y, tri->getP1().y), min(tri->getP1().y,tri->getP2().y));
        myy=max(max(tri->getP0().y, tri->getP1().y), max(tri->getP1().y,tri->getP2().y));

 for (double a=mx ; a<=mxx ; a++){
            for(double b=my; b<=myy; b++){

                Point pp(a,b);
                if (tri->EstDansTriangle(pp)){
                    double alpha, beta, gamma;
                    tri->CoordBary(pp, &alpha, &beta, &gamma);
                    matrice[a][b]=(beta * tri->getP0().val + gamma * tri->getP1().val +alpha * tri->getP2().val);}}}





        }




    return matrice;
}

