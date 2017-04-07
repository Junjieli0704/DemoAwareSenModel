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



#include "JST_inference.h"

JST_inference::JST_inference()
{
    numSentiLabs = 0;
	numTopics = 0;
	numDocs = 0;
	vocabSize = 0;
	newNumDocs = 0;
	newVocabSize = 0;

	wordmapfile = "wordmap.txt";
    tassign_suffix = ".newtassign";
    pi_suffix = ".newpi";
    theta_suffix = ".newtheta";
    phi_suffix = ".newphi";
    others_suffix = ".newothers";
    twords_suffix = ".newtwords";
    tassign_vis_suffix = ".newtassign_vis";
	save_model_name = "";
	dir = "";
	data_file = "";
	senti_lex_file = "";

	twords = 20;
	niters = 40;

	ptestdata = NULL;
	ptrndata = NULL;
	_alpha  = -1.0;
	_beta = -1.0;
	_gamma = -1.0;
}


JST_inference::~JST_inference()
{
    //logFile->write_to_log("JST_inference::~JST_inference begin\n");

    /*
    cout<<ptestdata<<endl;
	if (ptestdata)
		delete ptestdata;
    cout<<ptestdata<<endl;

    cout<<ptrndata<<endl;
	if (ptrndata)
		delete ptrndata;
    cout<<ptrndata<<endl;
    */

    //logFile->write_to_log("JST_inference::~JST_inference end\n");
}

int JST_inference::excute_model(Model_Para *model_para) {


    if(init_para(model_para)) return 1;


	if(init_inf()) {
	    logFile->write_to_log("Throw expectation in init_inf()!  \n","error");
		return 1;
	}


	if(inference()) {
	    logFile->write_to_log("Throw expectation in inference()!  \n","error");
		return 1;
	}
    return 0;
}

void JST_inference::compute_newpi() {

    //cout<<"compute_newpi() begin......\n";
	for (int m = 0; m < ptestdata->numDocs; m++) {
	    for (int l = 0; l < numSentiLabs; l++) {
		    newpi_dl[m][l] = (new_ndl[m][l] + gamma_l[l]) / (new_nd[m] + gammaSum);
	    }
	}
	//cout<<"compute_newpi() end......\n";
}


void JST_inference::compute_newtheta() {

    //cout<<"compute_newtheta() begin......\n";
	for (int m = 0; m < ptestdata->numDocs; m++) {
	    for (int l = 0; l < numSentiLabs; l++)  {
			for (int z = 0; z < numTopics; z++) {
			    newtheta_dlz[m][l][z] = (new_ndlz[m][l][z] + alpha_lz[l][z]) / (new_ndl[m][l] + alphaSum_l[l]);
			}
		}
	}
	//cout<<"compute_newtheta() end......\n";
}


int JST_inference::compute_newphi() {

    //cout<<"compute_newphi() begin......\n";
	map<int, int>::iterator it;

	for (int l = 0; l < numSentiLabs; l++)  {
	    for (int z = 0; z < numTopics; z++) {
			for(int r = 0; r < ptestdata->vocabSize; r++) {
			    it = ptestdata->_id2id.find(r);
				if (it != ptestdata->_id2id.end()) {
				    newphi_lzw[l][z][r] = (nlzw[l][z][it->second] + new_nlzw[l][z][r] + beta_lzw[l][z][r]) / (nlz[l][z] + new_nlz[l][z] + betaSum_lz[l][z]);
				}
				else {
				    logFile->write_to_log("Error! Cannot find word [" + logFile->convert_other_to_str(r) + "] !\n", "error");
					return 1;
				}
			}
		}
	}
	//cout<<"compute_newphi() end......\n";
	return 0;
}




