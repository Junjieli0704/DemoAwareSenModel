#include "LDA.h"

LDA::LDA()
{
    wordmapfile = "wordmap.txt";
    tassign_suffix = ".tassign";
    theta_suffix = ".theta";
    phi_suffix = ".phi";
    others_suffix = ".others";
    twords_suffix = ".twords";

    dir = "./";
    data_file = "trndocs.dat";
    save_model_name = "model-final";

    ptrndata = NULL;
    ptestdata = NULL;

    alpha = 50.0 / num_topics;
    beta = 0.1;
    num_iters = 2000;
    twords = 20;

    n_doo = NULL;
    n_oko = NULL;
    n_dko = NULL;
    n_okw = NULL;
    p_oko = NULL;
    z_dow = NULL;
    theta_dko = NULL;
    phi_okw = NULL;

}

LDA::~LDA()
{

}

void LDA::delete_model_parameters(){

    if (this->model_status == MODEL_STATUS_EST){
        utils::release_space(theta_dko,ptrndata->numDocs);
        utils::release_space(phi_okw,num_topics);
        utils::release_space(n_okw,num_topics);
        utils::release_space(n_dko,ptrndata->numDocs);
        utils::release_space(n_doo);
        utils::release_space(n_oko);
        utils::release_space(p_oko);
        utils::release_space(z_dow,ptrndata->numDocs);
    }

	if (this->model_status == MODEL_STATUS_INF){
        utils::release_space(theta_dko,ptestdata->numDocs);
        utils::release_space(phi_okw,num_topics);
        utils::release_space(n_okw,num_topics);
        utils::release_space(n_dko,ptestdata->numDocs);
        utils::release_space(n_doo);
        utils::release_space(n_oko);
        utils::release_space(p_oko);
        utils::release_space(n_okw_train,num_topics);
        utils::release_space(n_oko_train);
    }


}



void LDA::excute_model(Model_Para* model_para){

    if (init_para(model_para) == 0){
        est_inf();
        delete_model_parameters();
    }

}

int LDA::init_para(Model_Para* model_para) {

    this->model_status = model_para->model_status;

    this->save_model_name = model_para->save_model_name;

    this->dir = model_para->dir;

    if (model_para->data_file == "") {
        log_file->write_to_log("Please specify the input data file for model estimation!\n","error");
        return 1;
    }
    else {this->data_file = model_para->data_file;}

    if (model_para->numTopics >= 0.0)
        this->num_topics = model_para->numTopics;

    if (model_para->beta >= 0.0)
        this->beta = model_para->beta;

    if (model_para->alpha >= 0.0)
        this->alpha = model_para->alpha;
    else this->alpha = 50.0 / this->num_topics;

    if (model_para->niters >= 0)
        this->num_iters = model_para->niters;

    if (model_para->twords >= 0)
        this->twords = model_para->twords;

    if (model_para->wordmapfile != "")
        this->wordmapfile = model_para->wordmapfile;

    if (this->model_status == MODEL_STATUS_EST){
        if (init_est()) {
            return 1;
        }
    }

    if (this->model_status == MODEL_STATUS_INF){

        load_model_para(this->save_model_name);

        if (init_inf()) {
            return 1;
        }
    }

    return 0;
}

int LDA::load_model_para(string model_name){

    int num_doc_train = 0;
    int vocab_size_train = 0;

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

        if (optstr == "alpha")
            this->alpha = atof(optval.c_str());
        else if (optstr == "beta")
            this->beta = atof(optval.c_str());
        else if (optstr == "ntopics")
            this->num_topics = atoi(optval.c_str());
        else if (optstr == "ndocs")
            num_doc_train = atoi(optval.c_str());
        else if (optstr == "nwords")
            vocab_size_train = atoi(optval.c_str());

    }
    fclose(fin);

    ptrndata = new dataset(num_doc_train);
    //ptrndata->vocabSize = vocab_size_train;
    return 0;
}


