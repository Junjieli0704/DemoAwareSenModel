#include "USTM_FT_W.h"

USTM_FT_W::USTM_FT_W(){

    wordmapfile = "wordmap.txt";
    demomapfile = "demomap.txt";
	tassign_suffix = ".tassign";
	pi_suffix = ".pi";
	theta_suffix = ".theta";
	phi_suffix = ".phi";
	others_suffix = ".others";
	twords_suffix = ".twords";
    psi_suffix = ".psi";
	eta_suffix = ".eta";

	num_topics = 50;
	num_sentis = 3;
	num_vocabs = 0;
	num_docs = 0;
	num_corpus = 0;
	ave_doc_length = 0;

	niters = 100;
	twords = 20;

	_alpha  = -1.0;
	_beta = -1.0;
	_gamma = -1.0;


}

USTM_FT_W::~USTM_FT_W()
{
    //dtor
}


int USTM_FT_W::init_para(Model_Para* model_para){

    log_file->write_to_log("USTM_FT_W::init_para begin......\n");

    this->model_status = model_para->model_status;

    this->save_model_name = model_para->save_model_name;

    this->dir = model_para->dir;

    if (model_para->data_file == "") {
        log_file->write_to_log("Please specify the input data file for model estimation!\n","error");
        return 1;
    }
    else {this->data_file = model_para->data_file;}

    if (model_para->data_demo_file == "") {
        log_file->write_to_log("Please specify the input data demographics file for model estimation!\n","error");
        return 1;
    }
    else {this->data_demo_file = model_para->data_demo_file;}


    if (model_para->senti_lex_file == "") {
        log_file->write_to_log("Please specify the sentiment lexicon file for model estimation!\n","error");
        return 1;
    }
    else {this->senti_lex_file = model_para->senti_lex_file;}

    if (model_para->numTopics >= 0.0){
        this->num_topics = model_para->numTopics;
    }

    if (model_para->numSentis >= 0.0){
        this->num_sentis = model_para->numSentis;
    }

    // Initial alpha beta gamma
    if (model_para->alpha >= 0.0){
        this->_alpha = model_para->alpha;
    }
    else{this->_alpha = 50.0 / this->num_topics; }

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

    if (model_para->demomapfile != "") {
        this->demomapfile = model_para->demomapfile;
    }

    log_file->write_to_log("USTM_FT_W::init_para end......\n");

    return 0;

}

void USTM_FT_W::print_out_model_para(){

    if (this->model_status == MODEL_STATUS_EST){

        log_file->write_to_log("************** Model_Para for USTM_FT_W Training***************\n");
        log_file->write_to_log("model_type      --> USTM_FT_W\n");
        log_file->write_to_log("model_task      --> est\n");
        log_file->write_to_log("save_model_name --> " + this->save_model_name + "\n");
        log_file->write_to_log("dir             --> " + this->dir + "\n");
        log_file->write_to_log("data_file       --> " + this->data_file + "\n");
        log_file->write_to_log("data_demo_file  --> " + this->data_demo_file + "\n");
        log_file->write_to_log("senti_lex_file  --> " + this->senti_lex_file + "\n");
        log_file->write_to_log("alpha           --> " + log_file->convert_other_to_str(this->_alpha) + "\n");
        log_file->write_to_log("beta            --> " + log_file->convert_other_to_str(this->_beta) + "\n");
        log_file->write_to_log("gamma           --> " + log_file->convert_other_to_str(this->_gamma) + "\n");
        log_file->write_to_log("num_topics      --> " + log_file->convert_other_to_str(this->num_topics) + "\n");
        log_file->write_to_log("num_sentis      --> " + log_file->convert_other_to_str(this->num_sentis) + "\n");
        log_file->write_to_log("niters          --> " + log_file->convert_other_to_str(this->niters) + "\n");
        log_file->write_to_log("wordmapfile     --> " + this->wordmapfile + "\n");
        log_file->write_to_log("demomapfile     --> " + this->demomapfile + "\n");
        log_file->write_to_log("*********************************************************\n\n\n");

        log_file->write_to_log("************** Data_Para ********************************\n");
        log_file->write_to_log("numDocs         --> " + log_file->convert_other_to_str(this->ptrndata->numDocs) + "\n");
        log_file->write_to_log("vocabSize       --> " + log_file->convert_other_to_str(this->ptrndata->vocabSize) + "\n");
        log_file->write_to_log("demoSize        --> " + log_file->convert_other_to_str(this->ptrndemodata->vocabSize) + "\n");
        log_file->write_to_log("corpusSize      --> " + log_file->convert_other_to_str(this->ptrndata->corpusSize) + "\n");
        log_file->write_to_log("averDocLen      --> " + log_file->convert_other_to_str(this->ptrndata->aveDocLength) + "\n");
        log_file->write_to_log("*********************************************************\n\n\n");
    }

    if (this->model_status == MODEL_STATUS_INF){

        log_file->write_to_log("************** Model_Para for USTM_FT_W Testing***************\n");
        log_file->write_to_log("model_type      --> USTM_FT_W\n");
        log_file->write_to_log("model_task      --> inf\n");
        log_file->write_to_log("save_model_name --> " + this->save_model_name + "\n");
        log_file->write_to_log("dir             --> " + this->dir + "\n");
        log_file->write_to_log("data_file       --> " + this->data_file + "\n");
        log_file->write_to_log("data_demo_file  --> " + this->data_demo_file + "\n");
        log_file->write_to_log("senti_lex_file  --> " + this->senti_lex_file + "\n");
        log_file->write_to_log("alpha           --> " + log_file->convert_other_to_str(this->_alpha) + "\n");
        log_file->write_to_log("beta            --> " + log_file->convert_other_to_str(this->_beta) + "\n");
        log_file->write_to_log("gamma           --> " + log_file->convert_other_to_str(this->_gamma) + "\n");
        log_file->write_to_log("num_topics      --> " + log_file->convert_other_to_str(this->num_topics) + "\n");
        log_file->write_to_log("num_sentis      --> " + log_file->convert_other_to_str(this->num_sentis) + "\n");
        log_file->write_to_log("niters          --> " + log_file->convert_other_to_str(this->niters) + "\n");
        log_file->write_to_log("wordmapfile     --> " + this->wordmapfile + "\n");
        log_file->write_to_log("demomapfile     --> " + this->demomapfile + "\n");
        log_file->write_to_log("*********************************************************\n\n\n");

        log_file->write_to_log("************** Data_Para ********************************\n");
        log_file->write_to_log("numDocs         --> " + log_file->convert_other_to_str(this->ptestdata->numDocs) + "\n");
        log_file->write_to_log("vocabSize       --> " + log_file->convert_other_to_str(this->ptestdata->vocabSize) + "\n");
        log_file->write_to_log("demoSize        --> " + log_file->convert_other_to_str(this->ptestdemodata->vocabSize) + "\n");
        log_file->write_to_log("corpusSize      --> " + log_file->convert_other_to_str(this->ptestdata->corpusSize) + "\n");
        log_file->write_to_log("averDocLen      --> " + log_file->convert_other_to_str(this->ptestdata->aveDocLength) + "\n");
        log_file->write_to_log("*********************************************************\n\n\n");
    }
}