// Add_JJLi 2016-05-03
// Compute perplexity in Inference
double JST_inference::compute_perplexity(){

    //cout<<"Compute perplexity begin......\n";

    compute_newpi();
    compute_newtheta();
    compute_newphi();

    double N = 0;
    double log_per = 0.0;
    for (int m = 0; m < ptestdata->numDocs; m++) {
        double doc_plex = 0.0;
        for (int n = 0; n < ptestdata->_docs[m]->length; n++) {
            int w = ptestdata->_docs[m]->words[n];
            double doc_word_prob = 0;
            //cout<<m<<n<<endl;
            for (int senLabel = 0; senLabel < numSentiLabs; senLabel ++){
                for (int topic = 0; topic < numTopics; topic ++){
                    doc_word_prob = doc_word_prob + newphi_lzw[senLabel][topic][w] * newtheta_dlz[m][senLabel][topic] * newpi_dl[m][senLabel];
                }
            }

            //compute: numpy.log(numpy.inner(phi[:,w], theta))
            double neg_log_doc_prob = log(doc_word_prob);

            //compute: log_per -= numpy.log(numpy.inner(phi[:,w], theta))
            log_per -= neg_log_doc_prob;
            //double log_prob_z_w = log(phi[topic][w]);
            //doc_plex += log_prob_z_w;
        }
        //all_doc_plex += doc_plex;
        N += ptestdata->_docs[m]->length;  //  N += len(doc)
    }

    double plex_value = exp(log_per / N);

    //cout<<"Compute perplexity end......\n";

    return plex_value;

}

int JST_inference::inf_sampling(int m, int n, int& sentiLab, int& topic) {
	sentiLab = new_l[m][n];
	topic = new_z[m][n];
	int w = ptestdata->docs[m]->words[n];   // word index of trained model
	int _w = ptestdata->_docs[m]->words[n]; // word index of test data
	double u;

	new_nd[m]--;
	new_ndl[m][sentiLab]--;
	new_ndlz[m][sentiLab][topic]--;
	new_nlzw[sentiLab][topic][_w]--;
	new_nlz[sentiLab][topic]--;

    // do multinomial sampling via cumulative method
    for (int l = 0; l < numSentiLabs; l++) {
  	    for (int k = 0; k < numTopics; k++) {
		    new_p[l][k] = (nlzw[l][k][w] + new_nlzw[l][k][_w] + beta_lzw[l][k][_w]) / (nlz[l][k] + new_nlz[l][k] + betaSum_lz[l][k]) *
			    (new_ndlz[m][l][k] + alpha_lz[l][k]) / (new_ndl[m][l] + alphaSum_l[l]) *
			    (new_ndl[m][l] + gamma_l[l]) / (new_nd[m] + gammaSum);
		}
	}

	// accumulate multinomial parameters
	for (int l = 0; l < numSentiLabs; l++) {
		for (int k = 0; k < numTopics; k++) {
			if (k==0) {
			    if (l==0) continue;
		        else new_p[l][k] += new_p[l-1][numTopics-1];
			}
			else new_p[l][k] += new_p[l][k-1];
	    }
	}
	// probability normalization
	u = ((double)rand() / RAND_MAX) * new_p[numSentiLabs-1][numTopics-1];

	for (sentiLab = 0; sentiLab < numSentiLabs; sentiLab++) {
		for (topic = 0; topic < numTopics; topic++) {
		    if (new_p[sentiLab][topic] > u) {
		    	goto stop;
		    }
		}
	}

	stop:
	if (sentiLab == numSentiLabs) sentiLab = numSentiLabs - 1; // the max value of label is (S - 1)
	if (topic == numTopics) topic = numTopics - 1;

	// add estimated 'z' and 'l' to counts
	new_nd[m]++;
	new_ndl[m][sentiLab]++;
	new_ndlz[m][sentiLab][topic]++;
	new_nlzw[sentiLab][topic][_w]++;
	new_nlz[sentiLab][topic]++;

    return 0;
}

int JST_inference::save_model(string model_name) {

	if (save_model_newtassign(dir + save_model_name + tassign_suffix))
        return 1;
    if (save_model_newtassign_vis(dir + save_model_name + tassign_vis_suffix))
        return 1;
	//else cout<<"save_model_newtassign finished......\n";

	if (save_model_newtwords(dir + save_model_name + twords_suffix))
		return 1;
    //else cout<<"save_model_newtwords finished......\n";

	if (save_model_newpi_dl(dir + save_model_name + pi_suffix))
		return 1;
    //else cout<<"save_model_newpi_dl finished......\n";

	if (save_model_newtheta_dlz(dir + save_model_name + theta_suffix))
		return 1;
    //else cout<<"save_model_newtheta_dlz finished......\n";

	if (save_model_newphi_lzw(dir + save_model_name + phi_suffix))
		return 1;

    //else cout<<"save_model_newphi_lzw finished......\n";
	//if (save_model_newothers(dir + save_model_name + others_suffix))
	//	return 1;

	return 0;
}



