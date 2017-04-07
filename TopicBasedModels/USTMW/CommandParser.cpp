#include "CommandParser.h"


CCommandParser::CCommandParser(void)
{
    model_para.model_status = MODEL_STATUS_EST;
    model_para.model_type = MODEL_NAME_JST;
    model_para.save_model_name = "";
    model_para.dir = "";
    model_para.data_file = "";
    model_para.senti_lex_file = "";
    model_para.data_demo_file = "";

    model_para.alpha = 0.05;
    model_para.beta = 0.05;
    model_para.gamma = 0.05;
    model_para.eta = 0.05;

    model_para.numTopics = 30;
    model_para.niters = 150;
    model_para.twords = 20;
    model_para.numSentis = 3;


    model_para.wordmapfile = "wordmap.txt";
    model_para.demomapfile = "demomap.txt";
    model_para.log_file = "log.txt";
}


CCommandParser::~CCommandParser(void)
{

}

void CCommandParser::PrintOutHelpInfor(void)
{
	cout<<"Help......"<<endl;
	cout<<"USTMW.exe can be used to train a USTM_W model for sentiment analysis"<<endl;
	cout<<"USTMW.exe -ms     modelStatus   (est or inf) (default est)"<<endl;
	cout<<"          -mn     saveModelName (default model)\n";
	cout<<"          -dir    outDir\n";
	cout<<"          -df     dataFile\n";
	cout<<"          -ddf    dataDemoFile\n";
	cout<<"          -slf    sentimentLexFile\n";
	cout<<"          -lf     logFile       (default log.txt)\n";
	cout<<"          -alpha  alphaValue    (default 0.05)\n";
	cout<<"          -beta   betaValue     (default 0.05)\n";
	cout<<"          -gamma  gammaValue    (default 0.05)\n";
	cout<<"          -eta    etaValue      (default 0.05)\n";
	cout<<"          -nt     numTopics     (default 30)\n";
	cout<<"          -ns     numSentis     (default 3)\n";
	cout<<"          -ni     numIters      (default 150)\n";
	cout<<"          -wmf    wordMapFile   (default wordmap.txt)\n";
	cout<<"          -dmf    demoMapFile   (default demomap.txt)\n";
	cout<<"          -tws    twords        (default 20)\n";
	cout<<"          -h      print this help info\n";
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
	    else if (cmd_str == "-ddf")
			model_para.data_demo_file = argv[++i];
	    else if (cmd_str == "-slf")
			model_para.senti_lex_file = argv[++i];
	    else if (cmd_str == "-lf")
			model_para.log_file = argv[++i];
        else if (cmd_str == "-wmf")
			model_para.wordmapfile = argv[++i];
        else if (cmd_str == "-dmf")
			model_para.demomapfile = argv[++i];
        else if (cmd_str == "-alpha")
			model_para.alpha = atof(argv[++i]);
        else if (cmd_str == "-beta")
			model_para.beta = atof(argv[++i]);
        else if (cmd_str == "-gamma")
			model_para.gamma = atof(argv[++i]);
		else if (cmd_str == "-eta")
			model_para.eta = atof(argv[++i]);
        else if (cmd_str == "-nt")
			model_para.numTopics = atoi(argv[++i]);
        else if (cmd_str == "-ns")
			model_para.numSentis = atoi(argv[++i]);
        else if (cmd_str == "-ni")
			model_para.niters = atoi(argv[++i]);
        else if (cmd_str == "-tws")
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

    model_para.model_type = MODEL_NAME_USTM_FW_W;
}
