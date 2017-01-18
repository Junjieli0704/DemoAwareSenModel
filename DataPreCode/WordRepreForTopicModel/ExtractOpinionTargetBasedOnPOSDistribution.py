#coding=utf8

# -------------------------------------------------------------------- #
# 功能：利用高频和词汇的POS分布来抽取评价对象
#      高频 + POS分布（基本都为名词） --> 优先选为评价对象
#      进而抽取评价短语对
# Revise Time: 2017-01-17 16:11
# -------------------------------------------------------------------- #

import os
import sys
sys.path.append("../UsefulLibs")
import usefulAPI, jsonAPI

class DocInfo:
    def __init__(self):
        self.word_list = []
        self.pos_list = []
        self.aspect_list = []
        self.aspect_place_list = []

class AspectExtractBasedOnARM:
    def __init__(self,
                 in_json_dat_file,
                 minimum_support_value = 0.005,
                 p_support_value = 0.3):
        self.in_json_dat_file = in_json_dat_file
        self.senti_word_dict = {}
        #self.stop_word_dict = {}
        self.neg_adverb_word_dict = {}
        self.doc_info_list = []
        self.minimum_support_value = minimum_support_value
        self.p_support_value = p_support_value
        self.aspect_dict = {}

    def load_json_file(self):
        print 'before load_json_file ......'
        all_review_list = jsonAPI.load_json_movie_dat(self.in_json_dat_file,encoding = 'unicode')
        print 'after load_json_file ......'
        for review in all_review_list:
            doc_info = DocInfo()
            doc_info.word_list = review['con_for_doc_dict']['segmentation'].split(' ')
            doc_info.pos_list = review['con_for_doc_dict']['postag'].split(' ')
            self.doc_info_list.append(doc_info)

    def load_sentiment_word(self,senti_word_file):
        if os.path.exists(senti_word_file):
            file_con = open(senti_word_file,'r').readlines()
            for line_con in file_con:
                line_con = line_con.replace('\n','').replace('\r','')
                word_con_list = line_con.split('\t')
                if len(word_con_list) != 2: continue
                sen_word = word_con_list[0].decode('utf-8')
                self.senti_word_dict[sen_word] = word_con_list[1]
            return 1
        else:
            print "Error! Can't load senti_word_file...."
            return -1
    '''
    def load_stop_word(self,stop_word_file):
        if os.path.exists(stop_word_file):
            file_con = open(stop_word_file,'r').readlines()
            for line_con in file_con:
                line_con = line_con.replace('\n','').replace('\r','')
                self.stop_word_dict[line_con.decode('utf-8')] = 1
            return 1
        else:
            print "Error! Can't load stop_word_file...."
            return -1
    '''
    def get_aspect(self,aspect_number = 150):
        word_to_all_times_dict = {}
        word_to_n_times_dict = {}
        word_to_vj_times_dict = {}
        word_to_other_times_dict = {}

        for doc_info in self.doc_info_list:
            for i in range(0,len(doc_info.word_list)):
                word = doc_info.word_list[i]
                pos = doc_info.pos_list[i]

                self.add_dict_value(word_to_all_times_dict, word)
                self.add_dict_value(word_to_n_times_dict, word, 0)
                self.add_dict_value(word_to_vj_times_dict, word, 0)
                self.add_dict_value(word_to_other_times_dict, word, 0)
                if pos == 'NR' or pos == 'NN':
                    self.add_dict_value(word_to_n_times_dict,word)
                elif pos == 'VV' or pos == 'VE' or pos == 'VA' or pos == 'JJ':
                    self.add_dict_value(word_to_vj_times_dict,word)
                else:
                    self.add_dict_value(word_to_other_times_dict,word)

        word_to_score_dict = {}
        for target,value in word_to_all_times_dict.items():
            value = word_to_n_times_dict[target] - word_to_other_times_dict[target] - word_to_vj_times_dict[target]
            # 单字的评价对象 惩罚为 -10000
            if len(target) == 1: value = -10000
            # 情感词典里的评价对象  惩罚为 -5000
            elif self.senti_word_dict.has_key(target): value = -5000
            # 不是中文的评价对象 惩罚为 -2000
            elif usefulAPI.is_chinese_ustr(target) == False: value = -2000
            #
            # elif self.delete_word_dict.has_key(target): value = -3000
            word_to_score_dict[target] = value

        sorted_word_pair = sorted(word_to_score_dict.iteritems(), key=lambda d:d[1], reverse = True)

        for word_pair in sorted_word_pair:
            word = word_pair[0]
            self.aspect_dict[word] = 1
            if len(self.aspect_dict) >= aspect_number: break

        out_file_list = []
        out_file_list.append('word\tAllTimes\tNNTimes\tVATimes\tOtherTimes\tValue')
        for word_pair in sorted_word_pair:
            word = word_pair[0]
            temp_str_list = []
            temp_str_list.append(word.encode('utf-8'))
            temp_str_list.append(str(word_to_all_times_dict[word]))
            temp_str_list.append(str(word_to_n_times_dict[word]))
            temp_str_list.append(str(word_to_vj_times_dict[word]))
            temp_str_list.append(str(word_to_other_times_dict[word]))
            temp_str_list.append(str(word_to_score_dict[word]))
            out_file_list.append('\t'.join(temp_str_list))
        open('word_nn_sorted.txt','w+').write('\n'.join(out_file_list))


    def load_nw_adverb_word(self,neg_adverb_word_file):
        if os.path.exists(neg_adverb_word_file):
            file_con = open(neg_adverb_word_file,'r').readlines()
            for line_con in file_con:
                line_con = line_con.replace('\n','').replace('\r','')
                word_con_list = line_con.split('\t')
                if len(word_con_list) != 2: continue
                self.neg_adverb_word_dict[word_con_list[0].decode('utf-8')] = word_con_list[1]
            return 1
        else:
            print "Error! Can't load neg_adverb_word_file...."
            return -1

    def add_dict_value(self,dict,key,value = 1):
        if dict.has_key(key):
            dict[key] = dict[key] + value
        else:
            dict[key] = value

    # 输出从json文件导入的文本内容，仅仅用来测试
    # 如果json文件读入的方式是 utf-8, 这个测试函数没问题
    #                       unicode, 这个测试函数会报错
    def print_doc_list(self,out_file):
        out_file_con_list = []
        for doc_info in self.doc_info_list:
            out_file_con_list.append(' '.join(doc_info.word_list))
        open(out_file,'w+').write('\n'.join(out_file_con_list))

    def print_aspect_dict(self,out_file):
        out_file_con_list = []
        for key,value in self.aspect_dict.items():
            out_file_con_list.append(key.encode('utf-8'))
        open(out_file,'w+').write('\n'.join(out_file_con_list))



if __name__ == '__main__':

    movie_type = 'Comedy'
    in_json_dat_file = '../../../ExpData/MovieData/JsonDatForEachCat/' + movie_type + '.json'
    senti_word_file = '../../../ExpData/SentiWordDat/ReviseSentiWord/revise_sentiment_word_list.txt'
    aspect_extract = AspectExtractBasedOnARM(in_json_dat_file = in_json_dat_file)
    aspect_extract.load_json_file()
    aspect_extract.load_sentiment_word(senti_word_file)
    aspect_extract.get_aspect()
    aspect_extract.print_aspect_dict('aspect_dict.txt')