int USTM_FT_W::init_model_parameters()
{

    log_file->write_to_log("init_model_parameters begin.....\n");

    if (this->model_status == MODEL_STATUS_EST){
        num_corpus = ptrndata->corpusSize;
        ave_doc_length = ptrndata->aveDocLength;
        num_docs = ptrndata->numDocs;
        num_vocabs = ptrndata->vocabSize;
        num_demos = ptrndemodata->vocabSize;
    }

    if (this->model_status == MODEL_STATUS_INF){
        num_corpus = ptestdata->corpusSize;
        ave_doc_length = ptestdata->aveDocLength;
        num_docs = ptestdata->numDocs;
        num_vocabs = ptestdata->vocabSize;
        num_demos = ptestdemodata->vocabSize;
    }

    //Model Count
    utils::alloc_space(n_doooo,num_docs);
    utils::alloc_space(n_djooo,num_docs,num_demos);
    utils::alloc_space(n_djkoo,num_docs,num_demos,num_topics);
    utils::alloc_space(n_ojkow,num_demos,num_topics,num_vocabs);
    utils::alloc_space(n_ojkoo,num_demos,num_topics);
    utils::alloc_space(n_djkso,num_docs,num_demos,num_topics,num_sentis);
    utils::alloc_space(n_ojksw,num_demos,num_topics,num_sentis,num_vocabs);
    utils::alloc_space(n_ojkso,num_demos,num_topics,num_sentis);


    //topic and label assignments
    utils::alloc_space(p_ojkso,num_demos,num_topics,num_sentis);

    // hyperparameters
    utils::alloc_space(beta_ooosw,num_sentis,num_vocabs);
    utils::alloc_space(beta_oooso,num_sentis);

    // model parameters
    utils::alloc_space(theta_djkoo,num_docs,num_demos,num_topics);
    utils::alloc_space(phi_ojksw,num_demos,num_topics,num_sentis,num_vocabs);
    utils::alloc_space(eta_djkso,num_docs,num_demos,num_topics,num_sentis);
    utils::alloc_space(psi_djooo,num_docs,num_demos);

   	// incorporate prior information into beta
	this->prior2beta();

	log_file->write_to_log("init_model_parameters end.....\n");

	return 0;
}

int USTM_FT_W::prior2beta() {


    for(int i = 0;i < num_sentis; i++){
        for (int j = 0; j < num_vocabs; j++){
            beta_ooosw[i][j] = _beta;
        }
    }
	mapwordid2prior::iterator wordid2priorIt;


    if (this->model_status == MODEL_STATUS_EST){
        for (wordid2priorIt = this->senLex.wordid2senLabelDis.begin(); wordid2priorIt != this->senLex.wordid2senLabelDis.end(); wordid2priorIt++) {
            int wordID = wordid2priorIt->first;
            for (int j = 0; j < num_sentis; j++)  {
                beta_ooosw[j][wordID] = wordid2priorIt->second.labDist[j];
                beta_oooso[j] += beta_ooosw[j][wordID];
            }
        }
    }

    /*
    if (this->model_status == MODEL_STATUS_INF){
        for (wordid2priorIt = this->senLex.wordid2senLabelDis.begin(); wordid2priorIt != this->senLex.wordid2senLabelDis.end(); wordid2priorIt++) {
            int wordID = wordid2priorIt->first;
            int _wordid = ptestdata->changeid2_id(wordID);
            for (int j = 0; j < num_sentis; j++)  {
                beta_ooosw[j][_wordid] = wordid2priorIt->second.labDist[j];
                beta_oooso[j] += beta_ooosw[j][_wordid];
            }
        }
    }*/

	return 0;
}

void USTM_FT_W::delete_model_parameters(){

    if (this->model_status == MODEL_STATUS_INF){
        utils::release_space(n_ojkow_train,ptrndemodata->vocabSize,num_topics);
        utils::release_space(n_ojkoo_train,ptrndemodata->vocabSize);
        utils::release_space(n_ojksw_train,ptrndemodata->vocabSize,num_topics,num_sentis);
        utils::release_space(n_ojkso_train,ptrndemodata->vocabSize,num_topics);
    }

    utils::release_space(n_doooo);
    utils::release_space(n_djooo,num_docs);
    utils::release_space(n_djkoo,num_docs,num_demos);
    utils::release_space(n_ojkow,num_demos,num_topics);
    utils::release_space(n_ojkoo,num_demos);
    utils::release_space(n_djkso,num_docs,num_demos,num_topics);
    utils::release_space(n_ojksw,num_demos,num_topics,num_sentis);
    utils::release_space(n_ojkso,num_demos,num_topics);


    //topic and label assignments
    utils::release_space(p_ojkso,num_demos,num_topics);

    // hyperparameters
    utils::release_space(beta_ooosw,num_sentis);
    utils::release_space(beta_oooso);

    // model parameters
    utils::release_space(theta_djkoo,num_docs,num_demos);
    utils::release_space(phi_ojksw,num_demos,num_topics,num_sentis);
    utils::release_space(eta_djkso,num_docs,num_demos,num_topics);
    utils::release_space(psi_djooo,num_docs);

}


int USTM_FT_W::init_estimate() {

    cout<<"USTM_FT_W::init_estimate() begin......"<<endl;

    int is_need_print_para = 0;


    int sentiLab, topic, tag;

	srand(time(0)); // initialize for random number generation

    t_dooow = new int* [num_docs];
    z_dooow = new int* [num_docs];
    s_dooow = new int* [num_docs];

	for (int m = 0; m < num_docs; m++) {
		int doc_length = ptrndata->docs[m]->length;

		t_dooow[m] = new int[doc_length];
		s_dooow[m] = new int[doc_length];
		z_dooow[m] = new int[doc_length];


        for (int n = 0; n < doc_length; n++) {
            if (is_need_print_para) cout<<"m: "<<m<<"   n: "<<n<<endl;

            int w_id = ptrndata->docs[m]->words[n];


		    if (w_id < 0) {
		        string word_token = log_file->convert_other_to_str(w_id);
                string m_str = log_file->convert_other_to_str(m);
                string w_str = log_file->convert_other_to_str(n);
                string temp_str = "ERROE! word token " +  word_token + " has index smaller than 0 at doc[" + m_str + "][" + w_str + "]\n";
			    log_file->write_to_log(temp_str,"error");
				return 1;
			}


			int priorSentiLabel = this->senLex.get_word_senlabel(w_id);

    	    if ((priorSentiLabel > -1) && (priorSentiLabel < num_sentis)) {
			    sentiLab = priorSentiLabel; // incorporate prior information into the model

			}
			else {
			    sentiLab = (int)(((double)rand() / RAND_MAX) * num_sentis);
			    if (sentiLab == num_sentis) sentiLab = num_sentis -1;  // to avoid over array boundary
			}
    	    s_dooow[m][n] = sentiLab;



    	    if (is_need_print_para) cout<<"s_dooow[m][n]: "<<s_dooow[m][n]<<endl;

			// random initialize the topic assginment
			topic = (int)(((double)rand() / RAND_MAX) * num_topics);
			if (topic == num_topics)  topic = num_topics - 1; // to avoid over array boundary
			z_dooow[m][n] = topic;
			if (is_need_print_para) cout<<"z_dooow[m][n]: "<<z_dooow[m][n]<<endl;

			int doc_tag_size = ptrndemodata->docs[m]->length;
			int tag_place = (int)(((double)rand() / RAND_MAX) * doc_tag_size);
			if (tag_place == doc_tag_size)  tag_place = doc_tag_size - 1; // to avoid over array boundary

            tag = ptrndemodata->docs[m]->words[tag_place];
			t_dooow[m][n] = tag;
			if (is_need_print_para) cout<<"t_dooow[m][n]: "<<t_dooow[m][n]<<endl;

            // model count assignments
            // j -> tag, k -> topic, s -> sentiLab, d -> m, w -> w_id;
            n_doooo[m]++;
            if (is_need_print_para) cout<<"n_doooo[m]: "<<n_doooo[m]<<endl;

            n_djooo[m][tag]++;
            if (is_need_print_para) cout<<"n_djooo[m][tag]: "<<n_djooo[m][tag]<<endl;

            n_djkoo[m][tag][topic]++;
            if (is_need_print_para) cout<<"n_djkoo[m][tag][topic]: "<<n_djkoo[m][tag][topic]<<endl;

            n_ojkow[tag][topic][w_id]++;
            if (is_need_print_para) cout<<"n_ojkow[tag][topic][w_id]: "<<n_ojkow[tag][topic][w_id]<<endl;

            n_ojkoo[tag][topic]++;
            if (is_need_print_para) cout<<"n_ojkoo[tag][topic]: "<<n_ojkoo[tag][topic]<<endl;

            n_djkso[m][tag][topic][sentiLab]++;
            if (is_need_print_para) cout<<"n_djkso[m][tag][topic][sentiLab]: "<<n_djkso[m][tag][topic][sentiLab]<<endl;

            n_ojksw[tag][topic][sentiLab][w_id]++;
            if (is_need_print_para) cout<<"n_ojksw[tag][topic][sentiLab][w_id]: "<<n_ojksw[tag][topic][sentiLab][w_id]<<endl;

            n_ojkso[tag][topic][sentiLab]++;
            if (is_need_print_para) cout<<"n_ojkso[tag][topic][sentiLab]: "<<n_ojkso[tag][topic][sentiLab]<<endl;
        }
    }

    cout<<"USTM_FT_W::init_estimate() end......"<<endl;

    return 0;
}


