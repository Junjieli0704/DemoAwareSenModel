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


#include "JST_model.h"
using namespace std;


JST_model::JST_model(void) {

	wordmapfile = "wordmap.txt";
	tassign_suffix = ".tassign";
	pi_suffix = ".pi";
	theta_suffix = ".theta";
	phi_suffix = ".phi";
	others_suffix = ".others";
	twords_suffix = ".twords";
	tassign_vis_suffix = ".tassign_vis";

	numTopics = 50;
	numSentiLabs = 3;
	vocabSize = 0;
	numDocs = 0;
	corpusSize = 0;
	aveDocLength = 0;

	niters = 1000;
	twords = 20;

	_alpha  = -1.0;
	_beta = -1.0;
	_gamma = -1.0;
}


JST_model::~JST_model(void) {

}


int JST_model::init_para(Model_Para* model_para){

    this->save_model_name = model_para->save_model_name;

    this->dir = model_para->dir;

    if (model_para->data_file == "") {
        logFile->write_to_log("Please specify the input data file for model estimation!\n","error");
        return 1;
    }
    else {this->data_file = model_para->data_file;}

    if (model_para->senti_lex_file == "") {
        logFile->write_to_log("Please specify the sentiment lexicon file for model estimation!\n","error");
        return 1;
    }
    else {this->senti_lex_file = model_para->senti_lex_file;}

    // Initial numTopics numSentiLabs
    if (model_para->numTopics >= 0.0){
        this->numTopics = model_para->numTopics;
    }

    if (model_para->numSentis >= 0.0){
        this->numSentiLabs = model_para->numSentis;
    }

    // Initial alpha beta gamma
    if (model_para->alpha >= 0.0){
        this->_alpha = model_para->alpha;
    }
    else{this->_alpha = 50.0 / this->numTopics; }

    if (model_para->beta >= 0.0){
        this->_beta = model_para->beta;
    }

    if (model_para->gamma >= 0.0){
        this->_gamma = model_para->gamma;
    }

    // Initial niters twords
    if (model_para->niters >= 0){
        this->niters = model_para->niters;
    }

    if (model_para->twords >= 0){
        this->twords = model_para->twords;
    }


    if (model_para->wordmapfile != "") {
        this->wordmapfile = model_para->wordmapfile;
    }



    return 0;

}

/*
    Add by: JunjieLi@CASIA@2016-05-11
*/

void JST_model::print_out_model_para(){

    logFile->write_to_log("************** Model_Para for JST Training***************\n");
    logFile->write_to_log("model_type      --> JST\n");
    logFile->write_to_log("model_task      --> est\n");
    logFile->write_to_log("save_model_name --> " + this->save_model_name + "\n");
    logFile->write_to_log("dir             --> " + this->dir + "\n");
    logFile->write_to_log("data_file       --> " + this->data_file + "\n");
    logFile->write_to_log("senti_lex_file  --> " + this->senti_lex_file + "\n");
    logFile->write_to_log("alpha           --> " + logFile->convert_other_to_str(this->_alpha) + "\n");
    logFile->write_to_log("beta            --> " + logFile->convert_other_to_str(this->_beta) + "\n");
    logFile->write_to_log("gamma           --> " + logFile->convert_other_to_str(this->_gamma) + "\n");
    logFile->write_to_log("numTopics       --> " + logFile->convert_other_to_str(this->numTopics) + "\n");
    logFile->write_to_log("numSentiLabs    --> " + logFile->convert_other_to_str(this->numSentiLabs) + "\n");
    logFile->write_to_log("niters          --> " + logFile->convert_other_to_str(this->niters) + "\n");
    logFile->write_to_log("wordmapfile     --> " + this->wordmapfile + "\n");
    logFile->write_to_log("*********************************************************\n\n\n");


    logFile->write_to_log("************** Data_Para ********************************\n");
    logFile->write_to_log("numDocs         --> " + logFile->convert_other_to_str(this->pdataset->numDocs) + "\n");
    logFile->write_to_log("vocabSize       --> " + logFile->convert_other_to_str(this->pdataset->vocabSize) + "\n");
    logFile->write_to_log("corpusSize      --> " + logFile->convert_other_to_str(this->pdataset->corpusSize) + "\n");
    logFile->write_to_log("averDocLen      --> " + logFile->convert_other_to_str(this->pdataset->aveDocLength) + "\n");
    logFile->write_to_log("*********************************************************\n\n\n");
}

