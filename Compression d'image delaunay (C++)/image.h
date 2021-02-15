#ifndef IMAGE_H_INCLUDED
#define IMAGE_H_INCLUDED
#include <vector>
#include <string>
#include "Point.h"
#include<bits/stdc++.h>

using namespace std;

class image{
    private:
        int n;
        int m;
        vector<vector<int> > pixels;
    public:
        image(string path);
        vector<vector<int> > getpixels();
        vector<int> getdim();
        vector<Point> topoints();






};


#endif // IMAGE_H_INCLUDED