int JST_inference::save_model_newpi_dl(string filename) {

    FILE * fout = fopen(filename.c_str(), "w");
    if (!fout) {
		logFile->write_to_log("Cannot save file " + filename + "!\n","error");
		return 1;
    }

    for (int m = 0; m < ptestdata->numDocs; m++) {
		fprintf(fout, "%s ", ptestdata->docs[m]->docID.c_str());
		for (int l = 0; l < numSentiLabs; l++) {
			fprintf(fout, "%f ", newpi_dl[m][l]);
		}
		fprintf(fout, "\n");
    }

    fclose(fout);
	return 0;
}



int JST_inference::save_model_newtheta_dlz(string filename) {

    FILE * fout = fopen(filename.c_str(), "w");
    if (!fout) {
		logFile->write_to_log("Cannot save file " + filename + "!\n","error");
		return 1;
    }

    for(int m = 0; m < ptestdata->numDocs; m++) {
        //fprintf(fout, "Document %d\n", m);
        fprintf(fout, "%s ", ptestdata->docs[m]->docID.c_str());
	    for (int l = 0; l < numSentiLabs; l++) {
	        for (int z = 0; z < numTopics; z++) {
		        fprintf(fout, "label_%d:topic_%d:%f ", l,z,newtheta_dlz[m][l][z]);
	        }
		 }
		 fprintf(fout, "\n");
    }

    fclose(fout);
	return 0;
}



int JST_inference::save_model_newphi_lzw(string filename) {

	FILE * fout = fopen(filename.c_str(), "w");
    if (!fout) {
	    logFile->write_to_log("Cannot save file " + filename + "!\n","error");
	    return 1;
    }

    for (int l = 0; l < numSentiLabs; l++) {
	    for (int z = 0; z < numTopics; z++) {
		    fprintf(fout, "Label:%d_Topic:%d ", l, z);
     	    for (int r = 0; r < ptestdata->vocabSize; r++) {
			    fprintf(fout, "%d:%f ", r,newphi_lzw[l][z][r]);
     	    }
            fprintf(fout, "\n");
	   }
    }


    fclose(fout);
	return 0;
}


int JST_inference::save_model_newtwords(string filename) {

	mapid2word::iterator it; // typedef map<int, string> mapid2word
	map<int, int>::iterator _it;

	FILE * fout = fopen(filename.c_str(), "w");
    if (!fout) {
	    logFile->write_to_log("Cannot save file " + filename + "!\n","error");
	    return 1;
    }

    if (twords > ptestdata->vocabSize) {
	    twords = ptestdata->vocabSize;
    }

    for (int k = 0; k < numTopics; k++) {
        fprintf(fout, "Topic %dth:\n", k);
        for (int l = 0; l < numSentiLabs; l++) {
	        vector<pair<int, double> > words_probs;
	        pair<int, double> word_prob;
	        for (int w = 0; w < ptestdata->vocabSize; w++) {
		        word_prob.first = w;
	            word_prob.second = newphi_lzw[l][k][w];
	            words_probs.push_back(word_prob);
	        }

		    std::sort(words_probs.begin(), words_probs.end(), sort_pred());

	        fprintf(fout, "Label %dth\n", l);
	        for (int i = 0; i < twords; i++) {
				_it = ptestdata->_id2id.find(words_probs[i].first);
				if (_it == ptestdata->_id2id.end()) {
		            continue;
	            }
				it = id2word.find(_it->second);
	            if (it != id2word.end()) {
			        fprintf(fout, "\t%s   %f\n", (it->second).c_str(), words_probs[i].second);
	            }
	        }
	    } // for topic
    } // for label

    fclose(fout);
	return 0;
}


int JST_inference::save_model_newtassign(string filename) {

	FILE * fout = fopen(filename.c_str(), "w");
    if (!fout) {
	    logFile->write_to_log("Cannot save file " + filename + "!\n","error");
	    return 1;
    }

	for (int m = 0; m < ptestdata->numDocs; m++) {
		fprintf(fout, "%s ", ptestdata->docs[m]->docID.c_str());
		for (int n = 0; n < ptestdata->docs[m]->length; n++) {
	        fprintf(fout, "%d:%d:%d ", ptestdata->docs[m]->words[n], new_l[m][n], new_z[m][n]); //  wordID:sentiLab:topic
	    }
	    fprintf(fout, "\n");
    }

    fclose(fout);
	return 0;
}