int JST_model::excute_model(Model_Para* model_para) {

    if (init_para(model_para)) return 1;

    // + read training data
    pdataset = new dataset();
    if (pdataset->read_traindata(data_file, dir + wordmapfile,"word")) {
        logFile->write_to_log("Fail to read training data!\n","error");
        return 1;
    }

    if (senti_lex_file != "") {
	    if (this->senLex.read_senti_lexicon(senti_lex_file)) {
		    logFile->write_to_log("Error! Cannot read sentiFile " + senti_lex_file + "!\n","error");
            delete pdataset;
            return 1;
		}
        // Add non sentiment word prior.
		this->senLex.load_non_senti_word_prior(&pdataset->word2id_train);

		if (this->senLex.get_wordid2senLabelDis(&pdataset->word2id_train))
            return 1;
	}

	if (twords > 0)
        dataset::read_wordmap(dir + wordmapfile, &id2word);

    print_out_model_para();

    init_model_parameters();

	if (init_estimate()) return 1;

	if (estimate()) return 1;

	delete_model_parameters();

	return 0;
}


int JST_model::init_model_parameters()
{
	numDocs = pdataset->numDocs;
	vocabSize = pdataset->vocabSize;
	corpusSize = pdataset->corpusSize;
	aveDocLength = pdataset->aveDocLength;

	// model counts
	nd.resize(numDocs);
	for (int m = 0; m < numDocs; m++) {
		nd[m]  = 0;
	}

	ndl.resize(numDocs);
	for (int m = 0; m < numDocs; m++) {
		ndl[m].resize(numSentiLabs);
		for (int l = 0; l < numSentiLabs; l++)
		    ndl[m][l] = 0;
	}

	ndlz.resize(numDocs);
	for (int m = 0; m < numDocs; m++) {
		ndlz[m].resize(numSentiLabs);
		for (int l = 0; l < numSentiLabs; l++) {
			ndlz[m][l].resize(numTopics);
			for (int z = 0; z < numTopics; z++)
				ndlz[m][l][z] = 0;
		}
	}

	nlzw.resize(numSentiLabs);
	for (int l = 0; l < numSentiLabs; l++) {
		nlzw[l].resize(numTopics);
		for (int z = 0; z < numTopics; z++) {
			nlzw[l][z].resize(vocabSize);
			for (int r = 0; r < vocabSize; r++)
			    nlzw[l][z][r] = 0;
		}
	}

	nlz.resize(numSentiLabs);
	for (int l = 0; l < numSentiLabs; l++) {
		nlz[l].resize(numTopics);
		for (int z = 0; z < numTopics; z++) {
		    nlz[l][z] = 0;
		}
	}

	// posterior P
	p.resize(numSentiLabs);
	for (int l = 0; l < numSentiLabs; l++) {
		p[l].resize(numTopics);
	}

	// model parameters
	pi_dl.resize(numDocs);
	for (int m = 0; m < numDocs; m++) {
		pi_dl[m].resize(numSentiLabs);
	}

	theta_dlz.resize(numDocs);
	for (int m = 0; m < numDocs; m++) {
		theta_dlz[m].resize(numSentiLabs);
		for (int l = 0; l < numSentiLabs; l++) {
			theta_dlz[m][l].resize(numTopics);
		}
	}

	phi_lzw.resize(numSentiLabs);
	for (int l = 0; l < numSentiLabs; l++) {
		phi_lzw[l].resize(numTopics);
		for (int z = 0; z < numTopics; z++) {
			phi_lzw[l][z].resize(vocabSize);
		}
	}

	// init hyperparameters
	alpha_lz.resize(numSentiLabs);
	for (int l = 0; l < numSentiLabs; l++) {
		alpha_lz[l].resize(numTopics);
	}

	alphaSum_l.resize(numSentiLabs);

	if (_alpha <= 0) {
		_alpha =  (double)aveDocLength * 0.05 / (double)(numSentiLabs * numTopics);
	}

	for (int l = 0; l < numSentiLabs; l++) {
		alphaSum_l[l] = 0.0;
	    for (int z = 0; z < numTopics; z++) {
		    alpha_lz[l][z] = _alpha;
		    alphaSum_l[l] += alpha_lz[l][z];
	    }
	}

	opt_alpha_lz.resize(numSentiLabs);
	for (int l = 0; l < numSentiLabs; l++) {
		opt_alpha_lz[l].resize(numTopics);
	}

	//beta
	if (_beta <= 0) _beta = 0.01;

	beta_lzw.resize(numSentiLabs);
	betaSum_lz.resize(numSentiLabs);
	for (int l = 0; l < numSentiLabs; l++) {
		beta_lzw[l].resize(numTopics);
		betaSum_lz[l].resize(numTopics);
		for (int z = 0; z < numTopics; z++) {
			betaSum_lz[l][z] = 0.0;
			beta_lzw[l][z].resize(vocabSize);
			for (int r = 0; r < vocabSize; r++) {
				beta_lzw[l][z][r] = _beta;
			}
		}
	}

	// word prior transformation matrix
	lambda_lw.resize(numSentiLabs);
	for (int l = 0; l < numSentiLabs; l++) {
	    lambda_lw[l].resize(vocabSize);
		for (int r = 0; r < vocabSize; r++) {
			lambda_lw[l][r] = 1;
		}
	}

	// incorporate prior information into beta
	this->prior2beta();
	this->set_gamma();

	return 0;
}