int USTM_FT_W::init_inf() {

    /*

    cout<<"USTM_FT_W::init_inf() begin......"<<endl;

    int is_need_print_para = 0;


    int sentiLab, topic, tag;

	srand(time(0)); // initialize for random number generation

    t_dooow = new int* [num_docs];
    z_dooow = new int* [num_docs];
    s_dooow = new int* [num_docs];

	for (int m = 0; m < num_docs; m++) {
		int doc_length = ptestdata->docs[m]->length;

		t_dooow[m] = new int[doc_length];
		s_dooow[m] = new int[doc_length];
		z_dooow[m] = new int[doc_length];


        for (int n = 0; n < doc_length; n++) {
            if (is_need_print_para) cout<<"m: "<<m<<"   n: "<<n<<endl;

            int w = ptestdata->docs[m]->words[n];
            int _w = ptestdata->_docs[m]->words[n];

            if (is_need_print_para) cout<<"w: "<<w<<"   _w: "<<_w<<endl;

			int priorSentiLabel = this->senLex.get_word_senlabel(w);

    	    if ((priorSentiLabel > -1) && (priorSentiLabel < num_sentis)) {
			    sentiLab = priorSentiLabel; // incorporate prior information into the model

			}
			else {
			    sentiLab = (int)(((double)rand() / RAND_MAX) * num_sentis);
			    if (sentiLab == num_sentis) sentiLab = num_sentis -1;  // to avoid over array boundary
			}
    	    s_dooow[m][n] = sentiLab;
    	    if (is_need_print_para) cout<<"s_dooow["<<m<<"]["<<n<<"]: "<<s_dooow[m][n]<<endl;

			// random initialize the topic assginment
			topic = (int)(((double)rand() / RAND_MAX) * num_topics);
			if (topic == num_topics)  topic = num_topics - 1; // to avoid over array boundary
			z_dooow[m][n] = topic;
			if (is_need_print_para) cout<<"z_dooow["<<m<<"]["<<n<<"]: "<<z_dooow[m][n]<<endl;



			int doc_tag_size = ptestdemodata->_docs[m]->length;
			int tag_place = (int)(((double)rand() / RAND_MAX) * doc_tag_size);
			if (tag_place == doc_tag_size)  tag_place = doc_tag_size - 1; // to avoid over array boundary

            tag = ptestdemodata->_docs[m]->words[tag_place];
			t_dooow[m][n] = tag;
			if (is_need_print_para) cout<<"t_dooow["<<m<<"]["<<n<<"]: "<<t_dooow[m][n]<<endl;

            // model count assignments
            // j -> tag, k -> topic, s -> sentiLab, d -> m, w -> w_id;
            n_doooo[m]++;
            if (is_need_print_para) cout<<"n_doooo["<<m<<"]: "<<n_doooo[m]<<endl;

            n_djooo[m][tag]++;
            if (is_need_print_para) cout<<"n_djooo["<<m<<"]["<<tag<<"]: "<<n_djooo[m][tag]<<endl;

            n_djkoo[m][tag][topic]++;
            if (is_need_print_para) cout<<"n_djkoo["<<m<<"]["<<tag<<"]["<<topic<<"]: "<<n_djkoo[m][tag][topic]<<endl;

            n_ojkow[tag][topic][_w]++;
            if (is_need_print_para) cout<<"n_ojkow["<<tag<<"]["<<topic<<"]["<<_w<<"]: "<<n_ojkow[tag][topic][_w]<<endl;

            n_ojkoo[tag][topic]++;
            if (is_need_print_para) cout<<"n_ojkoo["<<tag<<"]["<<topic<<"]: "<<n_ojkoo[tag][topic]<<endl;

            n_djkso[m][tag][topic][sentiLab]++;
            if (is_need_print_para) cout<<"n_djkso["<<m<<"]["<<tag<<"]["<<topic<<"]["<<sentiLab<<"]: "<<n_djkso[m][tag][topic][sentiLab]<<endl;

            n_ojksw[tag][topic][sentiLab][_w]++;
            if (is_need_print_para) cout<<"n_ojksw["<<tag<<"]["<<topic<<"]["<<sentiLab<<"]["<<_w<<"]: "<<n_ojksw[tag][topic][sentiLab][_w]<<endl;

            n_ojkso[tag][topic][sentiLab]++;
            if (is_need_print_para) cout<<"n_ojkso["<<tag<<"]["<<topic<<"]["<<sentiLab<<"]: "<<n_ojkso[tag][topic][sentiLab]<<endl;
        }
    }

    cout<<"USTM_FT_W::init_inf() end......"<<endl;
    */
    return 0;
}



