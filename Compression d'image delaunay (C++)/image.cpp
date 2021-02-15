#include <iostream>
#include <stdlib.h>
#include <fstream>
#include <sstream>
#include "image.h"

using namespace std;

vector<int> image::getdim()
{
    vector<int> v;
    v.push_back(n);
    v.push_back(m);
    return v;
}

vector<vector<int> > image::getpixels()
{
    return pixels;
}

image::image(string path)
{
    vector<int> v;
    vector<vector<int> > vv;
    ifstream file(path.c_str());
    if (file.is_open())
    {
        string line;
        while (getline(file, line))
        {
            if (line.find('-') != string::npos)
            {
                string dimn=line.substr(0,line.find('-'));
                string dimm=string(line.substr(line.find('-')+1,line.size()));
                stringstream steam(dimm);
                int i=0;
                steam >> i;
                stringstream stm(dimn);
                int j=0;
                stm >> j;
                n=j;
                m=i;

            }
            else
            {

                v.clear();
                int p=line.size();
                int k;
                string temp="";
                for (k=0; k<p; k++)
                {
                    if (line[k]==' ')
                    {
                        int inter=std::atoi(temp.c_str());
                        v.push_back(inter);

                        temp="";
                    }
                    else
                    {
                        temp=temp+line[k];
                    }




                }

                vv.push_back(v);


            }
        }
    }

    pixels=vv;


    file.close();
}


vector<Point> image::topoints(){;
   vector<Point> pix;
   vector<vector<int> > vv=pixels;
    int lign = vv.size();
    int col = vv[1].size();
    int sr;
    for(sr=1;sr<lign+1;sr++){
        int in;

        for(in=1;in<col+1;in++){
            Point pnt(in,sr,vv[sr-1][in-1]);
            pix.push_back(pnt);
        }
    }
    return pix;
}









