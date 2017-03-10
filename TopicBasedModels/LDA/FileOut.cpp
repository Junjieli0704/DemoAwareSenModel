#include "FileOut.h"


CFileOut::CFileOut(void)
{
    str_out = "";
    str_filename = "";
}

CFileOut::~CFileOut(void)
{
    file_stream.close();
}

void CFileOut::WriteToFile(string str_out)
{
    file_stream.write(str_out.c_str(),str_out.length());
}

void CFileOut::Close()
{
    file_stream.close();

}

bool CFileOut::OpenAFile(string str_filename , int mode)
{
    if (file_stream.is_open())
        file_stream.close();

    if (mode == 0)                        //�����ļ�������򿪵���ԭ���ļ��������ļ�д������ʱ�򣬻Ḳ��
        file_stream.open(str_filename.c_str());


    if (mode == 1)
        file_stream.open(str_filename.c_str(),ios::app); //��׷�ӵ���ʽ���ļ�

    if (file_stream.fail()) return false;
    else return true;
}


void CFileOut::WriteToFile_StringVector(vector <string> str,string space_mark = "\n")
{
	if (!str.empty()){
		for (int i = 0; i < str.size(); i++){
			WriteToFile(str.at(i));
			WriteToFile(space_mark);
		}
	}
}
