#include <iostream>
#include <vector>
#include "image.h"
#include "extracteur.h"
#include "ex2.h"

using namespace std;

ex2::ex2(){
    cout << "choix de la methode naive" << endl;
}

vector<Point> ex2::extractpix(image I, int nombrePoints) {

    cout << "le nombre de pixels significatifs peut etre different a cause de soucis de divisibilite" << endl;
    int compteur=0;
    int compt=0;
    int temp=0;
    vector<Point> pts=I.topoints();
    vector<Point> ex;
    int n=pts.size()/nombrePoints;
    for (int i=0;i<pts.size();i++){
        if (temp%n==0){
            ex.push_back(pts[i]);
            temp=1;
            compt++;
            compteur++;
        }
        else {
            temp++;
            compteur++;
        }
    }

    return ex;
}





