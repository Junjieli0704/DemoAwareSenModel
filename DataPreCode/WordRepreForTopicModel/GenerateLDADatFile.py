#encoding=utf-8

# -------------------------------------------------------------------- #
# 对Json的数据进行处理，按照LDA模型采用的文件格式进行输出
# 有以下几类格式（本代码可以输出的，前面有OK）：
#   OK  LDA：    简单的词袋模型，文档表示成一堆词汇
#   OK  JST：    简单的词袋模型，文档表示成一堆词汇 + 情感词典作为情感信息的因素
#   OK  ASUM：   每个句子单独有一个主题，句子内容是词袋模型 + 情感词典作为情感信息的因素
#   OK  USTM_W： 简单的词袋模型，文档表示成一堆词汇 + 情感词典作为情感信息的因素 + 用户信息
#   OK  USTM_S： 每个句子单独有一个主题，句子内容是词袋模型 + 情感词典作为情感信息的因素 + 用户信息
#       D_PLDA： 篇章表示成评价对象pair的组合 + 情感词典作为情感信息的因素
#       DSTM：   篇章表示成评价对象pair的组合 + 情感词典作为情感信息的因素 + 用户信息
# 本代码是实现 LDA JST ASUM USTM_W USTM_S 的文件输出格式的代码
#    主要在 函数 generLDADat.generate_out_dat_lda_file 中，其中里面有个参数 mode
#       当 mode='Doc' --> LDA JST USTM_W 形式输出
#       当 mode='Sen' --> ASUM USTM_S    形式输出
#    函数 generLDADat.generate_out_demo_lda_file 用来生成包含用户信息的文件
# Revise Time: 2017-01-16 14:58
# -------------------------------------------------------------------- #

import os
import sys
sys.path.append("../UsefulLibs")
import usefulAPI, jsonAPI

class GenerateClassicLDABasedDat:
    def __init__(self,in_json_dat_file):
        self.in_json_dat_file = in_json_dat_file
        self.all_dat_list = []
        self.delete_word_dict = {}
        self.senti_word_dict = {}

    def load_json_file(self):
        print 'before load_json_file ......'
        self.all_dat_list = jsonAPI.load_json_dat(self.in_json_dat_file)
        print 'after  load_json_file ......'

    def load_senti_file(self,senti_file):
        if os.path.exists(senti_file):
            for line_con in open(senti_file,'r').readlines():
                line_con = line_con.strip()
                word_list = line_con.split('\t')
                if len(word_list) == 2:
                    word = word_list[0]
                    score = int(word_list[1])
                    self.senti_word_dict[word] = score
            return 1
        else:
            print 'Error! Sentiment word file is not exist.'
            return -1

    def generate_delete_word_dict(self,common_value = 0.3,rare_value = 2,is_need_pruncation = True):
        word_to_times_dict = {}
        for temp_dat in self.all_dat_list:
            word_list = temp_dat['doc_dict']['seg_con'].split(' ')
            pos_list =  temp_dat['doc_dict']['pos_con'].split(' ')

            for i in range(0,len(word_list)):
                word = word_list[i]
                if is_need_pruncation and pos_list[i] == 'PU':
                    self.delete_word_dict[word] = 1
                    continue
                if word_to_times_dict.has_key(word) == False:
                    word_to_times_dict[word] = 1
                else:
                    word_to_times_dict[word] = word_to_times_dict[word] + 1

        for word, times in word_to_times_dict.items():
            if self.senti_word_dict.has_key(word): continue
            elif times < rare_value:
                self.delete_word_dict[word] = 1
            elif times > len(self.all_dat_list) * common_value:
                self.delete_word_dict[word] = 1


    def generate_out_dat_lda_file(self,
                              mode = 'Doc',
                              sentiment_word_file = '',
                              common_value = 1.0,
                              rare_value = 5,
                              is_need_pruncation = False,
                              is_need_processing = True,
                              out_dat_file = 'dat.txt'):
        self.load_senti_file(sentiment_word_file)
        self.delete_word_dict = {}
        self.generate_delete_word_dict(common_value,rare_value,is_need_pruncation)
        if is_need_processing == False:
            self.delete_word_dict = {}
        if mode == 'Doc':
            out_line_con_list = []
            for temp_dat in self.all_dat_list:
                temp_word_list = []
                temp_word_list.append(temp_dat['comment_id'].encode('utf-8'))
                for word in temp_dat['doc_dict']['seg_con'].split(' '):
                    if self.delete_word_dict.has_key(word): continue
                    else: temp_word_list.append(word.encode('utf-8'))
                out_line_con_list.append(' '.join(temp_word_list))
            open(out_dat_file,'w+').write('\n'.join(out_line_con_list))

        elif mode == 'Sen':
            out_line_con_list = []
            for temp_dat in self.all_dat_list:
                commment_id = temp_dat['comment_id'].encode('utf-8')
                for i in range(0,len(temp_dat['doc_dict']['sen_list'])):
                    temp_word_list = []
                    temp_word_list.append(commment_id + '_s' + str(i+1))
                    for word in temp_dat['doc_dict']['sen_list'][i]['seg'].split(' '):
                        if self.delete_word_dict.has_key(word): continue
                        else: temp_word_list.append(word.encode('utf-8'))
                    if len(temp_word_list) == 1: continue
                    out_line_con_list.append(' '.join(temp_word_list))
            open(out_dat_file,'w+').write('\n'.join(out_line_con_list))

    def generate_out_demo_lda_file(self,out_demo_file = 'dat.txt'):
        out_dem_line_con_list = []
        for temp_dat in self.all_dat_list:
            temp_str = temp_dat['comment_id'].encode('utf-8') + 'demo '
            temp_word_list = []
            for temp_info in temp_dat['user_info'].split('_'):
                if len(temp_info.split('/')) == 2:
                   attribute = temp_info.split('/')[0]
                   value = temp_info.split('/')[1]
                   if attribute == 'Sex' or attribute == 'Loc' or attribute == 'Age':
                       if value != 'NULL':
                           temp_word_list.append(temp_info.encode('utf-8'))
            temp_str = temp_str + ' '.join(temp_word_list)
            out_dem_line_con_list.append(temp_str)
        open(out_demo_file,'w+').write('\n'.join(out_dem_line_con_list))


