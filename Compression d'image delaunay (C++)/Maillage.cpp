#include <queue>
#include <random>
#include <ctime>
#include "Maillage.h"
#include "Arete.h"
#include "Vecteur.h"

using namespace std;

Maillage::Maillage(double largeur, double hauteur) : _largeur(largeur), _hauteur(hauteur) {
    srand(time(0));

    // On ajoute les coins au maillage
    Point hg(0, 0), hd(_largeur, 0), bg(0, _hauteur), bd(_largeur, _hauteur);

    _points.push_back(hg);
    _points.push_back(hd);
    _points.push_back(bg);
    _points.push_back(bd);

    // On ajoute 2 triangles rectangle
    _ajouterTriangle(new Triangle(hg, hd, bg));
    _ajouterTriangle(new Triangle(hd, bd, bg));
}

Maillage::Maillage(const Maillage &m) {
    srand(time(0));

    this->_hauteur = m._hauteur;
    this->_largeur = m._largeur;
    this->_points = m._points;
    for (Triangle *tri:m.getTriangles()) {
        this->_triangles.insert(new Triangle(*tri));
    }
}

void Maillage::_ajouterTriangle(Triangle *triangle) {
     if (triangle->TriangleTrue()) {

    _triangles.insert(triangle);
    _ajouterVoisin(triangle, Arete(triangle->getP0(), triangle->getP1()));
    _ajouterVoisin(triangle, Arete(triangle->getP1(), triangle->getP2()));
    _ajouterVoisin(triangle, Arete(triangle->getP2(), triangle->getP0()));
     }
}

void Maillage::_ajouterVoisin(Triangle *triangle, const Arete &arete) {
    auto it = _voisins.find(arete);
    if (it != _voisins.end()) {
        vector<Triangle *> &voisinsArete = it->second;
        voisinsArete.push_back(triangle);
    } else {
        vector<Triangle *> voisinsArete;
        voisinsArete.push_back(triangle);
        _voisins.insert(make_pair(arete, voisinsArete));
    }
}

void Maillage::_retirerVoisin(Triangle *triangle, const Arete &arete) {
    auto it = _voisins.find(arete);
    if (it != _voisins.end()) {
        vector<Triangle *> &voisinsArete = it->second;
        for (int i = 0; i < voisinsArete.size(); i++) {
            if (voisinsArete.at(i) == triangle) {
                voisinsArete.erase(voisinsArete.begin() + i);
                return;
            }
        }
    } else {
        cout << "Erreur : arete non répertoriée" << endl;
    }
}

void Maillage::_retirerTriangle(Triangle *triangle) {
    _retirerVoisin(triangle, Arete(triangle->getP0(), triangle->getP1()));
    _retirerVoisin(triangle, Arete(triangle->getP1(), triangle->getP2()));
    _retirerVoisin(triangle, Arete(triangle->getP2(), triangle->getP0()));
    _triangles.erase(_triangles.find(triangle));
    delete triangle;
}

Triangle *Maillage::_trouverVoisin(Triangle *triangle, const Arete &arete) const {
    auto it = _voisins.find(arete);
    if (it != _voisins.end()) {
        const vector<Triangle *> &voisinsArete = it->second;
        for (Triangle *vois : voisinsArete) {
            if (vois != triangle) {
                return vois;
            }
        }
    }
    return nullptr;
}

vector<pair<Arete, Triangle *>> Maillage::_trouverVoisins(Triangle *triangle) const {
    vector<pair<Arete, Triangle *>> voisTriangle;

    Arete arete(triangle->getP0(), triangle->getP1());
    Triangle *vois = _trouverVoisin(triangle, arete);
    voisTriangle.emplace_back(arete, vois);

    arete = Arete(triangle->getP1(), triangle->getP2());
    vois = _trouverVoisin(triangle, arete);
    voisTriangle.emplace_back(arete, vois);

    arete = Arete(triangle->getP2(), triangle->getP0());
    vois = _trouverVoisin(triangle, arete);
    voisTriangle.emplace_back(arete, vois);

    return voisTriangle;
}

