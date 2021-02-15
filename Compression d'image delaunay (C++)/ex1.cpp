#include <iostream>
#include <vector>
#include "image.h"
#include "extracteur.h"
#include "ex1.h"

using namespace std;

struct ordering {
    bool operator()(pair<Point, double> const &a, pair<Point, double> const &b) {
        return a.second > b.second;
    }
};
ex1::ex1(){
cout << "choix de la methode utilisant la variation du gradient" << endl; }

vector<Point> ex1::extractpix(image I, int nombrePoints) {

    cout << "les dimensions de l'image " << I.getdim()[0] << "  " << I.getdim()[1] << endl;
    vector<vector<int> > pixel = (I).getpixels();
    vector<pair<Point, double>> pointsGrad; // liste des points et de la norme de leur gradient
    int n = pixel.size();
    int m = pixel[1].size();
    for (int i = 1; i < n - 1; i++) {
        for (int j = 1; j < m - 1; j++) {
            double gradx = (pixel[i + 1][j] - pixel[i - 1][j]) / 2.0;
            double grady = (pixel[i][j + 1] - pixel[i][j - 1]) / 2.0;
            double gradv = (pixel[i + 1][j + 1] - pixel[i - 1][j - 1]) / 2.0;
            double gradw = (pixel[i + 1][j - 1] - pixel[i - 1][j + 1]) / 2.0;
            double norm = sqrt(gradx * gradx + grady * grady + gradv * gradv + gradw * gradw);
            pointsGrad.emplace_back(Point(j, i, pixel[i][j]), norm);

        }
    }


    sort(pointsGrad.begin(), pointsGrad.end(), ordering());

    vector<Point> liste; // liste des points qu'on garde
    liste.reserve(nombrePoints);
    for (int i = 0; i < nombrePoints; i++) {
        liste.push_back(pointsGrad.at(i).first);
    }
    return liste;
}