int LDA::load_model(string model_name) {

    utils::alloc_space(n_okw_train,num_topics,ptestdata->vocabSize);
    utils::alloc_space(n_oko_train,num_topics);

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
        vector<int> topics;
        for (j = 1; j < length; j++) {
            string token = strtok.token(j);
            string split_str = ":-:-:";
            token = token.replace(token.find(split_str),split_str.length()," ");
            strtokenizer tok(token, " ");
            if (tok.count_tokens() != 2) {
                if (j != 0){
                    log_file->write_to_log("Invalid word-topic assignment line!\n");
                    return 1;
                }
                continue;
            }
            string word_str = tok.token(0);
            int word_id_in_test = ptestdata->get_id_from_str(word_str);
            words.push_back(word_id_in_test);
            topics.push_back(atoi(tok.token(1).c_str()));
        }

        for (j = 0; j < topics.size(); j++){
            n_okw_train[topics[j]][words[j]] += 1;
    	    n_oko_train[topics[j]] += 1;
        }
    }
    /*
    // this code is used for recording loading train data.
    for (int k = 0; k < this->num_topics; k++)
        for (int w = 0; w < ptestdata->vocabSize; w ++){
            if (n_okw_train[k][w] > 0)
                cout<<"n_okw_train["<<k<<"]["<<w<<"]: "<<n_okw_train[k][w]<<endl;
    }
    */

    fclose(fin);

    return 0;
}


int LDA::init_inf() {

    log_file->write_to_log("LDA::init_inf()  begin......\n");

    utils::alloc_space(p_oko,num_topics);

    // read new data for inference
    ptestdata = new dataset;
	if (ptestdata->read_data(this->data_file, this->dir + this->wordmapfile)) {
        log_file->write_to_log("Fail to read new data!\n");
        return 1;
    }

    // load model, i.e., read z and ptrndata
    if (load_model(save_model_name)) {
        log_file->write_to_log("Fail to load word-topic assignment file of the model!\n");
        return 1;
    }
    utils::alloc_space(n_doo,ptestdata->numDocs);
    utils::alloc_space(n_oko,num_topics);
    utils::alloc_space(n_dko,ptestdata->numDocs,num_topics);
    utils::alloc_space(n_okw,num_topics,ptestdata->vocabSize);

    srand(time(0));

    z_dow = new int*[ptestdata->numDocs];

    for (int m = 0; m < ptestdata->numDocs; m++) {
        int N = ptestdata->docs[m]->length;
        z_dow[m] = new int[N];
        for (int n = 0; n < N; n++) {
            int w = ptestdata->docs[m]->words[n];
    	    int topic = (int)(((double)rand() / RAND_MAX) * num_topics);
    	    if(topic == num_topics) topic = num_topics - 1;
    	    z_dow[m][n] = topic;
            n_okw[topic][w] += 1;
            n_dko[m][topic] += 1;
            n_oko[topic] += 1;
            n_doo[m] += 1;
        }
    }

    utils::alloc_space(theta_dko,ptestdata->numDocs,num_topics);
    utils::alloc_space(phi_okw,num_topics,ptestdata->vocabSize);

    log_file->write_to_log("LDA::init_inf()  end......\n");

    return 0;
}


int LDA::init_est() {

    int m, n;

    log_file->write_to_log("LDA::init_est() begin......\n");

    utils::alloc_space(p_oko,num_topics);

    // + read training data
    ptrndata = new dataset;
    if (ptrndata->read_data(this->data_file, this->dir + this->wordmapfile)) {
        string temp_str = "Fail to read training data!\n";
        log_file->write_to_log(temp_str,"error");
        return 1;
    }

    // + allocate memory and assign values for variables

    utils::alloc_space(n_doo,ptrndata->numDocs);
    utils::alloc_space(n_oko,num_topics);
    utils::alloc_space(n_dko,ptrndata->numDocs,num_topics);
    utils::alloc_space(n_okw,num_topics,ptrndata->vocabSize);

    srand(time(0));
    z_dow = new int*[ptrndata->numDocs];

    for (m = 0; m < ptrndata->numDocs; m++) {
        int N = ptrndata->docs[m]->length;
        z_dow[m] = new int[N];
        for (n = 0; n < N; n++) {
            int word_id = ptrndata->docs[m]->words[n];
    	    int topic = (int)(((double)rand() / RAND_MAX) * num_topics);
    	    if(topic == num_topics) topic = num_topics - 1;
    	    z_dow[m][n] = topic;
            n_okw[topic][word_id] += 1;
            n_dko[m][topic] += 1;
            n_oko[topic] += 1;
            n_doo[m] += 1;
        }
    }

    utils::alloc_space(theta_dko,ptrndata->numDocs,num_topics);
    utils::alloc_space(phi_okw,num_topics,ptrndata->vocabSize);

    log_file->write_to_log("LDA::init_est() end......\n");

    return 0;
}

