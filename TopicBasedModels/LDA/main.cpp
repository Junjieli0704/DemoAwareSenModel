#include <iostream>
#include "utils.h"
#include "math.h"
#include "log.h"
#include "CommandParser.h"
#include "LDA.h"
using namespace std;

/*
int main_fun(string config_file = "config.properties",
             string log_file = "log.txt",
             string model_name = "",
             int topic_nums = 0){

	utils *putils = new utils();

	if (putils->load_config_file(config_file)) {
        return 1;
	}

	set_model_para(putils,model_name,topic_nums);


	LogFile *logFile = new LogFile(log_file);
	logFile->open_file();

	Model::Choose_Model_Type(putils->get_model_para(),logFile);

	logFile->close_file();
}
*/

int main(int argc, char ** argv)
{
    CCommandParser commandParser;

    commandParser.LoadParaFromCommandLine(argc,argv);

    Model_Para* model_para = commandParser.get_model_para();

    utils::make_dir(model_para->dir);


	LogFile *logFile = new LogFile(model_para->dir + model_para->log_file);
	logFile->open_file();

    LDA lda;
    lda.set_log_file(logFile);
    lda.excute_model(model_para);

	logFile->close_file();



    return 0;
}
