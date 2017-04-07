#include <iostream>
#include "USTM_FT_W.h"
#include "utils.h"
#include "math.h"
#include "log.h"
#include "CommandParser.h"
using namespace std;


int main(int argc, char ** argv)
{

    CCommandParser commandParser;

    commandParser.LoadParaFromCommandLine(argc,argv);

    Model_Para* model_para = commandParser.get_model_para();

    utils::make_dir(model_para->dir);


	LogFile *logFile = new LogFile(model_para->dir + model_para->log_file);
	logFile->open_file();

    USTM_FT_W ustm_ft_w;
    ustm_ft_w.set_log_file(logFile);
    ustm_ft_w.excute_model(model_para);


	logFile->close_file();

    return 0;
}