void LDA::print_out_model_para(){

    vector <string> temp_str_list;

    if(this->model_status == MODEL_STATUS_EST){
        temp_str_list.push_back("************** Model_Para for LDA Training***************\n");
        temp_str_list.push_back("model_type      --> LDA\n");
        temp_str_list.push_back("model_task      --> est\n");
        temp_str_list.push_back("save_model_name --> " + this->save_model_name + "\n");
        temp_str_list.push_back("dir             --> " + this->dir + "\n");
        temp_str_list.push_back("data_file       --> " + this->data_file + "\n");
        temp_str_list.push_back("alpha           --> " + log_file->convert_other_to_str(this->alpha) + "\n");
        temp_str_list.push_back("beta            --> " + log_file->convert_other_to_str(this->beta) + "\n");
        temp_str_list.push_back("numTopics       --> " + log_file->convert_other_to_str(this->num_topics) + "\n");
        temp_str_list.push_back("niters          --> " + log_file->convert_other_to_str(this->num_iters) + "\n");
        temp_str_list.push_back("wordmapfile     --> " + this->wordmapfile + "\n");
        temp_str_list.push_back("*********************************************************\n\n\n");

        temp_str_list.push_back("************** Data_Para ********************************\n");
        temp_str_list.push_back("numDocs         --> " + log_file->convert_other_to_str(this->ptrndata->numDocs) + "\n");
        temp_str_list.push_back("vocabSize       --> " + log_file->convert_other_to_str(this->ptrndata->vocabSize) + "\n");
        temp_str_list.push_back("corpusSize      --> " + log_file->convert_other_to_str(this->ptrndata->corpusSize) + "\n");
        temp_str_list.push_back("*********************************************************\n\n\n");
    }

  else if(this->model_status == MODEL_STATUS_INF){
        temp_str_list.push_back("************** Model_Para for LDA Testing****************\n");
        temp_str_list.push_back("model_type      --> LDA\n");
        temp_str_list.push_back("model_task      --> inf\n");
        temp_str_list.push_back("save_model_name --> " + this->save_model_name + "\n");
        temp_str_list.push_back("dir             --> " + this->dir + "\n");
        temp_str_list.push_back("data_file       --> " + this->data_file + "\n");
        temp_str_list.push_back("alpha           --> " + log_file->convert_other_to_str(this->alpha) + "\n");
        temp_str_list.push_back("beta            --> " + log_file->convert_other_to_str(this->beta) + "\n");
        temp_str_list.push_back("numTopics       --> " + log_file->convert_other_to_str(this->num_topics) + "\n");
        temp_str_list.push_back("niters          --> " + log_file->convert_other_to_str(this->num_iters) + "\n");
        temp_str_list.push_back("wordmapfile     --> " + this->wordmapfile + "\n");
        temp_str_list.push_back("*********************************************************\n\n\n");

        temp_str_list.push_back("************** Data_Para ********************************\n");
        temp_str_list.push_back("numDocs         --> " + log_file->convert_other_to_str(this->ptestdata->numDocs) + "\n");
        temp_str_list.push_back("vocabSize       --> " + log_file->convert_other_to_str(this->ptestdata->vocabSize) + "\n");
        temp_str_list.push_back("corpusSize      --> " + log_file->convert_other_to_str(this->ptestdata->corpusSize) + "\n");
        temp_str_list.push_back("*********************************************************\n\n\n");
    }

    for(vector<string>::iterator it  = temp_str_list.begin(); it != temp_str_list.end(); ++it)
        log_file->write_to_log(*it);

}

void LDA::compute_theta() {

    if(this->model_status == MODEL_STATUS_EST){
        for (int m = 0; m < ptrndata->numDocs; m++)
            for (int k = 0; k < num_topics; k++)
                theta_dko[m][k] = (n_dko[m][k] + alpha) / (n_doo[m] + num_topics * alpha);
    }

    if(this->model_status == MODEL_STATUS_INF){
        for (int m = 0; m < ptestdata->numDocs; m++)
            for (int k = 0; k < num_topics; k++){
                theta_dko[m][k] = (n_dko[m][k] + alpha) / (n_doo[m] + num_topics * alpha);
            }
    }
}

