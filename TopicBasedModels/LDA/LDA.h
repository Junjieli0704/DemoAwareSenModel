#ifndef LDA_H
#define LDA_H

/*
 * Copyright (C) 2007 by
 *
 * 	Xuan-Hieu Phan
 *	hieuxuan@ecei.tohoku.ac.jp or pxhieu@gmail.com
 * 	Graduate School of Information Sciences
 * 	Tohoku University
 *
 * GibbsLDA++ is a free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published
 * by the Free Software Foundation; either version 2 of the License,
 * or (at your option) any later version.
 *
 * GibbsLDA++ is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with GibbsLDA++; if not, write to the Free Software Foundation,
 * Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA.
 */

/*
 * References:
 * + The Java code of Gregor Heinrich (gregor@arbylon.net)
 *   http://www.arbylon.net/projects/LdaGibbsSampler.java
 * + "Parameter estimation for text analysis" by Gregor Heinrich
 *   http://www.arbylon.net/publications/text-est.pdf
*/

/*********************************************************************/
// Rewrited By Junjie@CASIA@2016-06-20
/*********************************************************************/

#include "constants.h"
#include "dataset.h"
#include "utils.h"
#include "log.h"
#include <ctime>
#include <stdio.h>
#include <stdlib.h>
#include "strtokenizer.h"
#include "utils.h"
#include <math.h>
#include "FileOut.h"

using namespace std;

class LDA
{

public:
    LDA();
    ~LDA();

    void excute_model(Model_Para* model_para);

    void set_log_file(LogFile* logFile){
        this->log_file = logFile;
    }


private:
    CFileOut fileout;
    int model_status;
    LogFile *log_file;
    string wordmapfile;		// file that contains word map [string -> integer id]

    string tassign_suffix;	// suffix for topic assignment file
    string theta_suffix;	// suffix for theta file
    string phi_suffix;		// suffix for phi file
    string others_suffix;	// suffix for file containing other parameters
    string twords_suffix;	// suffix for file containing words-per-topics

    string dir;			    // out directory
    string data_file;		// in data file
    string save_model_name;	// model name

    dataset * ptrndata;	    // pointer to training dataset object
    dataset * ptestdata;	// pointer to testing dataset object

    mapid2word id2word;     // word map [int => string]

	int num_topics;
	int num_iters;
	int twords;	        // show top t_word-th words in each topic in model.twords_suffix

	int ** n_okw_train; // n_okw_train[k][w]: total number of word w assigned to topic k in the model data,
                        // size: num_topics * num_vocabs
	int *  n_oko_train; // n_oko_train[k]: total number of words assigned to topic k in the model data, size: num_topics



	// model counts
	int *    n_doo;    // n_doo[d]: total number of words in document d, size: num_docs
	int *    n_oko;    // n_oko[k]: total number of words assigned to topic k, size: num_topics
	int **   n_dko;    // n_dko[d][k]: total number of words in document d assigned to topic k,
                       // size: num_topics * num_topics
	int **   n_okw;    // n_okw[k][w]: total number of word w assigned to topic k,
                       // size: num_topics * num_vocabs

    // topic and label assignments
    double * p_oko;    // p_oko[k]: the probably of current word that has been assigned topic=k
    int **   z_dow;    // z_dow[d][w]: topic assignments for words, size: num_docs * num_vocabs

    // hyperparameters
    double alpha;
	double beta;

    // model parameters
    double** theta_dko; // size: num_docs * num_topics
    double** phi_okw;   // size: num_topics * num_vocabs


    void delete_model_parameters();
    int init_para(Model_Para* model_para);
    void print_out_model_para();
    void compute_theta();
    void compute_phi();
    double compute_perplexity();
    int save_model(string model_name);
    int save_model_tassign(string filename);
    int save_model_theta(string filename);
    int save_model_phi(string filename);
    int save_model_others(string filename);
    int save_model_twords(string filename);
    int sampling(int m, int n);
    void est_inf();

    // For Training
    int init_est();

    // For Testing
    int init_inf();
    int load_model_para(string model_name);
    int load_model(string model_name);

};

#endif // LDA_H
