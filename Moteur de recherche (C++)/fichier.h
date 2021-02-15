#ifndef FICHIER_H_INCLUDED
#define FICHIER_H_INCLUDED

using namespace std;

class fichier{
private:
    string path;
public:
    fichier(string path);
    string getpath() const;
    string extension();
    bool operator==(fichier const&a) const;
    bool operator!=(fichier const&a) const;
    bool operator<(fichier const &a)const;





};



#endif // FICHIER_H_INCLUDED
