#include "CommandParser.h"


CCommandParser::CCommandParser(void)
{
    model_para.model_status = MODEL_STATUS_EST;
    model_para.model_type = MODEL_NAME_LDA;
    model_para.save_model_name = "model";
    model_para.dir = "./Out/";
    model_para.data_file = "";

    model_para.alpha = 0.05;
    model_para.beta = 0.05;

    model_para.numTopics = 30;
    model_para.niters = 150;
    model_para.twords = 20;

    model_para.wordmapfile = "wordmap.txt";
    model_para.log_file = "log.txt";
}


CCommandParser::~CCommandParser(void)
{

}

void CCommandParser::PrintOutHelpInfor(void)
{

	cout<<"Help......"<<endl;
	cout<<"LDA.exe can be used to train or inference a LDA-based model."<<endl;
	cout<<"LDA.exe -ms     modelStatus   (est or inf) (default est)"<<endl;
	cout<<"        -mn     saveModelName (default model)\n";
	cout<<"        -dir    outDir        (default ./Out/)\n";
	cout<<"                modelOutFiles, logFile and wordMapFile\n";
	cout<<"                are all in the outDir\n";
	cout<<"        -df     dataFile\n";
	cout<<"        -lf     logFile       (default log.txt)\n";
	cout<<"        -alpha  alphaValue    (default 0.05)\n";
	cout<<"        -beta   betaValue     (default 0.05)\n";
	cout<<"        -nt     numTopics     (default 30)\n";
	cout<<"        -ni     numIters      (default 150)\n";
	cout<<"        -wmf    wordMapFile   (default wordmap.txt)\n";
	cout<<"        -tw     twords        (default 20)\n";
	cout<<"        -h      print this help info\n";

}



void CCommandParser::LoadParaFromCommandLine(int argc, char ** argv)
{
    string model_status = "";
    string model_name = "";

	if (argc == 1)	PrintOutHelpInfor();
	int i = 1;
	for (i = 1; (i<argc) ; i++) {
	    string cmd_str(argv[i]);
	    if (cmd_str == "-h"){
            PrintOutHelpInfor();
			exit(0);
	    }
	    else if (cmd_str == "-mt")
			model_name = argv[++i];
	    else if (cmd_str == "-ms")
			model_status = argv[++i];
	    else if (cmd_str == "-mn")
			model_para.save_model_name = argv[++i];
	    else if (cmd_str == "-dir")
			model_para.dir = argv[++i];
	    else if (cmd_str == "-df")
			model_para.data_file = argv[++i];
	    else if (cmd_str == "-lf")
			model_para.log_file = argv[++i];
        else if (cmd_str == "-wmf")
			model_para.wordmapfile = argv[++i];
        else if (cmd_str == "-alpha")
			model_para.alpha = atof(argv[++i]);
        else if (cmd_str == "-beta")
			model_para.beta = atof(argv[++i]);
        else if (cmd_str == "-nt")
			model_para.numTopics = atoi(argv[++i]);
        else if (cmd_str == "-ni")
			model_para.niters = atoi(argv[++i]);
        else if (cmd_str == "-tw")
			model_para.twords = atoi(argv[++i]);
	    else{
            cout << "Unrecognized option: " << argv[i] << "!" << endl;
			PrintOutHelpInfor();
			exit(0);
	    }
	}

	if (model_status == "est")
        model_para.model_status = MODEL_STATUS_EST;
    else if (model_status == "inf")
        model_para.model_status = MODEL_STATUS_INF;
    else
        model_para.model_status = MODEL_STATUS_UNKNOWN;

    model_para.model_type = MODEL_NAME_LDA;

}