void LDA::compute_phi() {

    if(this->model_status == MODEL_STATUS_EST){
        for (int k = 0; k < num_topics; k++)
            for (int w = 0; w < ptrndata->vocabSize; w++){
                phi_okw[k][w] = (n_okw[k][w] + beta) / (n_oko[k] + ptrndata->vocabSize * beta);
            }
    }

    if(this->model_status == MODEL_STATUS_INF){
        for (int k = 0; k < num_topics; k++)
            for (int w = 0; w < ptestdata->vocabSize; w++){
                //cout<<"n_okw_train["<<k<<"]["<<w<<"]"<<n_okw_train[k][w]<<endl;
                //phi_okw[k][w] = (n_okw_train[k][w] + n_okw[k][w] + beta) / (n_oko[k] + n_oko_train[k] + ptestdata->vocabSize * beta);
                phi_okw[k][w] = (n_okw[k][w] + beta) / (n_oko[k] + ptestdata->vocabSize * beta);
        }
    }

}

double LDA::compute_perplexity(){

    //log_file->write_to_log("LDA::compute_perplexity() begin......\n");

    compute_phi();
    compute_theta();

    dataset * ptempdat = NULL;

    if(this->model_status == MODEL_STATUS_EST)
        ptempdat = ptrndata;
    if(this->model_status == MODEL_STATUS_INF)
        ptempdat = ptestdata;

    double N = ptempdat->corpusSize;
    double log_per = 0.0;
    for (int m = 0; m < ptempdat->numDocs; m++) {
        for (int n = 0; n < ptempdat->docs[m]->length; n++) {
            int w = ptempdat->docs[m]->words[n];
            double doc_word_prob = 0;
            for (int k = 0; k < num_topics; k ++){
                doc_word_prob = doc_word_prob + theta_dko[m][k] * phi_okw[k][w];
            }

            double neg_log_doc_prob = -log(doc_word_prob);
            log_per += neg_log_doc_prob;
        }
    }

    double plex_value = exp(log_per / N);

    //log_file->write_to_log("LDA::compute_perplexity() end......\n");
    return plex_value;

}



void LDA::est_inf() {

    log_file->write_to_log("LDA::est_inf() begin......\n");

    if (twords > 0)
        dataset::read_wordmap(dir + wordmapfile, &id2word);

    print_out_model_para();

    string temp_str = "Sampling " + log_file->convert_other_to_str(num_iters) + " iterations!\n";
    log_file->write_to_log(temp_str,"info");
    temp_str = "Initial perplexity " + log_file->convert_other_to_str(compute_perplexity()) + "\n";
    log_file->write_to_log(temp_str,"info");

    dataset* ptempdat = NULL;

    if (this->model_status == MODEL_STATUS_EST)
        ptempdat = ptrndata;
    if (this->model_status == MODEL_STATUS_INF)
        ptempdat = ptestdata;


    int liter = 0;
    int last_iter = liter;
    for (liter = last_iter + 1; liter <= num_iters + last_iter; liter++) {
        //clock_t start,finish;
        //start=clock();
        for (int m = 0; m < ptempdat->numDocs; m++) {
            for (int n = 0; n < ptempdat->docs[m]->length; n++) {
                int topic = sampling(m, n);
                z_dow[m][n] = topic;
            }
        }
        //finish=clock();
        //double second_time = float(finish-start) / float(CLOCKS_PER_SEC);
        //log_file->write_to_log(log_file->convert_other_to_str(second_time),"info");
        temp_str = "Iteration: " + log_file->convert_other_to_str(liter) + " --> perplexity: " + log_file->convert_other_to_str(compute_perplexity()) + "\n";
        log_file->write_to_log(temp_str,"info");
    }
    log_file->write_to_log("Gibbs sampling completed!\n","info");
    log_file->write_to_log("Saving the final model!\n","info");
    compute_theta();
    compute_phi();
    save_model(utils::generate_model_name(-1,save_model_name));
    log_file->write_to_log("LDA::est_inf() end......\n");
}

