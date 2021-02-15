#ifndef MDRTWO_H_INCLUDED
#define MDRTWO_H_INCLUDED
#include "MdR.h"
using namespace std;

class MdRtwo: public MdR{
public:
    vector<pair <string,int> > rechercher(string str);
    MdRtwo(indexeur Ind);



};

#endif // MDRTWO_H_INCLUDED
