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

#ifndef _UTILS_H
#define _UTILS_H

#include "dataset.h"
#include "constants.h"
#include <string>
#include <algorithm>
using namespace std;


// for sorting word probabilitys
struct sort_pred {
    bool operator()(const std::pair<int,double> &left, const std::pair<int,double> &right) {
	    return left.second > right.second;
    }
};

class utils {
private:

    Model_Para model_para;

public:

	utils();

    static string generate_model_name(int iter, string model_name);

    // make directory
    static int make_dir(string strPath);

    // sort
    static void sort(vector<double> & probs, vector<int> & words);
    static void quicksort(vector<pair<int, double> > & vect, int left, int right);

    static void alloc_space(int* &point,int dim1);
    static void alloc_space(int** &point,int dim1,int dim2);
    static void alloc_space(int*** &point,int dim1,int dim2,int dim3);
    static void alloc_space(int**** &point,int dim1,int dim2,int dim3,int dim4);
    static void alloc_space(double* &point,int dim1);
    static void alloc_space(double** &point,int dim1,int dim2);
    static void alloc_space(double*** &point,int dim1,int dim2,int dim3);
    static void alloc_space(double**** &point,int dim1,int dim2,int dim3,int dim4);

    static void release_space(int* &point);
    static void release_space(int** &point,int dim1);
    static void release_space(int*** &point,int dim1,int dim2);
    static void release_space(int**** &point,int dim1,int dim2,int dim3);
    static void release_space(double* &point);
    static void release_space(double** &point,int dim1);
    static void release_space(double*** &point,int dim1,int dim2);
    static void release_space(double**** &point,int dim1,int dim2,int dim3);


};

#endif