int LDA::save_model(string model_name) {

    if (this->model_status == MODEL_STATUS_INF){
        tassign_suffix = ".new.tassign";
        theta_suffix = ".new.theta";
        phi_suffix = ".new.phi";
        others_suffix = ".new.others";
        twords_suffix = ".new.twords";
    }

    log_file->write_to_log("LDA::save_model() begin......\n");

    if (save_model_tassign(dir + model_name + tassign_suffix))
        return 1;

    if (save_model_others(dir + model_name + others_suffix))
        return 1;

    if (save_model_theta(dir + model_name + theta_suffix))
        return 1;

    if (save_model_phi(dir + model_name + phi_suffix))
        return 1;

    if (twords > 0)
        if (save_model_twords(dir + model_name + twords_suffix))
            return 1;

    log_file->write_to_log("LDA::save_model() end......\n");

    return 0;
}

int LDA::save_model_tassign(string filename) {

    int i, j;
    if (!fileout.OpenAFile(filename,0)){
        string temp_str = "Cannot open file " + filename + " to save!\n";
        log_file->write_to_log(temp_str,"error");
        return -1;
    }

    vector <string> file_con_list;

    if (this->model_status == MODEL_STATUS_EST){
        for (i = 0; i < ptrndata->numDocs; i++) {
            string line_con = "";
            line_con += ptrndata->docs[i]->docID;
            line_con += " ";
            for (j = 0; j < ptrndata->docs[i]->length; j++) {
                int word_id = ptrndata->docs[i]->words[j];
                string word_str = ptrndata->get_str_from_id(word_id);
                line_con += word_str;
                line_con += ":-:-:";
                line_con += fileout.ConvertOtherToString(z_dow[i][j]);
                line_con += " ";
            }
            file_con_list.push_back(line_con);
        }
    }

    fileout.WriteToFile_StringVector(file_con_list,"\n");
    fileout.Close();
    return 0;
}

int LDA::save_model_theta(string filename) {
    FILE * fout = fopen(filename.c_str(), "w");
    if (!fout) {
        string temp_str = "Cannot open file " + filename + " to save!\n";
        log_file->write_to_log(temp_str,"error");
        return 1;
    }

    if (this->model_status == MODEL_STATUS_EST){
        for (int i = 0; i < ptrndata->numDocs; i++) {
            fprintf(fout, "%s ", ptrndata->docs[i]->docID.c_str());
            for (int j = 0; j < num_topics; j++)
                fprintf(fout, "%d:%f ", j,theta_dko[i][j]);
            fprintf(fout, "\n");
        }
    }
    if (this->model_status == MODEL_STATUS_INF){
        for (int i = 0; i < ptestdata->numDocs; i++) {
            fprintf(fout, "%s ", ptestdata->docs[i]->docID.c_str());
            for (int j = 0; j < num_topics; j++)
                fprintf(fout, "%d:%f ", j,theta_dko[i][j]);
            fprintf(fout, "\n");
        }
    }


    fclose(fout);

    return 0;
}

int LDA::save_model_phi(string filename) {
    FILE * fout = fopen(filename.c_str(), "w");
    if (!fout) {
        string temp_str = "Cannot open file " + filename + " to save!\n";
        log_file->write_to_log(temp_str,"error");
        return 1;
    }
    int num_vocab = 0;
    if (this->model_status == MODEL_STATUS_EST)
        num_vocab = ptrndata->vocabSize;
    if (this->model_status == MODEL_STATUS_INF)
        num_vocab = ptestdata->vocabSize;

    for (int i = 0; i < num_topics; i++) {
        for (int j = 0; j < num_vocab; j++){
            fprintf(fout, "%d:%d:%f ", i,j,phi_okw[i][j]);}
        fprintf(fout, "\n");
    }

    fclose(fout);

    return 0;
}

