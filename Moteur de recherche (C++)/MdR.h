#ifndef MDR_H_INCLUDED
#define MDR_H_INCLUDED

using namespace std;

class MdR {
protected:
    vector<directory> dir;
    string filedir="C:/Users/Yassine/Desktop/Moteur de recherche/filedir.txt";
    indexeur I;
public:
    MdR(indexeur Ind);
    void adddir(directory d);
    void deletedir(directory d);
    virtual vector<pair <string,int> > rechercher(string recherche)=0;
    vector<directory> getdir();
    void loaddir();
    void savedir();
    void indexer();
    void dirreset();
    indexeur getindex();

};

#endif // MDR_H_INCLUDED
