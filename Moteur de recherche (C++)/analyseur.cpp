#include <iostream>
#include <stdlib.h>
#include <iterator>
#include <algorithm>
#include <string>
#include "analyseur.h"
#include "fichier.h"
#include "lecteur.h"
#include "ana.h"

using namespace std;

analyseur::analyseur(lecteur Lec):ana(Lec){
 cout << "analyseur cree " << endl;
}



map<string,int> analyseur::analyser(fichier file)
{
    map<string,int> detail;
    vector<string> texte=L.readfile(file);
    int n=texte.size();
    int i;
    for(i=0; i<n; i++)
    { string str=texte[i];
      transform(str.begin(), str.end(), str.begin(), ::toupper);


        if (find(stopwords.begin(),stopwords.end(),str)==stopwords.end())
        {
            detail[texte[i]]+=1;

        }
    }
    return detail;


}

int analyseur::occur(vector<string> texte, string mot)
{
    int n=texte.size();
    int i;
    int count=0;
    string strtwo=mot;
    transform(strtwo.begin(), strtwo.end(), strtwo.begin(), ::toupper);
    for (i=0; i<n; i++)
    {
        string strone=texte[i];

        transform(strone.begin(), strone.end(), strone.begin(), ::toupper);

        if (strone==strtwo)
        {
            count=count+1;
        }
    }
    return count;

}




int analyseur::counted(map<string,int> detail, string input)
{
   if ( detail.find(input) == detail.end() ) {
  return 0;
} else {
  return 1;
}


}
