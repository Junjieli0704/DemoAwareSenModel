/*
	����C++�����г�����������һ�����ļ�
	�ṹ�� paraModel������ C++ �����г���Ĳ�������
	����������
	// ������ʼ��
	void InitialParaModel(paraModel &tempParaModel);
	// �������������ʾ��Ϣ
	void PrintOutHelpInfor(void);
	// �����ض���ʽ���������е������
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