int JST_model::set_gamma() {

	if (_gamma <= 0 ) {
		_gamma = (double)aveDocLength * 0.05 / (double)numSentiLabs;
	}

	gamma_dl.resize(numDocs);
	gammaSum_d.resize(numDocs);

	for (int d = 0; d < numDocs; d++) {
		gamma_dl[d].resize(numSentiLabs);
		gammaSum_d[d] = 0.0;
		for (int l = 0; l < numSentiLabs; l++) {
			gamma_dl[d][l] = _gamma;
			gammaSum_d[d] += gamma_dl[d][l];
		}
	}

	return 0;
}


int JST_model::prior2beta() {

	mapwordid2prior::iterator wordid2priorIt;
	for (wordid2priorIt = this->senLex.wordid2senLabelDis.begin(); wordid2priorIt != this->senLex.wordid2senLabelDis.end(); wordid2priorIt++) {
		int wordID = wordid2priorIt->first;
        for (int j = 0; j < numSentiLabs; j++)  {
            lambda_lw[j][wordID] = wordid2priorIt->second.labDist[j];
        }
    }

	for (int l = 0; l < numSentiLabs; l++) {
		for (int z = 0; z < numTopics; z++) {
			betaSum_lz[l][z] = 0.0;
		    for (int r = 0; r < vocabSize; r++) {
			    beta_lzw[l][z][r] = beta_lzw[l][z][r] * lambda_lw[l][r];
			    betaSum_lz[l][z] += beta_lzw[l][z][r];
		    }
		}
	}

	return 0;
}


void JST_model::compute_phi_lzw() {
	for (int l = 0; l < numSentiLabs; l++)  {
	    for (int z = 0; z < numTopics; z++) {
			for(int r = 0; r < vocabSize; r++) {
				phi_lzw[l][z][r] = (nlzw[l][z][r] + beta_lzw[l][z][r]) / (nlz[l][z] + betaSum_lz[l][z]);
			}
		}
	}
}



void JST_model::compute_pi_dl() {

	for (int m = 0; m < numDocs; m++) {
	    for (int l = 0; l < numSentiLabs; l++) {
		    pi_dl[m][l] = (ndl[m][l] + gamma_dl[m][l]) / (nd[m] + gammaSum_d[m]);
		}
	}
}

void JST_model::compute_theta_dlz() {

	for (int m = 0; m < numDocs; m++) {
	    for (int l = 0; l < numSentiLabs; l++)  {
			for (int z = 0; z < numTopics; z++) {
			    theta_dlz[m][l][z] = (ndlz[m][l][z] + alpha_lz[l][z]) / (ndl[m][l] + alphaSum_l[l]);
			}
		}
	}
}


