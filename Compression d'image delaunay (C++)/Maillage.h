#ifndef PROJET_MAILLAGE_H
#define PROJET_MAILLAGE_H


#include <vector>
#include <array>
#include <algorithm>
#include <set>
#include <map>
#include <unordered_map>
#include <unordered_set>
#include "Point.h"
#include "Triangle.h"
#include "Arete.h"

// TODO test avec map <Arete*, vector<Triangle*>>

class Maillage {
private:
    std::vector<Point> _points;
    std::unordered_set<Triangle *> _triangles;
    std::unordered_map<Arete, std::vector<Triangle *>, AreteHash> _voisins;

    double _largeur;
    double _hauteur;

    void _ajouterTriangle(Triangle *triangle);

    void _retirerTriangle(Triangle *triangle);

    void _ajouterVoisin(Triangle *triangle, const Arete &arete);

    void _retirerVoisin(Triangle *triangle, const Arete &arete);

    std::vector<std::pair<Arete, Triangle *>> _trouverVoisins(Triangle *triangle) const;

    Triangle *_trouverVoisin(Triangle *triangle, const Arete &arete) const;
public:
    Maillage(double largeur, double hauteur);

    Maillage(const Maillage &m);

    void ajouterPoint(const Point &point);

    void ajouterPoints(const std::vector<Point> &points);

    /**
     * à tester et utiliser pourr maillage plus rapide
     */
    Triangle *triangleContenant(const Point &point) const;

    const std::vector<Point> &getPoints() const;

    const std::unordered_set<Triangle *> &getTriangles() const;

    double getLargeur() const;

    double getHauteur() const;

    /**
     * Écrit le maillage en format MESH sur l'output stream os (permet de visualiser le maillage avec Medit)
     */
    void meshFormat(std::ostream &os) const;

    virtual ~Maillage();
};


#endif //PROJET_MAILLAGE_H