int JST_inference::save_model_newtassign_vis(string filename) {

	FILE * fout = fopen(filename.c_str(), "w");
    if (!fout) {
	    logFile->write_to_log("Cannot save file " + filename + "!\n","error");
	    return 1;
    }

	for (int m = 0; m < ptestdata->numDocs; m++) {
		fprintf(fout, "%s ", ptestdata->docs[m]->docID.c_str());
		for (int n = 0; n < ptestdata->docs[m]->length; n++) {
             int word_id = ptestdata->docs[m]->words[n];
             string word_str = ptestdata->get_str_from_id(word_id);
	         fprintf(fout, "%s:s_%d:t_%d ", word_str.c_str(), new_l[m][n], new_z[m][n]); //  wordID:sentiLab:topic
         }
	    fprintf(fout, "\n");
    }

    fclose(fout);
	return 0;
}




int JST_inference::inference() {

    logFile->write_to_log("inference() begin......\n");

	int sentiLab, topic;
	logFile->write_to_log("Iteration 0 --> perplexity: " + logFile->convert_other_to_str(compute_perplexity())+ "\n");
	logFile->write_to_log("Sampling " + logFile->convert_other_to_str(niters) + " iterations!\n");

	for (int liter = 1; liter <= niters; liter++) {
		//printf("Iteration %d ...\n", liter);
        string iter_str = logFile->convert_other_to_str(liter);
        string perplex_str = logFile->convert_other_to_str(compute_perplexity());
        logFile->write_to_log("Iteration " + iter_str + " --> perplexity: " + perplex_str + "\n");
		for (int m = 0; m < ptestdata->numDocs; m++) {
			for (int n = 0; n < ptestdata->docs[m]->length; n++) {
				inf_sampling(m, n, sentiLab, topic);
				new_l[m][n] = sentiLab;
				new_z[m][n] = topic;
			}
		}
    }

	logFile->write_to_log("Gibbs sampling completed!\n");
	logFile->write_to_log("Saving the final model!\n");

	compute_newpi();
	compute_newtheta();
	compute_newphi();
	save_model(utils::generate_model_name(-1,this->save_model_name));
    logFile->write_to_log("inference() end......\n");
	return 0;
}





