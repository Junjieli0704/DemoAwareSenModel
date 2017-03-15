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


#ifndef	_MODEL_H
#define	_MODEL_H

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <sys/stat.h>
#include <math.h>
#include <fstream>
#include <sstream>
#include <iostream>
#include <vector>

#include "dataset.h"
#include "map_type.h"
#include "utils.h"
#include "strtokenizer.h"
#include "constants.h"
#include "sentiLex.h"
#include "log.h"

using namespace std;


class JST_model {

public:
	JST_model(void);
	~JST_model(void);

	//mapword2prior sentiLex; // <word, [senti lab, word prior distribution]>
	sentiLex senLex;
    mapid2word id2word; // word map [int => string]

	string dir;
	string data_file;
	string senti_lex_file;
	string wordmapfile;

	string tassign_suffix;
	string pi_suffix;
	string theta_suffix;
	string phi_suffix;
	string others_suffix;
	string twords_suffix;
	string save_model_name;

	int numTopics;
	int numSentiLabs;
	int niters;
	int twords;
	double _alpha;
	double _beta;
	double _gamma;

	// init functions
    int init_para(Model_Para* model_para);
	int excute_model(Model_Para* model_para);

    void set_log_file(LogFile* logFile){
        this->logFile = logFile;
    }


private:

	int numDocs;
	int vocabSize;
	int corpusSize;
	int aveDocLength;

	dataset * pdataset;

	LogFile* logFile;

	// model counts
	vector<int> nd;
	vector<vector<int> > ndl;
	vector<vector<vector<int> > > ndlz;
	vector<vector<vector<int> > > nlzw;
	vector<vector<int> > nlz;

	// topic and label assignments
	vector<vector<double> > p;
	vector<vector<int> > z;
	vector<vector<int> > l;

	// model parameters
	vector<vector<double> > pi_dl; // size: (numDocs x L)
	vector<vector<vector<double> > > theta_dlz; // size: (numDocs x L x T)
	vector<vector<vector<double> > > phi_lzw; // size: (L x T x V)

	// hyperparameters
	vector<vector<double> > alpha_lz; // \alpha_tlz size: (L x T)
	vector<double> alphaSum_l;
	vector<vector<vector<double> > > beta_lzw; // size: (L x T x V)
	vector<vector<double> > betaSum_lz;
	vector<vector<double> > gamma_dl; // size: (numDocs x L)
	vector<double> gammaSum_d;
	vector<vector<double> > lambda_lw; // size: (L x V) -- for encoding prior sentiment information

	vector<vector<double> > opt_alpha_lz;  //optimal value, size:(L x T) -- for storing the optimal value of alpha_lz after fix point iteration

	/************************* Functions ***************************/




	void print_out_model_para();

	int set_gamma();

	int init_model_parameters();
	inline int delete_model_parameters() {
		numDocs = 0;
		vocabSize = 0;
		corpusSize = 0;
		aveDocLength = 0;
		return 0;
	}

	int init_estimate();
	int estimate();
	int prior2beta();
	int sampling(int m, int n, int& sentiLab, int& topic);

	// compute parameter functions
	void compute_pi_dl();
	void compute_theta_dlz();
	void compute_phi_lzw();
	double compute_perplexity();

	// update parameter functions
	void init_parameters();
	int update_Parameters();

	// save model parameter funtions
	int save_model(string model_name);
	int save_model_tassign(string filename);
	int save_model_pi_dl(string filename);
	int save_model_theta_dlz(string filename);
	int save_model_phi_lzw(string filename);
	int save_model_others(string filename);
	int save_model_twords(string filename);

};

#endif
