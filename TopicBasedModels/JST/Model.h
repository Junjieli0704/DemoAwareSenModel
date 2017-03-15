#ifndef MODEL_H
#define MODEL_H
#include "constants.h"
#include "LDA.h"
#include "USTM_FT_W.h"
#include "D_PLDA.h"
#include "JST_model.h"
#include "JST_inference.h"
#include "SenLDA_model.h"
#include "ASUM_model.h"
#include "log.h"
#include <iostream>

using namespace std;

class Model
{
    public:
        Model();
        ~Model();

        static int Choose_Model_Type(Model_Para *model_para, LogFile* logFile);

        static int LDA_process(Model_Para *model_para,LogFile* logFile);

        static int USTM_FT_W_process(Model_Para *model_para,LogFile* logFile);

        static int D_PLDA_process(Model_Para *model_para,LogFile* logFile);

        static int JST_Train(Model_Para *model_para,LogFile* logFile);

        static int JST_Test(Model_Para *model_para,LogFile* logFile);

        static int SENLDA_Train(Model_Para *model_para,LogFile* logFile);

        static int SENLDA_Test(Model_Para *model_para,LogFile* logFile);

        static int ASUM_Train(Model_Para *model_para,LogFile* logFile);

        static int ASUM_Test(Model_Para *model_para,LogFile* logFile);

};

#endif // MODEL_H