void Maillage::ajouterPoint(const Point &point) {
    if(point.x < 0 || point.x > _largeur || point.y < 0 || point.y > _hauteur) {
        cout << "Erreur point invalide " << point << endl;
    }
    _points.push_back(point); // on ajoute le point au maillage

    // Déterminer les triangles à retirer
    unordered_set<Triangle *> aRetirer;
    unordered_set<Triangle *> traites;
    queue<Triangle *> queue; // queue pour BFS
    Triangle *triangle = triangleContenant(point);
    aRetirer.insert(triangle);
    traites.insert(triangle);
    queue.push(triangle);
    while (!queue.empty()) {
        triangle = queue.front();
        queue.pop();
        auto voisTriangle = _trouverVoisins(triangle);
        for (const pair<Arete, Triangle *> &v: voisTriangle) {
            const Arete &arete = v.first;
            Triangle *voisin = v.second;
            if (voisin != nullptr && traites.find(voisin) ==
                                     traites.end()) { // si le voisin n'a pas encore été traité
                traites.insert(voisin);
                if (voisin->EstDansCercle(point)) {
                    aRetirer.insert(voisin);
                    queue.push(voisin);
                }
            }
        }
    }
/*    for (auto *triangle : _triangles) {
        if (triangle->EstDansCercle(point)) {
            aRetirer.insert(triangle);
        }
    }*/
    // Déterminer la forme du trou polygonal
    vector<Arete> aretesPoly; // arêtes du polygone
    for (auto *t1 : aRetirer) {
        //cout << "Triangle a retirer " << endl;
        //cout << *t1;
        auto voisTriangle = _trouverVoisins(t1);
        for (const pair<Arete, Triangle *> &v: voisTriangle) {
            const Arete &arete = v.first;
            Triangle *voisin = v.second;
            //cout << "\tVoisin " << v.second << " par l'arete " << v.first << endl;
            if (aRetirer.find(voisin) ==
                aRetirer.end()) { // si le voisin n'est pas dans aRetirer
                aretesPoly.push_back(arete);
            }
        }
    }

    // cout << "Ajout des nouveaux triangles" << endl;
    // Créer les nouveaux triangles
    for (const auto &arete : aretesPoly) {
        auto *nouvTriangle = new Triangle(arete.p0, arete.p1, point);
        _ajouterTriangle(nouvTriangle);
        // cout << "\t" << *nouvTriangle;
    }

    // cout << "Retrait des triangles" << endl;
    for (auto *mauvaisTriangle : aRetirer) {
        // cout << "\t" << *mauvaisTriangle;
        _retirerTriangle(mauvaisTriangle);
    }
}

Triangle *Maillage::triangleContenant(const Point &point) const {
    Triangle *triangle = *_triangles.begin(); // on choisit arbitrairement un triangle

    while (!triangle->EstDansTriangle(point)) {

        double coords[3];
        triangle->CoordBary(point, coords, coords + 1, coords + 2);
        // on compte le nombre de coord négatives
        int nbCoordNeg = 0;

        //vector<pair<Arete, Triangle *>> voisins = _trouverVoisins(triangle);
        Triangle *voisins[3]{nullptr, nullptr, nullptr};
        Arete aretes[3]{Arete(triangle->getP0(), triangle->getP1()), Arete(triangle->getP1(), triangle->getP2()),
                        Arete(triangle->getP2(), triangle->getP0())};
        for (int i = 0; i < 3; i++) {
            voisins[i] = _trouverVoisin(triangle, aretes[i]);
            if (voisins[i] != nullptr && coords[i] < 0) {
                nbCoordNeg++;
            }
        }

        if(nbCoordNeg == 0) {
            cout << "Erreur triangleContenant : on ne peut plus avancer !" << endl;
            cout << *triangle << endl;
            return nullptr;
        }

        int indiceArete; // on cherche l'indice de l'arête à traverser
        int rnd = rand() % nbCoordNeg; // au hasard parmi les arêtes qui donnent coord negative
        for (int i = 0, j = 0; i < 3; i++) {
            if (coords[i] < 0) {
                if (j == rnd) {
                    indiceArete = i;
                    break;
                }
                j++;
            }
        }
        triangle = voisins[indiceArete];

    }
    return triangle;
}

Maillage::~Maillage() {
    for (auto *triangle : _triangles) {
        delete triangle;
    }
}

void Maillage::ajouterPoints(const vector<Point> &points) {
    for (const auto &point : points) {
        ajouterPoint(point);
    }
}

const vector<Point> &Maillage::getPoints() const {
    return _points;
}

const unordered_set<Triangle *> &Maillage::getTriangles() const {
    return _triangles;
}

double Maillage::getLargeur() const {
    return _largeur;
}

double Maillage::getHauteur() const {
    return _hauteur;
}

void Maillage::meshFormat(ostream &os) const {
    os << "MeshVersionFormatted 1\n"
          "Dimension 2" << endl;

    map<Point, int> pointsIndices;
    os << "Vertices" << endl;
    os << _points.size() << endl;
    for (int i = 1; i <= _points.size(); i++) {
        const Point &point = _points.at(i-1);
        os << point.x << " " << point.y << " " << "0" << endl;
        pointsIndices.insert(make_pair(point, i));
    }

    os << endl;
    os << "Triangles" << endl;
    os << _triangles.size() << endl;
    for (const auto &triangle : _triangles) {
        os << pointsIndices.at(triangle->getP0()) << " " << pointsIndices.at(triangle->getP1()) << " "
           << pointsIndices.at(triangle->getP2()) << " 0" << endl;
    }
    os << endl;

    os << "End" << endl;
}



















