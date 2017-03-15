/*
	处理C++命令行程序参数输入的一个库文件
	结构体 paraModel，定义 C++ 命令行程序的参数输入
	三个函数：
	// 参数初始化
	void InitialParaModel(paraModel &tempParaModel);
	// 输出程序运行提示信息
	void PrintOutHelpInfor(void);
	// 按照特定方式，从命令行导入参数
	void LoadParaFromCommandLine(int argc, char ** argv, paraModel &tempParaModel);
*/

#pragma once
#include <string>
#include <iostream>
#include <stdlib.h>

#include "constants.h"
using namespace std;


class CCommandParser
{
private:
    Model_Para model_para;

public:
	void InitialParaModel(void);

	void PrintOutHelpInfor(void);

	void LoadParaFromCommandLine(int argc, char ** argv);

	Model_Para* get_model_para() {return &this->model_para;}

	CCommandParser(void);
	~CCommandParser(void);
};

