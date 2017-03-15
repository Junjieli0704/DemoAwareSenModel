#ifndef LOG_H
#define LOG_H
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
using namespace std;

class LogFile
{
    string log_file;
    ofstream file_fin;
    public:
        LogFile(){
            log_file = "log.txt";
        }
        LogFile(string log_file){
            this->log_file = log_file;
        }
        ~LogFile(){
            if (file_fin.is_open())
                file_fin.close();
        }

        void open_file(void){
            if (file_fin.is_open())
                file_fin.close();
            file_fin.open(log_file.c_str(),ios::app);
        }

        void write_to_log(string str_out, string info_type = "info", bool is_need_print_out = true){
            info_type = info_type + ":\t";
            if (is_need_print_out)
                cout<<info_type<<str_out;
            else
                file_fin.write(info_type.c_str(),info_type.length());
                file_fin.write(str_out.c_str(),str_out.length());
        }

        void close_file(void){
            if (file_fin.is_open())
                file_fin.close();
        }

        template <class T>
        string convert_other_to_str(const T& num){
        	stringstream ss;
        	ss << num;
        	return ss.str();
        }

        template <class T>
        T convert_str_to_other(const string &s) {
            T temp_dat;
            std::stringstream ss(s);
            ss >> temp_dat;
            return temp_dat;
        }




};

#endif // LOG_H