int LDA::save_model_others(string filename) {
    FILE * fout = fopen(filename.c_str(), "w");
    if (!fout) {
        string temp_str = "Cannot open file " + filename + " to save!\n";
        log_file->write_to_log(temp_str,"error");
        return 1;
    }

    fprintf(fout, "alpha=%f\n", alpha);
    fprintf(fout, "beta=%f\n", beta);
    fprintf(fout, "ntopics=%d\n", num_topics);
    if (this->model_status == MODEL_STATUS_EST){
        fprintf(fout, "ndocs=%d\n", ptrndata->numDocs);
        fprintf(fout, "nwords=%d\n", ptrndata->vocabSize);
    }
    if (this->model_status == MODEL_STATUS_INF){
        fprintf(fout, "ndocs=%d\n", ptestdata->numDocs);
        fprintf(fout, "nwords=%d\n", ptestdata->vocabSize);
    }

    fclose(fout);

    return 0;
}

int LDA::save_model_twords(string filename) {
    FILE * fout = fopen(filename.c_str(), "w");
    if (!fout) {
        string temp_str = "Cannot open file " + filename + " to save!\n";
        log_file->write_to_log(temp_str,"error");
        return 1;
    }

    int num_vocab = 0;
    if (this->model_status == MODEL_STATUS_EST)
        num_vocab = ptrndata->vocabSize;
    if (this->model_status == MODEL_STATUS_INF)
        num_vocab = ptestdata->vocabSize;


    if (twords > num_vocab)
        twords = num_vocab;

    mapid2word::iterator it;

    for (int k = 0; k < num_topics; k++) {
        vector<pair<int, double> > words_probs;
        pair<int, double> word_prob;
        for (int w = 0; w < num_vocab; w++) {
            word_prob.first = w;
            word_prob.second = phi_okw[k][w];
            words_probs.push_back(word_prob);
        }

        // quick sort to sort word-topic probability
	utils::quicksort(words_probs, 0, words_probs.size() - 1);

	fprintf(fout, "Topic %dth:\n", k);
	for (int i = 0; i < twords; i++) {
	    it = id2word.find(words_probs[i].first);
	    if (it != id2word.end()) {
		fprintf(fout, "\t%s   %f\n", (it->second).c_str(), words_probs[i].second);
	    }
	}
    }

    fclose(fout);

    return 0;
}

int LDA::sampling(int m, int n) {

    //log_file->write_to_log("LDA::sampling() begin......\n");

    int topic = z_dow[m][n];

    int w = 0;
    int num_vocab = 0;


    if (this->model_status == MODEL_STATUS_EST){
        w = ptrndata->docs[m]->words[n];
        num_vocab = ptrndata->vocabSize;
    }
    if (this->model_status == MODEL_STATUS_INF){
        w = ptestdata->docs[m]->words[n];
        num_vocab = ptestdata->vocabSize;
    }

    n_okw[topic][w] -= 1;
    n_dko[m][topic] -= 1;
    n_oko[topic] -= 1;
    n_doo[m] -= 1;

    double Vbeta = num_vocab * beta;
    double Kalpha = num_topics * alpha;
    // do multinomial sampling via cumulative method
    for (int k = 0; k < num_topics; k++) {
        if (this->model_status == MODEL_STATUS_EST){
            p_oko[k] = (n_okw[k][w] + beta)  / (n_oko[k] + Vbeta) *
                       (n_dko[m][k] + alpha) / (n_doo[m] + Kalpha);
        }
        if (this->model_status == MODEL_STATUS_INF){
            p_oko[k] = (n_okw_train[k][w] + n_okw[k][w] + beta)  / (n_oko_train[k] + n_oko[k] + Vbeta) *
                       (n_dko[m][k] + alpha) / (n_doo[m] + Kalpha);
            //p_oko[k] = (n_okw[k][w] + beta)  / (n_oko[k] + Vbeta) *
            //           (n_dko[m][k] + alpha) / (n_doo[m] + Kalpha);
        }

    }

    // cumulate multinomial parameters
    for (int k = 1; k < num_topics; k++) {
        p_oko[k] += p_oko[k - 1];
    }

    // scaled sample because of unnormalized p[]
    double u = ((double)rand() / RAND_MAX) * p_oko[num_topics - 1];

    for (topic = 0; topic < num_topics; topic++) {
        if (p_oko[topic] > u) {
            break;
        }
    }

    if (topic == num_topics) topic = num_topics - 1;

    // add newly estimated z_i to count variables
    n_okw[topic][w] += 1;

    n_dko[m][topic] += 1;
    n_oko[topic] += 1;
    n_doo[m] += 1;

    //log_file->write_to_log("LDA::sampling() end......\n");

    return topic;
}