int JST_model::save_model(string model_name) {
    //cout<<model_name<<endl;

	if (save_model_tassign(dir + model_name + tassign_suffix))
		return 1;

	if (save_model_tassign_vis(dir + model_name + tassign_vis_suffix))
		return 1;

	if (save_model_twords(dir + model_name + twords_suffix))
		return 1;

	if (save_model_pi_dl(dir + model_name + pi_suffix))
		return 1;

	if (save_model_theta_dlz(dir + model_name + theta_suffix))
		return 1;

	if (save_model_phi_lzw(dir + model_name + phi_suffix))
		return 1;

	if (save_model_others(dir + model_name + others_suffix))
		return 1;


	return 0;
}


int JST_model::save_model_tassign(string filename) {
    FILE * fout = fopen(filename.c_str(), "w");
    if (!fout) {
	    logFile->write_to_log("Cannot save file " + filename + "!\n","error");
	    return 1;
    }
	for (int m = 0; m < pdataset->numDocs; m++) {
		fprintf(fout, "%s ", pdataset->docs[m]->docID.c_str());
		for (int n = 0; n < pdataset->docs[m]->length; n++) {
            int word_id = pdataset->docs[m]->words[n];
            //string word_str = pdataset->get_str_from_id(word_id);
	        fprintf(fout, "%d:%d:%d ", word_id, l[m][n], z[m][n]); //  wordID:sentiLab:topic
	    }
	    fprintf(fout, "\n");
    }
    fclose(fout);
	return 0;
}

int JST_model::save_model_tassign_vis(string filename) {
    FILE * fout = fopen(filename.c_str(), "w");
    if (!fout) {
	    logFile->write_to_log("Cannot save file " + filename + "!\n","error");
	    return 1;
    }
	for (int m = 0; m < pdataset->numDocs; m++) {
		fprintf(fout, "%s ", pdataset->docs[m]->docID.c_str());
		for (int n = 0; n < pdataset->docs[m]->length; n++) {
            int word_id = pdataset->docs[m]->words[n];
            string word_str = pdataset->get_str_from_id(word_id);
	        //fprintf(fout, "word_%s:senti_%d:topic_%d ", word_str.c_str(), l[m][n], z[m][n]); //  wordID:sentiLab:topic
	        string label_str = "";
	        if (l[m][n] == 0) label_str = "neu";
	        else if (l[m][n] == 1) label_str = "pos";
	        else if (l[m][n] == 2) label_str = "neg";

	        fprintf(fout, "%s:%s:t_%d ", word_str.c_str(), label_str.c_str(), z[m][n]); //  wordID:sentiLab:topic
	    }
	    fprintf(fout, "\n");
    }
    fclose(fout);
	return 0;
}



int JST_model::save_model_twords(string filename)
{
    FILE * fout = fopen(filename.c_str(), "w");
    if (!fout) {
	    logFile->write_to_log("Cannot save file " + filename + "!\n","error");
	    return 1;
    }

    if (twords > vocabSize) {
	    twords = vocabSize; // print out entire vocab list
    }

    mapid2word::iterator it;

    /*
    for (int k = 0; k < numTopics; k++) {
            for (int l = 0; l < numSentiLabs; l++) {
	        vector<pair<int, double> > words_probs;
	        pair<int, double> word_prob;
	        for (int w = 0; w < vocabSize; w++) {
		        word_prob.first = w; // w: word id/index
	            word_prob.second = phi_lzw[l][k][w]; // topic-word probability
	            words_probs.push_back(word_prob);
	        }

		    std::sort(words_probs.begin(), words_probs.end(), sort_pred());

	        fprintf(fout, "senti%d_topic%d\n", l, k);
	        for (int i = 0; i < twords; i++) {
		        it = id2word.find(words_probs[i].first);
	            if (it != id2word.end())
			        fprintf(fout, "%s   %15f\n", (it->second).c_str(), words_probs[i].second);
	        }
	    }
    }*/


     for (int k = 0; k < numTopics; k++) {
        fprintf(fout, "Topic %dth:\n", k);
        for (int l = 0; l < numSentiLabs; l++) {
	        vector<pair<int, double> > words_probs;
	        pair<int, double> word_prob;
	        for (int w = 0; w < vocabSize; w++) {
		        word_prob.first = w;
	            word_prob.second = phi_lzw[l][k][w];
	            words_probs.push_back(word_prob);
	        }

		    std::sort(words_probs.begin(), words_probs.end(), sort_pred());

		    if (l == 0)
                fprintf(fout, "Label %d : neutral\n",l);
		    else if (l == 1)
                fprintf(fout, "Label %d : positive\n",l);
		    else if (l == 2)
                fprintf(fout, "Label %d : negative\n",l);

	        //fprintf(fout, "Label %dth\n", l);
	        for (int i = 0; i < twords; i++) {
		        it = id2word.find(words_probs[i].first);
	            if (it != id2word.end())
			        fprintf(fout, "%s   %15f\n", (it->second).c_str(), words_probs[i].second);
	        }
	    } // for topic
    } // for label



    fclose(fout);
    return 0;
}