def generage_lda_dat_file_list(mode_list = ['Doc','Sen'],
                               common_value_list = [0.2,0.25,0.3,0.35,0.4,0.45,0.5],
                               is_need_prun_list = [True,False],
                               rare_value_list = [1,2,3,4,5,10]):
    movie_type = 'Comedy'
    in_json_dat_file = '../../../ExpData/MovieData/JsonDatForEachCat/' + movie_type + '.json'
    generLDADat = GenerateClassicLDABasedDat(in_json_dat_file)
    generLDADat.load_json_file()
    for mode in mode_list:
        for common_value in common_value_list:
            for is_need_prun in is_need_prun_list:
                for rare_value in rare_value_list:
                    out_file_fold = '../../../ExpData/MovieData/LDAData/TempDocSenDat/'
                    usefulAPI.mk_dir(out_file_fold)
                    out_lda_dat_file = out_file_fold + movie_type + '_' + mode + '_Rare_' + str(rare_value) + '_Prun_' + str(is_need_prun) + '_ComValue_' + str(common_value) + '.txt'
                    generLDADat.generate_out_dat_lda_file(mode = mode,
                                                          out_dat_file = out_lda_dat_file,
                                                          rare_value = rare_value,
                                                          is_need_pruncation = is_need_prun,
                                                          common_value = common_value)


if __name__ == '__main__':
    movie_type = 'Comedy'
    in_json_dat_file = '../../../ExpData/MovieData/JsonDat/JsonData/' + movie_type + '.json'
    in_senti_word_file = '../../../ExpData/SentiWordDat/ReviseSentiWord/revise_sentiment_word_list.txt'
    out_lda_dat_file = '../../../ExpData/MovieData/LDAData/LDA_Style_Dat/' + movie_type + '_doc.txt'
    out_lda_demo_file = '../../../ExpData/MovieData/LDAData/LDA_Style_Dat/' + movie_type + '_demo.txt'
    generLDADat = GenerateClassicLDABasedDat(in_json_dat_file)
    generLDADat.load_json_file()
    generLDADat.generate_out_dat_lda_file(mode='Doc',
                                          sentiment_word_file = in_senti_word_file,
                                          rare_value=5,
                                          is_need_pruncation = False,
                                          common_value = 0.3,
                                          is_need_processing= True,
                                          out_dat_file = out_lda_dat_file)
    generLDADat.generate_out_demo_lda_file(out_demo_file=out_lda_demo_file)