int USTM_FT_W::inf_sampling(int m, int w, int& sentiLab, int& topic, int &tag) {


    /*
    //log_file->write_to_log("USTM_FT_W::inf_sampling()  begin......\n");

	sentiLab = s_dooow[m][w];
    topic    = z_dooow[m][w];
    tag      = t_dooow[m][w];

    int w_id = ptestdata->_docs[m]->words[w];

    //cout<<"sentiLab: "<<sentiLab<<endl;
    //cout<<"topic: "<<topic<<endl;
    //cout<<"tag: "<<tag<<endl;


    double u;

	n_doooo[m]--;
	n_djooo[m][tag]--;
	n_djkoo[m][tag][topic]--;
	n_ojkow[tag][topic][w_id]--;
	n_ojkoo[tag][topic]--;
	n_djkso[m][tag][topic][sentiLab]--;
	n_ojksw[tag][topic][sentiLab][w_id]--;
	n_ojkso[tag][topic][sentiLab]--;


	// j -> tag, k -> topic, s -> sentiLab, d -> m, w -> w_id;

	for (int t = 0; t < num_demos; t++){
        //cout<<"t: "<<t<<endl;
        if (ptestdemodata->_docs[m]->is_contain_word(t) == 0){
            for (int l = 0; l < num_sentis; l++)
                for (int k = 0; k < num_topics; k++)
                    p_ojkso[t][k][l] = 0.0;
        }
        else{
            for (int l = 0; l < num_sentis; l++){
                for (int k = 0; k < num_topics; k++){
                    //cout<<"l: "<<l<<"k: "<<k<<endl;
                    p_ojkso[t][k][l] = (n_djkoo[m][t][k] + _alpha) / (n_doooo[m] + _alpha * num_topics * ptestdemodata->docs[m]->length) *
                                       //(n_ojkow[t][k][w_id] + _beta) / (n_ojkoo[t][k] + _beta * num_vocabs) *
                                       (n_djkso[m][t][k][l] + _gamma) / (n_djkoo[m][t][k] + num_sentis * _gamma) *
                                       (n_ojksw[t][k][l][w_id] + beta_ooosw[l][w_id]) / (n_ojkso[t][k][l] + beta_oooso[l]);
                }
            }
        }
    }





    // for (int t = 0; t < num_demos; t++)
    // for (int l = 0; l < num_sentis; l++)
    // for (int k = 0; k < num_topics; k++)
    //     cout<<"p_ojkso["<<t<<"]["<<k<<"]["<<l<<"]:  "<<p_ojkso[t][k][l]<<endl;





    for (int t = 0; t < num_demos; t++){
        for (int k = 0; k < num_topics; k++){
            for (int l = 0; l < num_sentis; l++){
                if (l==0){
                    if (k==0){
                        if (t==0) continue;
                        else p_ojkso[t][k][l] += p_ojkso[t-1][num_topics-1][num_sentis-1];
                    }
                    else p_ojkso[t][k][l] += p_ojkso[t][k-1][num_sentis-1];
                }
                else p_ojkso[t][k][l] += p_ojkso[t][k][l-1];
            }
        }
    }

    // probability normalization
	u = ((double)rand() / RAND_MAX) * p_ojkso[num_demos-1][num_topics-1][num_sentis-1];

	for (tag = 0; tag < num_demos; tag++){
        for (topic = 0; topic < num_topics; topic++){
            for (sentiLab = 0; sentiLab < num_sentis; sentiLab++){
                if (p_ojkso[tag][topic][sentiLab] > u)
                    goto stop;
		    }
        }
    }
	stop:
	if (sentiLab == num_sentis) sentiLab = num_sentis - 1; // the max value of label is (S - 1)
	if (topic == num_topics) topic = num_topics - 1;
	if (tag == num_demos) tag = ptestdemodata->_docs[m]->words[0];

	//cout<<"sentiLab: "<<sentiLab<<endl;
	//cout<<"topic: "<<topic<<endl;
	//cout<<"tag: "<<tag<<endl;

    if (ptestdemodata->_docs[m]->is_contain_word(tag) == 0)
        cout<<"Bad Sampling Tag.......\n";


	// add estimated 'z' and 'l' to count variables
	n_doooo[m]++;
	n_djooo[m][tag]++;
	n_djkoo[m][tag][topic]++;
	n_ojkow[tag][topic][w_id]++;
	n_ojkoo[tag][topic]++;
	n_djkso[m][tag][topic][sentiLab]++;
	n_ojksw[tag][topic][sentiLab][w_id]++;
	n_ojkso[tag][topic][sentiLab]++;

	//log_file->write_to_log("USTM_FT_W::inf_sampling()  end......\n");
    */
    return 0;
}


int USTM_FT_W::sampling(int m, int w, int& sentiLab, int& topic, int &tag) {

	sentiLab = s_dooow[m][w];
    topic    = z_dooow[m][w];
    tag      = t_dooow[m][w];

    int w_id = ptrndata->docs[m]->words[w];

    double u;


	n_doooo[m]--;
	n_djooo[m][tag]--;
	n_djkoo[m][tag][topic]--;
	n_ojkow[tag][topic][w_id]--;
	n_ojkoo[tag][topic]--;
	n_djkso[m][tag][topic][sentiLab]--;
	n_ojksw[tag][topic][sentiLab][w_id]--;
	n_ojkso[tag][topic][sentiLab]--;

	// j -> tag, k -> topic, s -> sentiLab, d -> m, w -> w_id;

	for (int t = 0; t < num_demos; t++){
        if (ptrndemodata->docs[m]->is_contain_word(t) == 0){
            for (int l = 0; l < num_sentis; l++)
                for (int k = 0; k < num_topics; k++)
                    p_ojkso[t][k][l] = 0.0;
        }
        else{
            for (int l = 0; l < num_sentis; l++){
                for (int k = 0; k < num_topics; k++){
                    p_ojkso[t][k][l] = (n_djkoo[m][t][k] + _alpha) / (n_doooo[m] + _alpha * num_topics * ptrndemodata->docs[m]->length) *
                                       //(n_ojkow[t][k][w_id] + _beta) / (n_ojkoo[t][k] + _beta * num_vocabs) *
                                       (n_djkso[m][t][k][l] + _gamma) / (n_djkoo[m][t][k] + num_sentis * _gamma) *
                                       (n_ojksw[t][k][l][w_id] + beta_ooosw[l][w_id]) / (n_ojkso[t][k][l] + beta_oooso[l]);
                }
            }
        }
    }
    /*
    for (int t = 0; t < num_demos; t++)
    for (int l = 0; l < num_sentis; l++)
    for (int k = 0; k < num_topics; k++)
        cout<<"p_ojkso["<<t<<"]["<<k<<"]["<<l<<"]:  "<<p_ojkso[t][k][l]<<endl;*/





    for (int t = 0; t < num_demos; t++){
        for (int k = 0; k < num_topics; k++){
            for (int l = 0; l < num_sentis; l++){
                if (l==0){
                    if (k==0){
                        if (t==0) continue;
                        else p_ojkso[t][k][l] += p_ojkso[t-1][num_topics-1][num_sentis-1];
                    }
                    else p_ojkso[t][k][l] += p_ojkso[t][k-1][num_sentis-1];
                }
                else p_ojkso[t][k][l] += p_ojkso[t][k][l-1];
            }
        }
    }

    // probability normalization
	u = ((double)rand() / RAND_MAX) * p_ojkso[num_demos-1][num_topics-1][num_sentis-1];

	for (tag = 0; tag < num_demos; tag++){
        for (topic = 0; topic < num_topics; topic++){
            for (sentiLab = 0; sentiLab < num_sentis; sentiLab++){
                if (p_ojkso[tag][topic][sentiLab] > u)
                    goto stop;
		    }
        }
    }
	stop:
	if (sentiLab == num_sentis) sentiLab = num_sentis - 1; // the max value of label is (S - 1)
	if (topic == num_topics) topic = num_topics - 1;
	if (tag == num_demos) tag = ptrndemodata->docs[m]->words[0];

	//cout<<"sentiLab: "<<sentiLab<<endl;
	//cout<<"topic: "<<topic<<endl;
	//cout<<"tag: "<<tag<<endl;
    if (ptrndemodata->docs[m]->is_contain_word(tag) == 0)
            cout<<"Bad Sampling Tag.......\n";



	// add estimated 'z' and 'l' to count variables
	n_doooo[m]++;
	n_djooo[m][tag]++;
	n_djkoo[m][tag][topic]++;
	n_ojkow[tag][topic][w_id]++;
	n_ojkoo[tag][topic]++;
	n_djkso[m][tag][topic][sentiLab]++;
	n_ojksw[tag][topic][sentiLab][w_id]++;
	n_ojkso[tag][topic][sentiLab]++;

    return 0;
}



