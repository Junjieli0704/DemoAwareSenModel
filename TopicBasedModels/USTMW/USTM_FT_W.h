#ifndef USTM_FT_W_H
#define USTM_FT_W_H

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

class USTM_FT_W
{
public:
    USTM_FT_W();
    ~USTM_FT_W();

	// init functions

	int excute_model(Model_Para* model_para){
	    if (model_para->model_status == MODEL_STATUS_EST)
            excute_model_train(model_para);
        if (model_para->model_status == MODEL_STATUS_INF)
            excute_model_test(model_para);
	}

	int excute_model_train(Model_Para* model_para);

	int excute_model_test(Model_Para* model_para);

    void set_log_file(LogFile* logFile){
        this->log_file = logFile;
    }

private:

    int num_corpus;
    double ave_doc_length;
	int num_docs;
	int num_vocabs;
	int num_demos;
    int num_topics;
	int num_sentis;
	int niters;
	int twords;

    sentiLex senLex;
    mapid2word id2word; // word map [int => string]
    mapid2word demo2word; // word map [int => string]

	string dir;
	string data_file;
	string data_demo_file;
	string senti_lex_file;
	string wordmapfile;
	string demomapfile;

	string tassign_suffix;
	string tassign_vis_suffix;
	string pi_suffix;
	string theta_suffix;
	string phi_suffix;
	string others_suffix;
	string twords_suffix;
	string psi_suffix;
	string eta_suffix;

	string save_model_name;

	double _alpha;
	double _beta;
	double _gamma;

    dataset * ptrndata;	        // pointer to training dataset object
    dataset * ptrndemodata;	    // pointer to training dataset object
    dataset * ptestdata;	    // pointer to testing dataset object
    dataset * ptestdemodata;	// pointer to testing dataset object

	LogFile* log_file;

	int model_status;

	// Only for testing, counts in model.
    int ***  n_ojkow_train; // n_ojkow_train[j][k][w]: total number of times the w has been
                            // assigned to tag j and topic k, size: demoSize * numTopics * vocabSize
    int **   n_ojkoo_train; // n_ojkoo_train[j][k]: total number of words that have been
                            // assigned to tag j and topic k, size: demoSize * numTopics
    int **** n_ojksw_train; // n_ojksw_train[j][k][s][w]: total number of times that word w has
                            // beend assigned to tag j, topic k and sentiment s in all documents,
                            // size: demoSize * numTopics * numSentiLabs * vocabSize
    int ***  n_ojkso_train; // n_ojkso_train[j][k][s]: total number of words that have been
                            // assigned to tag j, topic k and sentiment s in all documents,
                            // size: numTopics * numSentiLabs * vocabSize


	// model counts
	int *    n_doooo; // n_doooo[d]: total number of words in document d, size: numDocs
	int **   n_djooo; // n_djooo[d][j]: total number of words in document d assigned to tag j, size: numDocs * demoSize
	int ***  n_djkoo; // n_djkoo[d][j][k]: total number of words in document d that have
	                  // assigned to tag j and topic k, size: numDocs * demoSize * numTopics
    int ***  n_ojkow; // n_ojkow[j][k][w]: total number of times the w has been
                      // assigned to tag j and topic k, size: demoSize * numTopics * vocabSize
    int **   n_ojkoo; // n_ojkoo[j][k]: total number of words that have been
                      // assigned to tag j and topic k, size: demoSize * numTopics
    int **** n_djkso; // n_djkso[d][j][k][s]: total number of words that have been
                      // assigned to tag j, topic k and sentiment s in document d,
                      // size: numDocs * demoSize * numTopics * numSentiLabs
    int **** n_ojksw; // n_ojksw[j][k][s][w]: total number of times that word w has
                      // beend assigned to tag j, topic k and sentiment s in all documents,
                      // size: demoSize * numTopics * numSentiLabs * vocabSize
    int ***  n_ojkso; // n_ojkso[j][k][s]: total number of words that have been
                      // assigned to tag j, topic k and sentiment s in all documents,
                      // size: numTopics * numSentiLabs * vocabSize



    // topic and label assignments
    double *** p_ojkso;  // p_ojkso[t][z][s]: the probably of current word that has been
                         // assigned (tag=t,sentiment=s,topic=z)
                         // size: demoSize * numTopics * numSentiLabs
    int ** t_dooow;      // t_dooow[d][w] new sampled tag for word w in document d
    int ** z_dooow;      // z_dooow[d][w] new sampled topic for word w in document d
    int ** s_dooow;      // s_dooow[d][w] new sampled sentiment for word w in document d

    // hyperparameters
    double ** beta_ooosw; // beta_ooosw[s][w] weight of word w in the Dirichlet prior
                          // for the topics with sentiment s
    double *  beta_oooso; // beta_oooso[s] sum of the weights of all words in the Dirichlet prior
                          // for the topics with sentiment s

    // model parameters
    double**   psi_djooo;   // size: numDocs * demoSize
    double***  theta_djkoo; // size: numDocs * demoSize * numTopics
    double**** phi_ojksw;   // size: demoSize * numTopics * numSentiLabs * vocabSize
    double**** eta_djkso;   // size: numDocs * demoSize * numTopics * numSentiLabs


    /************************* Functions ***************************/
    int init_para(Model_Para* model_para);
    void print_out_model_para();
    int prior2beta();
    int init_model_parameters();
    void delete_model_parameters();
    void compute_phi_ojksw();
	void compute_eta_djkso();
	void compute_theta_djkoo();
	void compute_psi_djooo();
	double compute_perplexity();
	int save_model(string model_name);
    int save_model_tassign(string filename);
    int save_model_tassign_vis(string filename);
    int save_model_twords(string filename);
    int save_model_psi_djooo(string filename);
    int save_model_theta_djkoo(string filename);
    int save_model_eta_djkso(string filename);
    int save_model_phi_ojksw(string filename);
    int save_model_others(string filename);

    //For Training
	int init_estimate();
    int estimate();
    int sampling(int m, int n, int& sentiLab, int& topic, int& tag);

    //For Testing
    int init_inf();
    int load_model_para(string model_name);
    int load_model(string model_name);
    int inference();
    int inf_sampling(int m, int n, int& sentiLab, int& topic, int& tag);



};

#endif // USTM_FT_W_H
