#include <iostream>
#include <dirent.h>
#include <sys/types.h>
#include "fichier.h"
#include "directory.h"
using namespace std;

directory::directory(string p):path(p){

}
string directory::getpath() const
{
    return path;
}
bool directory::operator==(directory const &a)const{
    return (path==a.getpath());
    }

bool directory::operator!=(directory const &a)const{
    return (path!=a.getpath());
    }









vector<fichier> directory::getfiles()
{

    vector<fichier> liste;
    struct dirent *entry;
    DIR *dir = opendir(path.c_str());

    if (dir == NULL)
    {
        return liste;
    }
    while ((entry = readdir(dir)) != NULL)
    {
        string str=string(path)+'/'+entry->d_name;
        fichier f=fichier(str);
        if (f.extension()=="txt")
        {
            liste.push_back(f);
        }
    }
    closedir(dir);
    return liste;






}
