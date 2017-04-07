/**********************************************************************
		        Joint Sentiment-Topic (JST) Model
***********************************************************************

(C) Copyright 2013, Chenghua Lin and Yulan He

Written by: Chenghua Lin, University of Aberdeen, chenghua.lin@abdn.ac.uk.
Part of code is from http://gibbslda.sourceforge.net/.

This file is part of JST implementation.

JST is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free
Software Foundation; either version 2 of the License, or (at your
option) any later version.

JST is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
USA

***********************************************************************/

#include <stdio.h>
#include <string>
#include <map>
#include <iostream>
#include <sstream>
#include "strtokenizer.h"
#include "utils.h"
#include "dataset.h"
#include <sys/types.h>
#include <sys/stat.h>

using namespace std;

#undef WINDOWS
#ifdef _WIN32
    #define WINDOWS
#endif
#ifdef __WIN32__
    #define WINDOWS
#endif

#ifdef WINDOWS
	#include <direct.h>  // For _mkdir().
	#include <io.h>      // For access().
#else
	#include <unistd.h>  // For access().
#endif


utils::utils() {

}

string utils::generate_model_name(int iter, string model_name = "model")  {

	char buff[BUFF_SIZE_SHORT];

	sprintf(buff, "%05d", iter);

	if (iter >= 0)
		model_name += buff;

	return model_name;
}


#ifdef WINDOWS
int utils::make_dir(string strPath) {
	if(_access(strPath.c_str(), 0) == 0)
		return 0;
	else if(_mkdir(strPath.c_str()) == 0)
		return 0;
	else {
		printf("Throw exception in creating directory %s !\n",strPath.c_str());
		return 1;
	}
}
#else

int utils::make_dir(string strPath) {
	if(access(strPath.c_str(), 0) == 0)
		return 0;
	else if(mkdir(strPath.c_str(),  S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH) == 0)
		return 0;
	else {
		cout<<"Throw exception in creating directory "<<strPath.c_str()<<endl;
		return 1;
	}
}
#endif

void utils::quicksort(vector<pair<int, double> > & vect, int left, int right) {
    int l_hold, r_hold;
    pair<int, double> pivot;

    l_hold = left;
    r_hold = right;
    int pivotidx = left;
    pivot = vect[pivotidx];

    while (left < right) {
	while (vect[right].second <= pivot.second && left < right) {
	    right--;
	}
	if (left != right) {
	    vect[left] = vect[right];
	    left++;
	}
	while (vect[left].second >= pivot.second && left < right) {
	    left++;
	}
	if (left != right) {
	    vect[right] = vect[left];
	    right--;
	}
    }

    vect[left] = pivot;
    pivotidx = left;
    left = l_hold;
    right = r_hold;

    if (left < pivotidx) {
	quicksort(vect, left, pivotidx - 1);
    }
    if (right > pivotidx) {
	quicksort(vect, pivotidx + 1, right);
    }
}






void utils::alloc_space(int* &point,int dim1){

    point = new int[dim1];
    for (int i = 0; i < dim1; i++)
        point[i] = 0;
}


void utils::alloc_space(int** &point,int dim1,int dim2){

    point = new int*[dim1];
    for (int i = 0; i < dim1; i++)
        alloc_space(point[i],dim2);
}

void utils::alloc_space(int*** &point,int dim1,int dim2,int dim3){

    point = new int**[dim1];
    for (int i = 0; i < dim1; i++)
        alloc_space(point[i],dim2,dim3);
}


void utils::alloc_space(int**** &point,int dim1,int dim2,int dim3,int dim4){

    point = new int***[dim1];
    for (int i = 0; i < dim1; i++)
        alloc_space(point[i],dim2,dim3,dim4);
}

void utils::alloc_space(double* &point,int dim1){

    point = new double[dim1];
    for (int i = 0; i < dim1; i++) {
        point[i] = 0.0;
    }
}

void utils::alloc_space(double** &point,int dim1,int dim2){

    point = new double*[dim1];
    for (int i = 0; i < dim1; i++)
        alloc_space(point[i],dim2);
}

void utils::alloc_space(double*** &point,int dim1,int dim2,int dim3){

    point = new double**[dim1];
    for (int i = 0; i < dim1; i++)
        alloc_space(point[i],dim2,dim3);
}

void utils::alloc_space(double**** &point,int dim1,int dim2,int dim3,int dim4){

    point = new double***[dim1];
    for (int i = 0; i < dim1; i++)
        alloc_space(point[i],dim2,dim3,dim4);

}


void utils::release_space(int* &point){

    if (point) delete point;

}


void utils::release_space(int** &point,int dim1){

    if (point) {
         for (int i = 0; i < dim1; i++) {
            release_space(point[i]);
	    }
    }
    delete point;
}


void utils::release_space(int*** &point,int dim1,int dim2){

    if (point) {
         for (int i = 0; i < dim1; i++) {
            release_space(point[i],dim2);
	    }
    }
    delete point;
}


void utils::release_space(int**** &point,int dim1,int dim2,int dim3){

    if (point) {
         for (int i = 0; i < dim1; i++) {
            release_space(point[i],dim2,dim3);
	    }
    }
    delete point;
}



void utils::release_space(double* &point){

    if (point) delete point;

}

void utils::release_space(double** &point,int dim1){

    if (point) {
         for (int i = 0; i < dim1; i++) {
            release_space(point[i]);
	    }
    }
    delete point;
}

void utils::release_space(double*** &point,int dim1,int dim2){

    if (point) {
         for (int i = 0; i < dim1; i++) {
            release_space(point[i],dim2);
	    }
    }
    delete point;
}

void utils::release_space(double**** &point,int dim1,int dim2,int dim3){

    if (point) {
         for (int i = 0; i < dim1; i++) {
            release_space(point[i],dim2,dim3);
	    }
    }
    delete point;
}

