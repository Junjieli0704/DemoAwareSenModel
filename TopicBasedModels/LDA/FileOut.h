/* 处理文件输出的库文件 */

#pragma once
#include <string>
#include <fstream>
#include <sstream>
#include <vector>
using namespace std;
class CFileOut
{
private:
    string str_out;
    string str_filename;
    ofstream file_stream;



public:
    CFileOut(void);
    ~CFileOut(void);
    bool OpenAFile(string str_filename , int mode = 0);
	void WriteToFile(string str_out);
	void Close();
	void WriteToFile_StringVector(vector <string> str,string space_mark);

    template <class T>
	T ConvertStrToOther(const string &s) {
		T tempDat;
		std::stringstream ss(s);
		ss >> tempDat;
		return tempDat;

	}

	template <class T>
	string ConvertOtherToString(const T& num)
	{
		stringstream ss;
		ss << num;
		return ss.str();
	}




};

