#include <iostream>
#include <stdlib.h>
#include <fstream>
#include "fichier.h"
#include "lecteur.h"

using namespace std;

vector<string> lecteur::readfile(fichier f)
{

    ifstream myReadFile;
    string ch=f.getpath();
    myReadFile.open(ch.c_str());
    string output;
    vector<string> liste;
    if (myReadFile.is_open())
    {
        while (!myReadFile.eof())
        {


            myReadFile >> output;
            liste.push_back(output);


        }
    }
    myReadFile.close();
    return liste;




}