int JST_inference::init_para(Model_Para* model_para){

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
    Add by: JunjieLi@CASIA@2016-05-12
*/

void JST_inference::print_out_model_para(){


    logFile->write_to_log("************** Model_Para for JST Testing***************\n");
    logFile->write_to_log("model_type      --> JST\n");
    logFile->write_to_log("model_task      --> inf\n");
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
    logFile->write_to_log("numDocs         --> " + logFile->convert_other_to_str(this->ptestdata->numDocs) + "\n");
    logFile->write_to_log("vocabSize       --> " + logFile->convert_other_to_str(this->ptestdata->vocabSize) + "\n");
    logFile->write_to_log("corpusSize      --> " + logFile->convert_other_to_str(this->ptestdata->corpusSize) + "\n");
    logFile->write_to_log("averDocLen      --> " + logFile->convert_other_to_str(this->ptestdata->aveDocLength) + "\n");
    logFile->write_to_log("*********************************************************\n\n\n");
}

// read '.others' file
int JST_inference::read_model_setting(string filename) {

	char buff[BUFF_SIZE_LONG];
	string line;
	numSentiLabs = 0;
	numTopics = 0;
	numDocs = 0;
	vocabSize = 0;

	FILE * fin = fopen(filename.c_str(), "r");
	if (!fin) {
        printf("Cannot read file %s!\n", filename.c_str());
        return 1;
	}

	while (fgets(buff, BUFF_SIZE_LONG - 1, fin) != NULL) {
		line = buff;
		strtokenizer values(line, ": \t\r\n={}[]"); // \t\r\n are separators

		if (values.token(0) == "numSentiLabs") {
			numSentiLabs = atoi(values.token(1).c_str());
		}
		else if (values.token(0) == "numTopics") {
			numTopics = atoi(values.token(1).c_str());
		}
		else if (values.token(0) == "numDocs") {
			numDocs = atoi(values.token(1).c_str());
		}
		else if (values.token(0) == "vocabSize") {
			vocabSize = atoi(values.token(1).c_str());
		}
		if (numSentiLabs > 0 && numTopics > 0 && numDocs > 0 && vocabSize > 0) {
			break;
		}
	}

	fclose(fin);



	if (numSentiLabs == 0 || numTopics == 0 || numDocs == 0 || vocabSize == 0) {
		cout << "Throw exception in reading model parameter settings!\n" << filename << endl;
		return 1;
	}


	return 0;
}

// read '.tassign' file of previously trained model
int JST_inference::load_model(string filename) {

    char buff[BUFF_SIZE_LONG];
	string line;

    FILE * fin = fopen(filename.c_str(), "r");
    if (!fin) {
	    printf("Cannot read file %s!\n", filename.c_str());
	    return 1;
    }

	ptrndata->docs = new document*[numDocs];
	ptrndata->vocabSize= vocabSize;
	ptrndata->numDocs= numDocs;
	l.resize(ptrndata->numDocs);
	z.resize(ptrndata->numDocs);

    for (int m = 0; m < numDocs; m++) {
		fgets(buff, BUFF_SIZE_LONG - 1, fin);  // first line - ignore the document ID
		fgets(buff, BUFF_SIZE_LONG - 1, fin);  // second line - read the sentiment label / topic assignments
		line = buff;
	    strtokenizer strtok(line, " \t\r\n");
	    int length = strtok.count_tokens();

	    vector<int> words;
		vector<int> sentiLabs;
	    vector<int> topics;

	    for (int j = 0; j < length; j++) {
	        string token = strtok.token(j);
	        strtokenizer tok(token, ":");
	        if (tok.count_tokens() != 3) {
		        if (j != 0){
                    printf("Invalid word-topic assignment line!\n");
                    return 1;
                }
                continue;
	        }

	        words.push_back(atoi(tok.token(0).c_str()));
			sentiLabs.push_back(atoi(tok.token(1).c_str()));
	        topics.push_back(atoi(tok.token(2).c_str()));
	    }

		// allocate and add training document to the corpus
		document * pdoc = new document(words);
		ptrndata->add_doc(pdoc, m);

		l[m].resize(sentiLabs.size());
		for (int j = 0; j < (int)sentiLabs.size(); j++) {
			l[m][j] = sentiLabs[j];
		}

		z[m].resize(topics.size());
		for (int j = 0; j < (int)topics.size(); j++) {
			z[m][j] = topics[j];
		}
	}
    fclose(fin);

	// init model counts
	nlzw.resize(numSentiLabs);
	for (int l = 0; l < numSentiLabs; l++) {
		nlzw[l].resize(numTopics);
		for (int z = 0; z < numTopics; z++) {
			nlzw[l][z].resize(vocabSize);
			for (int r = 0; r < vocabSize; r++) {
			    nlzw[l][z][r] = 0;
			}
		}
	}

	nlz.resize(numSentiLabs);
	for (int l = 0; l < numSentiLabs; l++) {
		nlz[l].resize(numTopics);
		for (int z = 0; z < numTopics; z++) {
            nlz[l][z] = 0;
		}
	}

	// recover count values from trained model
	for (int m = 0; m < ptrndata->numDocs; m++) {
		int docLength = ptrndata->docs[m]->length;
		for (int n = 0; n < docLength; n++) {
			int w = ptrndata->docs[m]->words[n];
			int sentiLab = this->l[m][n];
			int topic = this->z[m][n];
			nlzw[sentiLab][topic][w]++;
			nlz[sentiLab][topic]++;
		}
	}

    return 0;
}

int JST_inference::init_parameters() {

	// model counts
	new_p.resize(numSentiLabs);
	for (int l = 0; l < numSentiLabs; l++) 	{
		new_p[l].resize(numTopics);
		for (int z = 0; z < numTopics; z++) {
		    new_p[l][z] = 0.0;
		}
	}

	new_nd.resize(ptestdata->numDocs);
	for (int m = 0; m < ptestdata->numDocs; m++) {
	    new_nd[m] = 0;
	}

	new_ndl.resize(ptestdata->numDocs);
	for (int m = 0; m < ptestdata->numDocs; m++) {
		new_ndl[m].resize(numSentiLabs);
		for (int l = 0; l < numSentiLabs; l++) {
		    new_ndl[m][l] = 0;
		}
	}

	new_ndlz.resize(ptestdata->numDocs);
	for (int m = 0; m < ptestdata->numDocs; m++) {
		new_ndlz[m].resize(numSentiLabs);
	    for (int l = 0; l < numSentiLabs; l++)	{
			new_ndlz[m][l].resize(numTopics);
			for (int z = 0; z < numTopics; z++) {
			    new_ndlz[m][l][z] = 0;
			}
		}
	}

	new_nlzw.resize(numSentiLabs);
	for (int l = 0; l < numSentiLabs; l++) {
		new_nlzw[l].resize(numTopics);
		for (int z = 0; z < numTopics; z++) {
			new_nlzw[l][z].resize(ptestdata->vocabSize);
			for (int r = 0; r < ptestdata->vocabSize; r++) {
			    new_nlzw[l][z][r] = 0;
			}
		}
	}

	new_nlz.resize(numSentiLabs);
	for (int l = 0; l < numSentiLabs; l++) {
		new_nlz[l].resize(numTopics);
		for (int z = 0; z < numTopics; z++) {
		    new_nlz[l][z] = 0;
		}
	}

	// model parameters
	newpi_dl.resize(ptestdata->numDocs);
	for (int m = 0; m < ptestdata->numDocs; m++) {
		newpi_dl[m].resize(numSentiLabs);
	}

	newtheta_dlz.resize(ptestdata->numDocs);
	for (int m = 0; m < ptestdata->numDocs; m++) {
		newtheta_dlz[m].resize(numSentiLabs);
		for (int l = 0; l < numSentiLabs; l++) {
			newtheta_dlz[m][l].resize(numTopics);
		}
	}

	newphi_lzw.resize(numSentiLabs);
	for (int l = 0; l < numSentiLabs; l++) {
		newphi_lzw[l].resize(numTopics);
		for (int z = 0; z < numTopics; z++) {
			newphi_lzw[l][z].resize(ptestdata->vocabSize);
		}
	}


	// hyperparameters
	_alpha =  (double)ptestdata->aveDocLength * 0.05 / (double)(numSentiLabs * numTopics);
	alpha_lz.resize(numSentiLabs);
	alphaSum_l.resize(numSentiLabs);
	for (int l = 0; l < numSentiLabs; l++) {
		alphaSum_l[l] = 0.0;
		alpha_lz[l].resize(numTopics);
		for (int z = 0; z < numTopics; z++) {
			alpha_lz[l][z] = _alpha;
			alphaSum_l[l] += alpha_lz[l][z];
		}
	}

	// gamma
	gamma_l.resize(numSentiLabs);
	gammaSum = 0.0;
	for (int l = 0; l < numSentiLabs; l++) {
		gamma_l[l] = (double)ptestdata->aveDocLength * 0.05 / (double)numSentiLabs;
		gammaSum += gamma_l[l];
	}

	//beta
	if (_beta <= 0) {
		_beta = 0.01;
	}
	beta_lzw.resize(numSentiLabs);
	betaSum_lz.resize(numSentiLabs);
	for (int l = 0; l < numSentiLabs; l++) {
		beta_lzw[l].resize(numTopics);
		betaSum_lz[l].resize(numTopics);
		for (int z = 0; z < numTopics; z++) {
			beta_lzw[l][z].resize(ptestdata->vocabSize);
			for (int r = 0; r < ptestdata->vocabSize; r++) {
				beta_lzw[l][z][r] = _beta;
				betaSum_lz[l][z] += beta_lzw[l][z][r];
			}
		}
	}

	//logFile->write_to_log("dddd\n");


	// incorporate prior knowledge into beta
	if (senti_lex_file != "") {
		// word prior transformation matrix
		lambda_lw.resize(numSentiLabs);
		for (int l = 0; l < numSentiLabs; l++) {
		  lambda_lw[l].resize(ptestdata->vocabSize);
			for (int r = 0; r < ptestdata->vocabSize; r++)
				lambda_lw[l][r] = 1;
		}
		// MUST init beta_lzw first before incorporating prior information into beta
		this->prior2beta();
	}



	return 0;
}

int JST_inference::prior2beta() {

    //logFile->write_to_log("llll\n");

	mapwordid2prior::iterator wordid2priorIt;
	for (wordid2priorIt = this->senLex.wordid2senLabelDis.begin(); wordid2priorIt != this->senLex.wordid2senLabelDis.end(); wordid2priorIt++) {
		int wordID = wordid2priorIt->first;
        for (int j = 0; j < numSentiLabs; j++)  {
            lambda_lw[j][wordID] = wordid2priorIt->second.labDist[j];
        }
    }

    //logFile->write_to_log("eeellll\n");

	for (int l = 0; l < numSentiLabs; l++) {
		for (int z = 0; z < numTopics; z++) {
			betaSum_lz[l][z] = 0.0;
		    for (int r = 0; r < ptestdata->vocabSize; r++) {
			    beta_lzw[l][z][r] = beta_lzw[l][z][r] * lambda_lw[l][r];
			    betaSum_lz[l][z] += beta_lzw[l][z][r];
		    }
		}
	}

	//logFile->write_to_log("mmmmeeellll\n");

	return 0;
}


int JST_inference::init_inf() {

    cout<<"init_inf() begin.....\n";

	ptrndata = new dataset();
	ptestdata = new dataset();

	if(read_model_setting(dir + save_model_name + ".others")) {
	    logFile->write_to_log("Throw exception in read_para_setting()!\n","error");
		return 1;
	}

	// load model
	if(load_model(dir + save_model_name + ".tassign")) {
	    logFile->write_to_log("Throw exception in load_model()!\n","error");
		return 1;
	}

    if(ptestdata->read_testdata(this->data_file,this->dir + this->wordmapfile)) {
		logFile->write_to_log("Throw exception in function read_testdata()! \n","error");
		delete ptestdata;
		return 1;
	}

	if (twords > 0)
        dataset::read_wordmap(dir + wordmapfile, &id2word);


	if (this->senti_lex_file != "") {
        if (this->senLex.read_senti_lexicon(this->senti_lex_file)){
            // Add non sentiment word prior.
            this->senLex.load_non_senti_word_prior(&this->ptrndata->word2id_train);
            this->senLex.get_wordid2senLabelDis(&this->ptrndata->word2id_train);
        }
	}


	if(init_parameters()) {
	    logFile->write_to_log("Throw exception in init_parameters!\n","error");
		return 1;
	}


	print_out_model_para();


	// init inf
	int sentiLab, topic;
	new_z.resize(ptestdata->numDocs);
	new_l.resize(ptestdata->numDocs);

	for (int m = 0; m < ptestdata->numDocs; m++) {
		int docLength = ptestdata->_docs[m]->length;
		new_z[m].resize(docLength);
		new_l[m].resize(docLength);
		for (int t = 0; t < docLength; t++) {

		    if (ptestdata->_docs[m]->words[t] < 0) {
                string word_token = logFile->convert_other_to_str(ptestdata->docs[m]->words[t]);
                string m_str = logFile->convert_other_to_str(m);
                string t_str = logFile->convert_other_to_str(t);
                string temp_str = "ERROE! word token " +  word_token + " has index smaller than 0 at doc[" + m_str + "][" + t_str + "]\n";
			    logFile->write_to_log(temp_str,"error");
			    return 1;
			}

			int priorSentiLabel = this->senLex.get_word_senlabel(ptestdata->docs[m]->words[t]);

    	    if ((priorSentiLabel > -1) && (priorSentiLabel < numSentiLabs)) {
			    sentiLab = priorSentiLabel; // incorporate prior information into the model

			}
			else {
			    sentiLab = (int)(((double)rand() / RAND_MAX) * numSentiLabs);
			    if (sentiLab == numSentiLabs) sentiLab = numSentiLabs -1;  // to avoid over array boundary
			}

		    new_l[m][t] = sentiLab;


			// sample topic label
			topic = (int)(((double)rand() / RAND_MAX) * numTopics);
			if (topic == numTopics)  topic = numTopics - 1;
			new_z[m][t] = topic;


			new_nd[m]++;
			new_ndl[m][sentiLab]++;
			new_ndlz[m][sentiLab][topic]++;
			new_nlzw[sentiLab][topic][ptestdata->_docs[m]->words[t]]++;
			new_nlz[sentiLab][topic]++;

       }
	}


	cout<<"init_inf() end.....\n";

	return 0;
}






