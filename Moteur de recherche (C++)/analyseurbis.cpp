#include <iostream>
#include <stdlib.h>
#include <iterator>
#include <algorithm>
#include <string>
#include "analyseurbis.h"
#include "fichier.h"
#include "lecteur.h"
#include "ana.h"

using namespace std;

analyseurbis::analyseurbis(lecteur Lec):ana(Lec){
cout << "analyseurbis cree " << endl;
}



map<string,int> analyseurbis::analyser(fichier file)
{
    map<string,int> detail;
    vector<string> texte=L.readfile(file);
    int n=texte.size();
    int i;
    for(i=0; i<n; i++)
    { string str=texte[i];
      transform(str.begin(), str.end(), str.begin(), ::toupper);
      detail[texte[i]]+=1;


    }
    return detail;


}
