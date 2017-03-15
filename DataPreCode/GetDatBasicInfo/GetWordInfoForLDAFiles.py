#encoding=utf-8


# -------------------------------------------------------------------- #
# 获取LDA待处理文件的里面词汇的基本信息，maxLen，minLen之类
# Time: 2017-03-14
# -------------------------------------------------------------------- #

import sys
sys.path.append("../UsefulLibs")
import usefulAPI, jsonAPI

class GetWordInfo:
    def __init__(self,lda_dat_file,out_file):
        self.lda_dat_file = lda_dat_file
        self.out_file = out_file
        self.all_dat_list = []
        self.word_dict = {}
        self.len_distri_dict = {}
        self.average_voca_len = 0.0

    def init_len_distri_dict(self):
        self.len_distri_dict['0-9'] = 0
        self.len_distri_dict['10-19'] = 0
        self.len_distri_dict['20-29'] = 0
        self.len_distri_dict['30-39'] = 0
        self.len_distri_dict['40+'] = 0

    def add_len_distri_dict(self,len_num):
        if len_num < 10:
            self.len_distri_dict['0-9'] = self.len_distri_dict['0-9'] + 1
        elif len_num < 20:
            self.len_distri_dict['10-19'] = self.len_distri_dict['10-19'] + 1
        elif len_num < 30:
            self.len_distri_dict['20-29'] = self.len_distri_dict['20-29'] + 1
        elif len_num < 40:
            self.len_distri_dict['30-39'] = self.len_distri_dict['30-39'] + 1
        else:
            self.len_distri_dict['40+'] = self.len_distri_dict['40+'] + 1


    def analysis_dat(self):
        self.init_len_distri_dict()
        all_voca_len = 0.0
        line_con_list = open(self.lda_dat_file,'r').readlines()
        for line_con in line_con_list:
            word_con_list = line_con.strip().split(' ')
            self.all_dat_list.append(line_con.strip())
            self.add_len_distri_dict(len(word_con_list) - 1)
            all_voca_len = all_voca_len + len(word_con_list) - 1
            for i in range(1,len(word_con_list)):
                word = word_con_list[i]
                if self.word_dict.has_key(word) == False:
                    self.word_dict[word] = 1
        self.average_voca_len = all_voca_len / len(line_con_list)

    def print_out_res(self):
        out_line_con_list = []
        out_line_con_list.append('voca_len:\t' + str(len(self.word_dict)))
        out_line_con_list.append('aver_len:\t' + str(self.average_voca_len))
        out_line_con_list.append('len 0-9:\t' + str(self.len_distri_dict['0-9']))
        out_line_con_list.append('len 10-19:\t' + str(self.len_distri_dict['10-19']))
        out_line_con_list.append('len 20-29:\t' + str(self.len_distri_dict['20-29']))
        out_line_con_list.append('len 30-39:\t' + str(self.len_distri_dict['30-39']))
        out_line_con_list.append('len 40+:\t' + str(self.len_distri_dict['40+']))
        open(self.out_file,'w+').write('\n'.join(out_line_con_list))

if __name__ == '__main__':

    lda_dat_file = '../../../ExpData/MovieData/LDAData/LDA_Style_Dat/Comedy_doc.txt'
    out_file = '../../../ExpData/MovieData/LDAData/LDA_Style_Dat/Comedy_doc_ana.txt'
    get_word_info = GetWordInfo(lda_dat_file,out_file)
    get_word_info.analysis_dat()
    get_word_info.print_out_res()