void USTM_FT_W::compute_phi_ojksw() {


    if(this->model_status == MODEL_STATUS_EST){
        for (int t = 0; t < num_demos; t++)
            for (int z = 0; z < num_topics; z++)
                for (int s = 0; s < num_sentis; s++)
                    for (int w = 0; w < num_vocabs; w++){
                        phi_ojksw[t][z][s][w] = (n_ojksw[t][z][s][w] + beta_ooosw[s][w]) / (n_ojkso[t][z][s] + beta_oooso[s]);
                    }
    }

    if(this->model_status == MODEL_STATUS_INF){
        /*
        for (int _t = 0; _t < num_demos; _t++)
            for (int z = 0; z < num_topics; z++)
                for (int s = 0; s < num_sentis; s++)
                    for (int _w = 0; _w < num_vocabs; _w++){
                        int w = ptestdata->change_id2id(_w);
                        int t = ptestdemodata->change_id2id(_t);
                        phi_ojksw[_t][z][s][_w] = (n_ojksw[_t][z][s][_w] + n_ojksw_train[t][z][s][w] + beta_ooosw[s][_w]) / (n_ojkso[_t][z][s] + n_ojkso_train[t][z][s] + beta_oooso[s]);
                    }
        */
    }
    /*
    for (int t = 0; t < num_demos; t++)
    for (int z = 0; z < num_topics; z++)
    for (int s = 0; s < num_sentis; s++)
    for (int w = 0; w < num_vocabs; w++)
        cout<<"phi_ojksw["<<t<<"]["<<z<<"]["<<s<<"]["<<w<<"]:  "<<phi_ojksw[t][z][s][w]<<endl;
    */
    //log_file->write_to_log("USTM_FT_W::compute_phi_ojksw() end......\n");

}


void USTM_FT_W::compute_eta_djkso() {

    for (int m = 0; m < num_docs; m++)
	    for (int t = 0; t < num_demos; t++){
            //if (ptrndemodata->docs[m]->is_contain_word(t) == 0)
            //    continue;
            if (this->model_status == MODEL_STATUS_EST)
                if (ptrndemodata->docs[m]->is_contain_word(t) == 0)
                    continue;
            /*if (this->model_status == MODEL_STATUS_INF)
                if (ptestdemodata->_docs[m]->is_contain_word(t) == 0)
                    continue;*/
			for (int z = 0; z < num_topics; z++)
			    for (int s = 0; s < num_sentis; s++)
                    eta_djkso[m][t][z][s] = (n_djkso[m][t][z][s] + _gamma) / (n_djkoo[m][t][z] + num_sentis * _gamma);
        }
    /*
    for (int m = 0; m < num_docs; m++)
    for (int t = 0; t < num_demos; t++)
    for (int z = 0; z < num_topics; z++)
    for (int s = 0; s < num_sentis; s++)
        cout<<"eta_djkso["<<m<<"]["<<t<<"]["<<z<<"]["<<s<<"]:  "<<eta_djkso[m][t][z][s]<<endl;
    */

    //log_file->write_to_log("USTM_FT_W::compute_eta_djkso() end......\n");



}

void USTM_FT_W::compute_theta_djkoo() {

    for (int m = 0; m < num_docs; m++)
       for (int t = 0; t < num_demos; t++){
            if (this->model_status == MODEL_STATUS_EST)
                if (ptrndemodata->docs[m]->is_contain_word(t) == 0)
                    continue;
            /*if (this->model_status == MODEL_STATUS_INF)
                if (ptestdemodata->_docs[m]->is_contain_word(t) == 0)
                    continue;*/
			for (int z = 0; z < num_topics; z++)
                theta_djkoo[m][t][z] = (n_djkoo[m][t][z] + _alpha) / ( n_djooo[m][t] +  num_topics * _alpha);
        }

    /*
    for (int m = 0; m < num_docs; m++)
    for (int t = 0; t < num_demos; t++)
    for (int z = 0; z < num_topics; z++)
        cout<<"theta_djkoo["<<m<<"]["<<t<<"]["<<z<<"]:  "<<theta_djkoo[m][t][z]<<endl;*/

    //log_file->write_to_log("USTM_FT_W::compute_theta_djkoo() end......\n");




}

void USTM_FT_W::compute_psi_djooo() {


    for (int m = 0; m < num_docs; m++)
        for (int t = 0; t < num_demos; t++){
            if (this->model_status == MODEL_STATUS_EST){
                if (ptrndemodata->docs[m]->is_contain_word(t) == 0) psi_djooo[m][t] = 0;
                else psi_djooo[m][t] = (n_djooo[m][t] + _alpha) / ( n_doooo[m] + ptrndemodata->docs[m]->length  * _alpha);
            }
            /*if (this->model_status == MODEL_STATUS_INF){
                if (ptestdemodata->_docs[m]->is_contain_word(t) == 0) psi_djooo[m][t] = 0;
                else psi_djooo[m][t] = (n_djooo[m][t] + _alpha) / ( n_doooo[m] + ptestdemodata->_docs[m]->length  * _alpha);
            }*/
        }
    /*
    for (int m = 0; m < num_docs; m++)
    for (int t = 0; t < num_demos; t++)
        cout<<"psi_djooo["<<m<<"]["<<t<<"]:  "<<psi_djooo[m][t]<<endl;
    */
    //log_file->write_to_log("USTM_FT_W::compute_psi_djooo() end......\n");
}


