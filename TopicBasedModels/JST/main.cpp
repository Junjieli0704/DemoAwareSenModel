#include <iostream>
#include "utils.h"
#include "math.h"
#include "log.h"
#include "CommandParser.h"
#include "constants.h"
#include "JST_model.h"
#include "JST_inference.h"

using namespace std;

int main(int argc, char ** argv)
{
    CCommandParser commandParser;

    commandParser.LoadParaFromCommandLine(argc,argv);

    Model_Para* model_para = commandParser.get_model_para();

    utils::make_dir(model_para->dir);


	LogFile *logFile = new LogFile(model_para->dir + model_para->log_file);
	logFile->open_file();

	if (model_para->model_status == MODEL_STATUS_EST){
        JST_model jst_est;
        jst_est.set_log_file(logFile);
        jst_est.excute_model(model_para);
    }

    if (model_para->model_status == MODEL_STATUS_INF){
        JST_inference jst_inf;
        jst_inf.set_log_file(logFile);
        jst_inf.excute_model(model_para);
    }

	logFile->close_file();

    return 0;
}
