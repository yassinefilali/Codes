#include <iostream>
#include <stdlib.h>
#include <fstream>
#include <random>
#include <chrono>
#include "Point.h"
#include "Triangle.h"
#include "Maillage.h"
#include "image.h"
#include "extracteur.h"
#include <windows.h>
#include "Decom.h"
#include "ex1.h"
#include "ex2.h"
#include <vector>
#include<math.h>
using namespace std::chrono;
using namespace std;

void afficheMaillage(const Maillage &maillage) {
    cout << "MAILLAGE : " << endl;
    cout << "Sommets" << endl;
    for (auto point : maillage.getPoints()) {
        cout << point << endl;
    }
    cout << "Triangles" << endl;
    for (auto *triangle : maillage.getTriangles()) {
        cout << *triangle;
    }
}

int main() {
    char wd[256];
    GetCurrentDirectoryA(256, wd);
    string wrkdir=wd;
    system((wrkdir+"/dist/imagematrix/imagematrix.exe").c_str());
    image *img;
    fstream file((wrkdir+"/temp.txt").c_str());
    string path;
    if (file.is_open())
    {
        string line;
        while (getline(file, line))
        {path=line;
        cout << path << endl;}}
    img = new image(path);
    string name=path.substr(path.rfind('\\')+1, path.rfind('.')-path.rfind('\\')-1);
    cout <<"name is " << name << endl;
    vector<int> dim = img->getdim();


    vector<vector<int> > pix = img->getpixels();
    //vector<Point> pixp = img->topoints();
    int n;
    cout << "choisir le mode d'extraction de pixels significatifs" << endl;
    cout << " n=1 : methode utilisant la variation du gradient" << endl;
    cout << " sinon : methode naive" << endl;
    cin >> n;
    extracteur *ex;
    if (n==1){
    ex = new ex1();}
    else {ex=new ex2();}
    cout << "saisir le nombre de points particuliers a considerer" << endl;
    int p;
    cin >> p;

    vector<Point> liste = ex->extractpix((*img), p);

    map<int,map<int,int>> pt;
    int lig, col;

    lig = dim[0];
    col = dim[1];

    cout << "lignes : " << lig << " colonnes : " << col << endl;

    Maillage mail(col, lig);
    cout << "Nombre de points specifiques choisis : " << liste.size() << endl;


cout<< "**************************************"<<endl;
    auto start = high_resolution_clock::now();
    cout << "Construction du maillage ..." << endl;
    mail.ajouterPoints(liste);
    auto stop = high_resolution_clock::now();

    auto duration = duration_cast<microseconds>(stop - start);


    cout << "Fin de l'ajout des points, duree : " << duration.count() / 10E5 << endl;

    cout << "le maillage est compose de " << mail.getTriangles().size() << " triangles " << endl;
    ofstream out("test.mesh");
    mail.meshFormat(out);
    out.close();

    float alpha;
    alpha=(2*(float)liste.size())/((float)(lig*col));

    cout<< "Le facteur de la compression : alpha = "<< alpha<< endl;
    cout<< "**************************************"<<endl;
    cout << "Debut decompression ..." << endl;
    auto start1 = high_resolution_clock::now();
    Decom d(&mail);
    pt = d.decompresser();

    auto stop1 = high_resolution_clock::now();
    auto duration1 = duration_cast<microseconds>(stop1 - start1);
    cout<<"fin de la decompression, duree : "<< duration1.count()/10E5<<endl;
    cout<< "**************************************"<<endl;

//Qualité de l'image compressée
double q=0;
double qc;
double PSNR;
    for (int i=0 ; i<pix.size(); i++){
            for(int j=0; j<pix[i].size() ; j++){
        q=q+abs((pix[i][j]-pt[i][j])*(pix[i][j]-pt[i][j]));
    }}
    qc=q/(lig*col);
    PSNR=10*log10(255*255/qc);
    cout<<"Le rapport singal bruit PSNR est " << PSNR <<endl;
cout<< "**************************************"<<endl;
/////
    cout<<"Votre photo se trouve dans le dossier resultimages "<<endl;
    cout<< "**************************************"<<endl;

    //Déclaration d'un flux permettant d'écrire dans le fichier
    string const nomFichier(wrkdir+"/resultimages/"+name+"_result.txt");
    ofstream monFlux(nomFichier.c_str());
    if (monFlux) {
        monFlux << lig << "-" << col << endl;
        int i = 0;
        while (i < lig) {
            for (int j = 0; j < col; j++) {
                monFlux << pt[j][i] << " ";
            }
            monFlux << endl;
            i = i + 1;
        }
    } else {
        cout << "ERREUR: Impossible d'ouvrir le fichier." << endl;
    }
    system((wrkdir+"/dist/matriximage/matriximage.exe").c_str());

    system("medit-win.exe test.mesh");



    return 0;
}