// Compute Perplexity
double USTM_FT_W::compute_perplexity(){

    //log_file->write_to_log("USTM_FT_W::compute_perplexity() begin......\n");

    compute_theta_djkoo();
    compute_eta_djkso();
    compute_phi_ojksw();
    compute_psi_djooo();

    double N = 0;
    double log_per = 0.0;

    if(this->model_status == MODEL_STATUS_EST){
        for (int m = 0; m < num_docs; m++) {
            for (int n = 0; n < ptrndata->docs[m]->length; n++) {
                //cout<<"m: "<<m<<" n: "<<n<<endl;
                int w = ptrndata->docs[m]->words[n];
                double doc_word_prob = 0;
                for (int t = 0; t < ptrndemodata->docs[m]->length; t++){
                    int tag = ptrndemodata->docs[m]->words[t];
                    for (int senLabel = 0; senLabel < num_sentis; senLabel ++)
                        for (int topic = 0; topic < num_topics; topic ++)
                            doc_word_prob +=  psi_djooo[m][tag] * theta_djkoo[m][tag][topic] * eta_djkso[m][tag][topic][senLabel] * phi_ojksw[tag][topic][senLabel][w];
                }
                //cout<<"doc_word_prob: "<<doc_word_prob<<endl;
                double neg_log_doc_prob = log(doc_word_prob);
                //cout<<"neg_log_doc_prob: "<<neg_log_doc_prob<<endl;
                log_per -= neg_log_doc_prob;
                //cout<<"log_per: "<<log_per<<endl;
            }
            N += ptrndata->docs[m]->length;  //  N += len(doc)
        }
        double plex_value = exp(log_per / N);
        //log_file->write_to_log("USTM_FT_W::compute_perplexity() end......\n");
        return plex_value;
    }


    if(this->model_status == MODEL_STATUS_INF){
        /*
        for (int m = 0; m < num_docs; m++) {
            //cout<<"num_docs: "<<num_docs<<endl;
            for (int n = 0; n < ptestdata->_docs[m]->length; n++) {
                //cout<<"m: "<<m<<" n: "<<n<<endl;
                //cout<<"ptestdata->_docs[m]->length: "<<ptestdata->_docs[m]->length<<endl;
                int w = ptestdata->_docs[m]->words[n];
                double doc_word_prob = 0;
                for (int t = 0; t < ptestdemodata->_docs[m]->length; t++){
                    int tag = ptestdemodata->_docs[m]->words[t];
                    for (int senLabel = 0; senLabel < num_sentis; senLabel ++)
                        for (int topic = 0; topic < num_topics; topic ++){
                            doc_word_prob +=  psi_djooo[m][tag] * theta_djkoo[m][tag][topic] * eta_djkso[m][tag][topic][senLabel] * phi_ojksw[tag][topic][senLabel][w];
                            //cout<<"psi_djooo["<<m<<"]["<<tag<<"]: "<<psi_djooo[m][tag]<<endl;
                            //cout<<"theta_djkoo["<<m<<"]["<<tag<<"]["<<topic<<"]: "<<theta_djkoo[m][tag][topic]<<endl;
                            //cout<<"eta_djkso["<<m<<"]["<<tag<<"]["<<topic<<"]["<<senLabel<<"]: "<<eta_djkso[m][tag][topic][senLabel]<<endl;
                            //cout<<"phi_ojksw["<<tag<<"]["<<topic<<"]["<<senLabel<<"]["<<w<<"]: "<<phi_ojksw[tag][topic][senLabel][w]<<endl;
                        }
                }
                //cout<<"doc_word_prob: "<<doc_word_prob<<endl;
                double neg_log_doc_prob = log(doc_word_prob);
                //cout<<"neg_log_doc_prob: "<<neg_log_doc_prob<<endl;
                log_per -= neg_log_doc_prob;
                //cout<<"log_per: "<<log_per<<endl;
            }
            N += ptestdata->_docs[m]->length;  //  N += len(doc)
        }
        double plex_value = exp(log_per / N);
        //log_file->write_to_log("USTM_FT_W::compute_perplexity() end......\n");
        return plex_value;*/

    }






}





int USTM_FT_W::estimate() {

	int sentiLab, topic, tag;

    log_file->write_to_log("Iteration 0 --> perplexity: " + log_file->convert_other_to_str(compute_perplexity())+ "\n");
	log_file->write_to_log("Sampling " + log_file->convert_other_to_str(niters) + " iterations!\n");

	//printf("Sampling %d iterations!\n", niters);
	for (int liter = 1; liter <= niters; liter++) {
        //printf("Iteration %d --> ...\n", liter);
		for (int m = 0; m < num_docs; m++) {
		    for (int w = 0; w < ptrndata->docs[m]->length; w++) {
				sampling(m, w, sentiLab, topic, tag);
				s_dooow[m][w] = sentiLab;
                z_dooow[m][w] = topic;
                t_dooow[m][w] = tag;
            }
		}
        string iter_str = log_file->convert_other_to_str(liter);
        string perplex_str = log_file->convert_other_to_str(compute_perplexity());
        log_file->write_to_log("Iteration " + iter_str + " --> perplexity: " + perplex_str + "\n");
	}

	log_file->write_to_log("Gibbs sampling completed!\n");
	log_file->write_to_log("Saving the final model!\n");
	compute_theta_djkoo();
	compute_eta_djkso();
	compute_phi_ojksw();
	compute_psi_djooo();
	save_model(utils::generate_model_name(-1,this->save_model_name));

	return 0;
}

int USTM_FT_W::inference() {

    /*

	int sentiLab, topic, tag;

    log_file->write_to_log("Iteration 0 --> perplexity: " + log_file->convert_other_to_str(compute_perplexity())+ "\n");
	log_file->write_to_log("Sampling " + log_file->convert_other_to_str(niters) + " iterations!\n");

	//printf("Sampling %d iterations!\n", niters);
	for (int liter = 1; liter <= niters; liter++) {
        //printf("Iteration %d --> ...\n", liter);
		for (int m = 0; m < num_docs; m++) {
		    for (int w = 0; w < ptestdata->_docs[m]->length; w++) {
                //cout<<"m: "<<m<<" w: "<<w<<endl;
				inf_sampling(m, w, sentiLab, topic, tag);
				//cout<<"ptestdata->_docs[m]->length: "<<ptestdata->_docs[m]->length<<endl;
				s_dooow[m][w] = sentiLab;
                z_dooow[m][w] = topic;
                t_dooow[m][w] = tag;
            }
		}
        string iter_str = log_file->convert_other_to_str(liter);
        string perplex_str = log_file->convert_other_to_str(compute_perplexity());
        log_file->write_to_log("Iteration " + iter_str + " --> perplexity: " + perplex_str + "\n");
	}

	log_file->write_to_log("Gibbs sampling completed!\n");
	log_file->write_to_log("Saving the final model!\n");
	compute_theta_djkoo();
	compute_eta_djkso();
	compute_phi_ojksw();
	compute_psi_djooo();
	//save_model(utils::generate_model_name(-1,this->save_model_name));
    */
	return 0;
}



int USTM_FT_W::save_model(string model_name) {

    if (this->model_status == MODEL_STATUS_INF){
        pi_suffix = ".new.pi";
        theta_suffix = ".new.theta";
        phi_suffix = ".new.phi";
        others_suffix = ".new.others";
        twords_suffix = ".new.twords";
        psi_suffix = ".new.psi";
        eta_suffix = ".new.eta";
    }



    log_file->write_to_log("USTM_FT_W::save_model() begin......\n");

	if (save_model_tassign(dir + model_name + tassign_suffix))
		return 1;

    /*
	if (save_model_twords(dir + model_name + twords_suffix))
		return 1;
    */

	if (save_model_psi_djooo(dir + model_name + psi_suffix))
		return 1;

	if (save_model_theta_djkoo(dir + model_name + theta_suffix))
		return 1;

	if (save_model_eta_djkso(dir + model_name + eta_suffix))
		return 1;

	if (save_model_phi_ojksw(dir + model_name + phi_suffix))
		return 1;

	if (save_model_others(dir + model_name + others_suffix))
		return 1;

    log_file->write_to_log("USTM_FT_W::save_model() end......\n");

	return 0;
}


