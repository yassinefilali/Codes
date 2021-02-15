#ifndef DIRECTORY_H_INCLUDED
#define DIRECTORY_H_INCLUDED
#include <vector>
#include <iostream>
#include <dirent.h>
#include <sys/types.h>
#include "fichier.h"
#include "directory.h"

using namespace std;
class directory{
    private:
        string path;
    public:
        directory(string p);
        string getpath() const;
        vector<fichier> getfiles();
        bool operator==(directory const&a) const;
        bool operator!=(directory const&a) const;





};


#endif // DIRECTORY_H_INCLUDED
