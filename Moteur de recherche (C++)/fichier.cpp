#include <iostream>
#include <stdlib.h>
#include <dirent.h>
#include <sys/types.h>
#include "fichier.h"



using namespace std;
string fichier::getpath() const{
    return path;
}
bool fichier::operator==(fichier const &a)const{
    return (path==a.getpath());
    }

bool fichier::operator!=(fichier const &a)const{
    return (path!=a.getpath());
    }
bool fichier::operator<(fichier const &a)const{
    return (path<a.getpath());
    }

fichier::fichier(string p):path(p){}



string fichier::extension(){
    string x="";
    int i=path.rfind('.')+1;
    int n=path.size();
    for (i;i<n;i++){
        x=x+path[i];
    }
    return x;
}