int USTM_FT_W::save_model_tassign(string filename) {
    FILE * fout = fopen(filename.c_str(), "w");
    if (!fout) {
	    log_file->write_to_log("Cannot save file " + filename + "!\n","error");
	    return 1;
    }

    dataset* ptempdat;
    if (this->model_status == MODEL_STATUS_EST)
        ptempdat = ptrndata;
    if (this->model_status == MODEL_STATUS_INF)
        ptempdat = ptestdata;

    for (int m = 0; m < num_docs; m++) {
        fprintf(fout, "%s ", ptempdat->docs[m]->docID.c_str());
        for (int n = 0; n < ptempdat->docs[m]->length; n++)
            fprintf(fout, "%d:%d:%d:%d ", ptrndata->docs[m]->words[n], t_dooow[m][n],z_dooow[m][n], s_dooow[m][n]); //  wordID:tag:topic:senti
        fprintf(fout, "\n");
    }

    fclose(fout);
	return 0;
}


int USTM_FT_W::save_model_twords(string filename)
{
    /*
    FILE * fout = fopen(filename.c_str(), "w");
    if (!fout) {
	    printf("Cannot save file %s!\n", filename.c_str());
	    return 1;
    }

    if (twords > vocabSize) {
	    twords = vocabSize; // print out entire vocab list
    }

    mapid2word::iterator it;

    for (int l = 0; l < numSentiLabs; l++) {
        for (int k = 0; k < numTopics; k++) {
	        vector<pair<int, double> > words_probs;
	        pair<int, double> word_prob;
	        for (int w = 0; w < vocabSize; w++) {
		        word_prob.first = w; // w: word id/index
	            word_prob.second = phi_lzw[l][k][w]; // topic-word probability
	            words_probs.push_back(word_prob);
	        }

		    std::sort(words_probs.begin(), words_probs.end(), sort_pred());

	        fprintf(fout, "Label%d_Topic%d\n", l, k);
	        for (int i = 0; i < twords; i++) {
		        it = id2word.find(words_probs[i].first);
	            if (it != id2word.end())
			        fprintf(fout, "%s   %15f\n", (it->second).c_str(), words_probs[i].second);
	        }
	    }
    }

    fclose(fout);
    */
    return 0;

}



int USTM_FT_W::save_model_psi_djooo(string filename) {

	FILE * fout = fopen(filename.c_str(), "w");
    if (!fout) {
		log_file->write_to_log("Cannot save file " + filename + "!\n","error");
		return 1;
    }

	for (int m = 0; m < num_docs; m++) {
		fprintf(fout, "%s ", ptrndata->docs[m]->docID.c_str());
		for (int j = 0; j < num_demos; j++) {
			fprintf(fout, "tag_%d:%f ", psi_djooo[m][j]);
		}
		fprintf(fout, "\n");
    }
    fclose(fout);
	return 0;
}


int USTM_FT_W::save_model_theta_djkoo(string filename) {

	FILE * fout = fopen(filename.c_str(), "w");
    if (!fout) {
		log_file->write_to_log("Cannot save file " + filename + "!\n","error");
		return 1;
    }

    for(int m = 0; m < num_docs; m++) {
        fprintf(fout, "%s ", ptrndata->docs[m]->docID.c_str());
        for (int t = 0; t < num_demos; t++) {
	        for (int z = 0; z < num_topics; z++) {
		        fprintf(fout, "tag_%d:topic:%d:%f ", t,z,theta_djkoo[m][t][z]);
	        }
		    fprintf(fout, "\n");
		 }
    }

    fclose(fout);
    return 0;
}

int USTM_FT_W::save_model_eta_djkso(string filename) {

	FILE * fout = fopen(filename.c_str(), "w");
    if (!fout) {
		log_file->write_to_log("Cannot save file " + filename + "!\n","error");
		return 1;
    }

    for(int m = 0; m < num_docs; m++) {
        fprintf(fout, "%s ", ptrndata->docs[m]->docID.c_str());
        for (int t = 0; t < num_demos; t++) {
	        for (int z = 0; z < num_topics; z++) {
                for (int s = 0; s < num_sentis; s++)
                    fprintf(fout, "tag_%d:topic_%d:senti_%d:%f ", t,z,s,eta_djkso[m][t][z]);
                    //fprintf(fout, "%d:%d:%d:%f ", t,z,s,eta_djkso[m][t][z]);
	        }
		    fprintf(fout, "\n");
		 }
    }

    fclose(fout);
    return 0;
}


int USTM_FT_W::save_model_phi_ojksw(string filename) {

	FILE * fout = fopen(filename.c_str(), "w");
    if (!fout) {
	    log_file->write_to_log("Cannot save file " + filename + "!\n","error");
	    return 1;
    }

    for (int t = 0; t < num_demos; t++) {
        for (int z = 0; z < num_topics; z++) {
            for (int s = 0; s < num_sentis; s++){
                fprintf(fout, "tag_%d:topic:%d_senti:%d ", t, z, s);
                for (int r = 0; r < num_vocabs; r++) {
                    fprintf(fout, "%d:%f ", r,phi_ojksw[t][z][s][r]);
                }
                fprintf(fout, "\n");
            }
        }
    }

    fclose(fout);
	return 0;
}


int USTM_FT_W::save_model_others(string filename) {

	FILE * fout = fopen(filename.c_str(), "w");
    if (!fout) {
	    log_file->write_to_log("Cannot save file " + filename + "!\n","error");
	    return 1;
    }

	fprintf(fout, "dir=%s\n", this->dir.c_str());
	fprintf(fout, "data_file=%s\n", this->data_file.c_str());
	fprintf(fout, "data_demo_file=%s\n", this->data_demo_file.c_str());
	fprintf(fout, "senti_lex_file=%s\n", this->senti_lex_file.c_str());

	fprintf(fout, "\n-------------------- Corpus statistics -----------------------\n");
    fprintf(fout, "numDocs=%d\n", num_docs);
    fprintf(fout, "corpusSize=%d\n", num_corpus);
	fprintf(fout, "aveDocLength=%d\n", ave_doc_length);
    fprintf(fout, "vocabSize=%d\n", num_vocabs);
    fprintf(fout, "demoSize=%d\n", num_demos);

    fprintf(fout, "\n---------------------- Model settings -----------------------\n");
	fprintf(fout, "numSentiLabs=%d\n", num_sentis);
	fprintf(fout, "numTopics=%d\n", num_topics);

	fprintf(fout, "_alpha=%f\n", _alpha);
	fprintf(fout, "_beta=%f\n", _beta);
	fprintf(fout, "_gamma=%f\n", _gamma);

	fclose(fout);
    return 0;
}

int USTM_FT_W::excute_model_train(Model_Para* model_para)
{
    if (init_para(model_para)) return 1;

    // read training data
    ptrndata = new dataset();
    if (ptrndata->read_data(data_file, dir + wordmapfile,"word")) {
        log_file->write_to_log("Fail to read training data!\n","error");
        return 1;
    }

    // read training demographics data
    ptrndemodata = new dataset();
    if (ptrndemodata->read_data(data_demo_file, dir + demomapfile,"word")) {
        log_file->write_to_log("Fail to read training demographics data!\n","error");
        return 1;
    }

    if (senti_lex_file != "") {
	    if (this->senLex.read_senti_lexicon(senti_lex_file)) {
	        string temp_str = senti_lex_file;
            log_file->write_to_log("Error! Cannot read sentiFile " + temp_str + "!\n","error");
            delete ptrndata;
            return 1;
		}
        if (this->senLex.get_wordid2senLabelDis(&ptrndata->word2id))
            return 1;
	}

	if (twords > 0)
        dataset::read_wordmap(dir + wordmapfile, &id2word);

    init_model_parameters();

    print_out_model_para();

	if (init_estimate()) return 1;

	if (estimate()) return 1;

	delete_model_parameters();

	return 0;

}