int JST_model::save_model_pi_dl(string filename) {

	FILE * fout = fopen(filename.c_str(), "w");
    if (!fout) {
		logFile->write_to_log("Cannot save file " + filename + "!\n","error");
		return 1;
    }

	for (int m = 0; m < numDocs; m++) {
		fprintf(fout, "%s ", pdataset->docs[m]->docID.c_str());
		for (int l = 0; l < numSentiLabs; l++) {
			fprintf(fout, "%f ", pi_dl[m][l]);
		}
		fprintf(fout, "\n");
    }

    fclose(fout);
	return 0;
}


int JST_model::save_model_theta_dlz(string filename) {

	FILE * fout = fopen(filename.c_str(), "w");
    if (!fout) {
		logFile->write_to_log("Cannot save file " + filename + "!\n","error");
		return 1;
    }

    for(int m = 0; m < numDocs; m++) {
        //fprintf(fout, "Document %d\n", m);
        fprintf(fout, "%s ", pdataset->docs[m]->docID.c_str());
	    for (int l = 0; l < numSentiLabs; l++) {
	        for (int z = 0; z < numTopics; z++) {
		        fprintf(fout, "senti_%d:topic_%d:%f ", l,z,theta_dlz[m][l][z]);
	        }
		 }
		 fprintf(fout, "\n");
    }

    fclose(fout);
    return 0;
}


int JST_model::save_model_phi_lzw(string filename) {

	FILE * fout = fopen(filename.c_str(), "w");
    if (!fout) {
	    logFile->write_to_log("Cannot save file " + filename + "!\n","error");
	    return 1;
    }

	for (int l = 0; l < numSentiLabs; l++) {
	    for (int z = 0; z < numTopics; z++) {
		    fprintf(fout, "senti:%d_topic:%d ", l, z);
     	    for (int r = 0; r < vocabSize; r++) {
			    fprintf(fout, "%d:%f ", r,phi_lzw[l][z][r]);
     	    }
            fprintf(fout, "\n");
	   }
    }

    fclose(fout);
	return 0;
}



int JST_model::save_model_others(string filename) {

	FILE * fout = fopen(filename.c_str(), "w");
    if (!fout) {
	    logFile->write_to_log("Cannot save file " + filename + "!\n","error");
	    return 1;
    }

	fprintf(fout, "dir=%s\n", this->dir.c_str());
	fprintf(fout, "data_file=%s\n", this->data_file.c_str());
	fprintf(fout, "senti_lex_file=%s\n", this->senti_lex_file.c_str());

	fprintf(fout, "\n-------------------- Corpus statistics -----------------------\n");
    fprintf(fout, "numDocs=%d\n", numDocs);
    fprintf(fout, "corpusSize=%d\n", corpusSize);
	fprintf(fout, "aveDocLength=%d\n", aveDocLength);
    fprintf(fout, "vocabSize=%d\n", vocabSize);

    fprintf(fout, "\n---------------------- Model settings -----------------------\n");
	fprintf(fout, "numSentiLabs=%d\n", numSentiLabs);
	fprintf(fout, "numTopics=%d\n", numTopics);

	fprintf(fout, "_alpha=%f\n", _alpha);
	fprintf(fout, "_beta=%f\n", _beta);
	fprintf(fout, "_gamma=%f\n", _gamma);

	fclose(fout);
    return 0;
}


int JST_model::init_estimate() {

    int sentiLab, topic;
	srand(time(0)); // initialize for random number generation
	z.resize(numDocs);
	l.resize(numDocs);

	for (int m = 0; m < numDocs; m++) {
		int docLength = pdataset->docs[m]->length;
		z[m].resize(docLength);
		l[m].resize(docLength);

        for (int t = 0; t < docLength; t++) {
		    if (pdataset->docs[m]->words[t] < 0) {
		        string word_token = logFile->convert_other_to_str(pdataset->docs[m]->words[t]);
                string m_str = logFile->convert_other_to_str(m);
                string t_str = logFile->convert_other_to_str(t);
                string temp_str = "ERROE! word token " +  word_token + " has index smaller than 0 at doc[" + m_str + "][" + t_str + "]\n";
			    logFile->write_to_log(temp_str,"error");
				return 1;
			}

			int priorSentiLabel = this->senLex.get_word_senlabel(pdataset->docs[m]->words[t]);

    	    if ((priorSentiLabel > -1) && (priorSentiLabel < numSentiLabs)) {
			    sentiLab = priorSentiLabel; // incorporate prior information into the model

			}
			else {
			    sentiLab = (int)(((double)rand() / RAND_MAX) * numSentiLabs);
			    if (sentiLab == numSentiLabs) sentiLab = numSentiLabs -1;  // to avoid over array boundary
			}
    	    l[m][t] = sentiLab;

			// random initialize the topic assginment
			topic = (int)(((double)rand() / RAND_MAX) * numTopics);
			if (topic == numTopics)  topic = numTopics - 1; // to avoid over array boundary
			z[m][t] = topic;

			// model count assignments
			nd[m]++;
			ndl[m][sentiLab]++;
			ndlz[m][sentiLab][topic]++;
			nlzw[sentiLab][topic][pdataset->docs[m]->words[t]]++;
			nlz[sentiLab][topic]++;
        }
    }

    return 0;
}


// Add_JJLi 2016-05-05
// Compute perplexity
double JST_model::compute_perplexity(){

    //compute_phi();
    //compute_theta();    //  theta = self.n_m_z[m] / (len(self.docs[m]) + Kalpha)

    compute_pi_dl();
    compute_theta_dlz();
    compute_phi_lzw();

    double N = 0;
    double log_per = 0.0;
    for (int m = 0; m < numDocs; m++) {
        double doc_plex = 0.0;

        for (int n = 0; n < pdataset->docs[m]->length; n++) {
            int w = pdataset->docs[m]->words[n];
            double doc_word_prob = 0;

            for (int senLabel = 0; senLabel < numSentiLabs; senLabel ++){
                for (int topic = 0; topic < numTopics; topic ++){
                    doc_word_prob = doc_word_prob + phi_lzw[senLabel][topic][w] * theta_dlz[m][senLabel][topic] * pi_dl[m][senLabel];
                }
            }


           // for (int k = 0; k < K; k ++){
           //    doc_word_prob = doc_word_prob + theta[m][k] * phi[k][w];
           //}

            //compute: numpy.log(numpy.inner(phi[:,w], theta))
            double neg_log_doc_prob = log(doc_word_prob);

            //compute: log_per -= numpy.log(numpy.inner(phi[:,w], theta))
            log_per -= neg_log_doc_prob;
            //double log_prob_z_w = log(phi[topic][w]);
            //doc_plex += log_prob_z_w;
        }
        //all_doc_plex += doc_plex;
        N += pdataset->docs[m]->length;  //  N += len(doc)
    }

    double plex_value = exp(log_per / N);

    return plex_value;
}