int USTM_FT_W::load_model_para(string model_name){

    log_file->write_to_log("USTM_FT_W::load_model_para() begin......\n");

    int num_doc_train = 0;
    int vocab_size_train = 0;
    int demo_size_train = 0;

    string filename = dir + model_name + others_suffix;

    FILE * fin = fopen(filename.c_str(), "r");
    if (!fin) {
        log_file->write_to_log("Cannot open file: " + filename + "\n");
        return 1;
    }

    char buff[BUFF_SIZE_SHORT];
    string line;

    while (fgets(buff, BUFF_SIZE_SHORT - 1, fin)) {
        line = buff;
        strtokenizer strtok(line, "= \t\r\n");
        int count = strtok.count_tokens();

        if (count != 2) {
            continue;
        }

        string optstr = strtok.token(0);
        string optval = strtok.token(1);

        if (optstr == "_alpha")
            this->_alpha = atof(optval.c_str());
        else if (optstr == "_beta")
            this->_beta = atof(optval.c_str());
        else if (optstr == "_gamma")
            this->_gamma = atof(optval.c_str());
        else if (optstr == "numTopics")
            this->num_topics = atoi(optval.c_str());
        else if (optstr == "numSentiLabs")
            this->num_sentis = atoi(optval.c_str());
        else if (optstr == "demoSize")
            demo_size_train = atoi(optval.c_str());
        else if (optstr == "numDocs")
            num_doc_train = atoi(optval.c_str());
        else if (optstr == "vocabSize")
            vocab_size_train = atoi(optval.c_str());
    }
    fclose(fin);

    ptrndata = new dataset(num_doc_train);
    ptrndata->vocabSize = vocab_size_train;
    ptrndemodata = new dataset(num_doc_train);
    ptrndemodata->vocabSize = demo_size_train;

    cout<<"ptrndata->vocabSize: "<<ptrndata->vocabSize<<endl;
    cout<<"ptrndemodata->vocabSize: "<<ptrndemodata->vocabSize<<endl;
    cout<<"num_doc_train: "<<num_doc_train<<endl;

    log_file->write_to_log("USTM_FT_W::load_model_para() begin......\n");

    return 0;
}


int USTM_FT_W::load_model(string model_name) {

    log_file->write_to_log("USTM_FT_W::load_model() begin......\n");

    utils::alloc_space(n_ojkow_train,ptrndemodata->vocabSize,num_topics,ptrndata->vocabSize);
    utils::alloc_space(n_ojkoo_train,ptrndemodata->vocabSize,num_topics);
    utils::alloc_space(n_ojksw_train,ptrndemodata->vocabSize,num_topics,num_sentis,ptrndata->vocabSize);
    utils::alloc_space(n_ojkso_train,ptrndemodata->vocabSize,num_topics,num_sentis);

    int i, j;

    string filename = dir + model_name + tassign_suffix;
    FILE * fin = fopen(filename.c_str(), "r");
    if (!fin) {
        log_file->write_to_log("Cannot open file " + filename + "to load model\n");
        return 1;
    }

    char buff[BUFF_SIZE_LONG];
    string line;

    for (i = 0; i < ptrndata->numDocs; i++) {
        char * pointer = fgets(buff, BUFF_SIZE_LONG, fin);
        if (!pointer) {
            log_file->write_to_log("Invalid word-topic assignment file, check the number of docs!\n");
            return 1;
        }

        line = buff;
        strtokenizer strtok(line, " \t\r\n");
        int length = strtok.count_tokens();

        vector<int> words;
        vector<int> tags;
        vector<int> sentis;
        vector<int> topics;

        for (j = 0; j < length; j++) {
            string token = strtok.token(j);
            strtokenizer tok(token, ":");
            if (tok.count_tokens() != 4) {
                if (j != 0){
                    log_file->write_to_log("Invalid word-topic assignment line!\n");
                    return 1;
                }
                continue;
            }
            words.push_back(atoi(tok.token(0).c_str()));
            tags.push_back(atoi(tok.token(1).c_str()));
            topics.push_back(atoi(tok.token(2).c_str()));
            sentis.push_back(atoi(tok.token(3).c_str()));
        }


        for (j = 0; j < topics.size(); j++){
            int w = words[j];
            int t = tags[j];
            int s = sentis[j];
            int z = topics[j];
            n_ojkow_train[t][z][w]    += 1;
            n_ojkoo_train[t][z]       += 1;
            n_ojksw_train[t][z][s][w] += 1;
            n_ojkso_train[t][z][s]    += 1;
            /*
            cout<<"w: "<<w<<endl;
            cout<<"t: "<<t<<endl;
            cout<<"s: "<<s<<endl;
            cout<<"z: "<<z<<endl;
            n_ojkow_train[t][z][w]    += 1;
            cout<<"n_ojkow_train[t][z][w]: "<<n_ojkow_train[t][z][w]<<endl;
            n_ojkoo_train[t][z]       += 1;
            cout<<"n_ojkoo_train[t][z]: "<<n_ojkoo_train[t][z]<<endl;
            n_ojksw_train[t][z][s][w] += 1;
            cout<<"n_ojksw_train[t][z][s][w]: "<<n_ojksw_train[t][z][s][w]<<endl;
            n_ojkso_train[t][z][s]    += 1;
            cout<<"n_ojkso_train[t][z][s]: "<<n_ojkso_train[t][z][s]<<endl;*/

        }
    }

    fclose(fin);

    log_file->write_to_log("USTM_FT_W::load_model() end......\n");

    return 0;
}

int USTM_FT_W::excute_model_test(Model_Para* model_para)
{
    /*

    log_file->write_to_log("USTM_FT_W::excute_model_test() begin......\n");

    if (init_para(model_para)) return 1;

    load_model_para(model_para->save_model_name);

    load_model(model_para->save_model_name);

    // read training data
    ptestdata = new dataset();
    if (ptestdata->read_testdata(data_file, dir + wordmapfile)) {
        log_file->write_to_log("Fail to read training data!\n","error");
        return 1;
    }

    // read training demographics data
    ptestdemodata = new dataset();
    if (ptestdemodata->read_testdata(data_demo_file, dir + demomapfile)) {
        log_file->write_to_log("Fail to read training demographics data!\n","error");
        return 1;
    }

    if (senti_lex_file != "") {
	    if (this->senLex.read_senti_lexicon(senti_lex_file)) {
	        string temp_str = senti_lex_file;
            log_file->write_to_log("Error! Cannot read sentiFile " + temp_str + "!\n","error");
            delete ptrndata;
            return 1;
		}
        if (this->senLex.get_wordid2senLabelDis(&ptestdata->word2id_train))
            return 1;
	}


	/// Problem
	if (twords > 0)
        dataset::read_wordmap(dir + wordmapfile, &id2word);

    init_model_parameters();

    print_out_model_para();


	if (init_inf()) return 1;

	if (inference()) return 1;

	delete_model_parameters();

	log_file->write_to_log("USTM_FT_W::excute_model_test() end......\n");
    */
	return 0;

}