int JST_model::estimate() {

    int ** senti_sample_ana;
    senti_sample_ana = new int*[3];
    for(int j=0;j<3;j++){
        senti_sample_ana[j]=new int[3];
    }

	int sentiLab, topic;
	mapname2labs::iterator it;

    logFile->write_to_log("Iteration 0 --> perplexity: " + logFile->convert_other_to_str(compute_perplexity())+ "\n");
	logFile->write_to_log("Sampling " + logFile->convert_other_to_str(niters) + " iterations!\n");
	for (int liter = 1; liter <= niters; liter++) {
        for (int i = 0; i < 3; i++)
        for (int j = 0; j < 3; j++){
            senti_sample_ana[i][j] = 0;
        }
        //if (liter % 50 == 0)
        string iter_str = logFile->convert_other_to_str(liter);
        string perplex_str = logFile->convert_other_to_str(compute_perplexity());
        logFile->write_to_log("Iteration " + iter_str + " --> perplexity: " + perplex_str + "\n");
		for (int m = 0; m < numDocs; m++) {
		    for (int n = 0; n < pdataset->docs[m]->length; n++) {
				sampling(m, n, sentiLab, topic);
				l[m][n] = sentiLab;
				z[m][n] = topic;
                int w_id = pdataset->docs[m]->words[n];
                senti_sample_ana[this->senLex.get_word_senlabel(w_id)][sentiLab]++;
			}
		}
		for (int i = 0; i < 3; i++)
        for (int j = 0; j < 3; j++)
            cout<<"senti_sample_ana["<<i<<"]["<<j<<"] = "<<senti_sample_ana[i][j]<<endl;
	}

	logFile->write_to_log("Gibbs sampling completed!\n");
	logFile->write_to_log("Saving the final model!\n");
	compute_pi_dl();
	compute_theta_dlz();
	compute_phi_lzw();
	save_model(utils::generate_model_name(-1,this->save_model_name));

	return 0;
}


int JST_model::sampling(int m, int n, int& sentiLab, int& topic) {

	sentiLab = l[m][n];
	topic = z[m][n];
	int w = pdataset->docs[m]->words[n]; // the ID/index of the current word token in vocabulary
	double u;

	nd[m]--;
	ndl[m][sentiLab]--;
	ndlz[m][sentiLab][topic]--;
	nlzw[sentiLab][topic][pdataset->docs[m]->words[n]]--;
	nlz[sentiLab][topic]--;



	// do multinomial sampling via cumulative method
	for (int l = 0; l < numSentiLabs; l++) {
		for (int k = 0; k < numTopics; k++) {
			p[l][k] = (nlzw[l][k][w] + beta_lzw[l][k][w]) / (nlz[l][k] + betaSum_lz[l][k]) *
		   		(ndlz[m][l][k] + alpha_lz[l][k]) / (ndl[m][l] + alphaSum_l[l]) *
				(ndl[m][l] + gamma_dl[m][l]) / (nd[m] + gammaSum_d[m]);
		}
	}

	// accumulate multinomial parameters
	for (int l = 0; l < numSentiLabs; l++)  {
		for (int k = 0; k < numTopics; k++) {
			if (k==0)  {
			    if (l==0) continue;
		        else p[l][k] += p[l-1][numTopics-1]; // accumulate the sum of the previous array
			}
			else p[l][k] += p[l][k-1];
		}
	}

	// probability normalization
	u = ((double)rand() / RAND_MAX) * p[numSentiLabs-1][numTopics-1];

	// sample sentiment label l, where l \in [0, S-1]
	bool loopBreak=false;
	for (sentiLab = 0; sentiLab < numSentiLabs; sentiLab++) {
		for (topic = 0; topic < numTopics; topic++) {
		    if (p[sentiLab][topic] > u) {
		        loopBreak = true;
		        break;
		    }
		}
		if (loopBreak == true) {
			break;
		}
	}

	if (sentiLab == numSentiLabs) sentiLab = numSentiLabs - 1; // to avoid over array boundary
	if (topic == numTopics) topic = numTopics - 1;

	// add estimated 'z' and 'l' to count variables
	nd[m]++;
	ndl[m][sentiLab]++;
	ndlz[m][sentiLab][topic]++;
	nlzw[sentiLab][topic][pdataset->docs[m]->words[n]]++;
	nlz[sentiLab][topic]++;

    return 0;
}
