#coding=utf8

# -------------------------------------------------------------------- #
# 功能：利用频繁项挖掘的方法找出作为名词的评价对象，并且找附近的形容词作为评价词，
#      进而抽取评价短语对
# Revise Time: 2017-01-18 17:07
# -------------------------------------------------------------------- #

import os
import sys
sys.path.append("../UsefulLibs")
import usefulAPI, jsonAPI

class DocInfo:
    def __init__(self):
        self.word_list = []
        self.pos_list = []


class AspectExtractBasedOnARM:
    def __init__(self,
                 in_json_dat_file,
                 connect_str = ' ',
                 min_support_value = 0.005,
                 min_p_support_value = 3):
        self.in_json_dat_file = in_json_dat_file
        self.doc_info_list = []
        self.min_support_value = min_support_value
        self.connect_str = connect_str
        self.senti_word_dict = {}
        self.min_p_support_value = min_p_support_value
        self.aspect_dict = {}
        self.noun_to_dociddict_dict = {}             #类似倒排索引的方法找出每个名词对应的doc_list列表

    def load_json_file(self):
        print 'load_json_file begin......'
        all_review_list = jsonAPI.load_json_movie_dat(self.in_json_dat_file,encoding = 'unicode')
        print 'load_json_file end......'
        for review in all_review_list:
            doc_info = DocInfo()
            doc_info.word_list = review['con_for_doc_dict']['segmentation'].split(' ')
            doc_info.pos_list = review['con_for_doc_dict']['postag'].split(' ')
            self.doc_info_list.append(doc_info)

    def add_word_to_dict(self,word,doc_id):
        if self.noun_to_dociddict_dict.has_key(word):
            if self.noun_to_dociddict_dict[word].has_key(doc_id) == False:
                self.noun_to_dociddict_dict[word][doc_id] = 1
        else:
            self.noun_to_dociddict_dict[word] = {}
            self.noun_to_dociddict_dict[word][doc_id] = 1

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

    def get_seq_word_list(self,word_list,pos_list,i,ngram = 'uni',connect_str = '-*-'):
        if ngram == 'uni':
            return word_list[i], pos_list[i]
        elif ngram == 'bi' and i >= 1:
            word_str = word_list[i - 1] + connect_str + word_list[i]
            pos_str =  pos_list[i - 1] + connect_str + pos_list[i]
            return word_str,pos_str
        elif ngram == 'tri' and i >= 2:
            word_str = word_list[i - 2] + connect_str + word_list[i - 1] + connect_str + word_list[i]
            pos_str =  pos_list[i - 2] + connect_str + pos_list[i - 1] + connect_str + pos_list[i]
            return word_str, pos_str
        else:
            return 'NULL','NULL'

    def is_add_str_to_dict(self,word_str,pos_str,connect_str):
        word_list = word_str.split(connect_str)
        pos_list = pos_str.split(connect_str)
        is_contain_PU = False
        is_len_great_one = False #里面至少有一个词汇，长度大于1
        for word in word_list:
            if len(word) > 1: is_len_great_one = True
        if len(word_list) == 1:
            is_chinese_char = usefulAPI.is_chinese_ustr(word_str)
        else:
            is_chinese_char = True
        is_all_in_senti_word_dict = True
        for word in word_list:
            if self.senti_word_dict.has_key(word) == False:
                is_all_in_senti_word_dict = False
        is_contain_all_noun = True
        for pos in pos_list:
            if pos != 'NN' and pos != 'NR': is_contain_all_noun = False
            if pos == 'PU': is_contain_PU = True
        if is_len_great_one == False or is_chinese_char == False or \
                is_all_in_senti_word_dict or is_contain_all_noun == False or is_contain_PU:
                return False
        return True

    def generate_noun_to_doc_list_dict(self):
        print 'generate_noun_to_doc_list_dict begin......'
        for doc_id in range(0,len(self.doc_info_list)):
            if doc_id % 1000 == 0:
                print str(doc_id) + ' / ' + str(len(self.doc_info_list))
            doc_info = self.doc_info_list[doc_id]
            for i in range(0,len(doc_info.word_list)):
                # 通过 bi tri 抽取评价对象组合实际上也就是做 Compactness pruning
                gram_list = ['uni','bi','tri']
                for gram in gram_list:
                    word_str, pos_str = self.get_seq_word_list(doc_info.word_list,doc_info.pos_list,i,gram,self.connect_str)
                    if word_str == 'NULL' and pos_str == 'NULL': continue
                    if self.is_add_str_to_dict(word_str,pos_str,connect_str):
                        self.add_word_to_dict(word_str,doc_id)
        print 'generate_noun_to_doc_list_dic end......'

    def redundancy_pruning(self):
        print 'redundancy pruning begin......'
        noun_to_p_support_dict = {}
        noun_phrase_to_len_dict = {}

        # 计算该名词自己的 p_support 值
        for noun, doc_id_dict in self.noun_to_dociddict_dict.items():
            if len(doc_id_dict) < len(self.doc_info_list) * self.min_support_value: continue
            if noun.find(self.connect_str) == -1:
                noun_to_p_support_dict[noun] = len(doc_id_dict)
            else:
                noun_phrase_to_len_dict[noun] = len(doc_id_dict)

        # 更新该名词的 p_support 值 = 将该名词自己的 p_support 值 - 该名词 superset 的 p_support
        noun_to_p_support_new_dict = {}
        for noun, p_support in noun_to_p_support_dict.items():
            for noun_phrase, len_value in noun_phrase_to_len_dict.items():
                if noun_phrase.find(noun) == -1: continue
                p_support = p_support - len_value
            noun_to_p_support_new_dict[noun] = p_support

        # 与设定阈值比较，小于阈值的名词舍弃
        for noun,p_old_support in noun_to_p_support_dict.items():
            if noun_to_p_support_new_dict[noun] < self.min_p_support_value:
                self.noun_to_dociddict_dict[noun] = {}

        print 'redundancy pruning end......'

    def generate_aspect(self):
        for noun, doc_id_dict in self.noun_to_dociddict_dict.items():
            if len(doc_id_dict) >= len(self.doc_info_list) * self.min_support_value:
                self.aspect_dict[noun] = len(doc_id_dict)

    def print_aspect_dict(self,out_file):
        out_file_con_list = []
        for key,value in self.aspect_dict.items():
            out_file_con_list.append(key.encode('utf-8') + '\t' + str(value))
        open(out_file,'w+').write('\n'.join(out_file_con_list))

if __name__ == '__main__':
    movie_type = 'Comedy'
    in_json_dat_file = '../../../ExpData/MovieData/JsonDatForEachCat/' + movie_type + '.json'
    senti_word_file = '../../../ExpData/SentiWordDat/ReviseSentiWord/revise_sentiment_word_list.txt'
    connect_str = ' '
    aspect_extract = AspectExtractBasedOnARM(in_json_dat_file = in_json_dat_file,
                                             connect_str=connect_str,
                                             min_p_support_value=3,
                                             min_support_value=0.01)
    aspect_extract.load_json_file()
    aspect_extract.load_sentiment_word(senti_word_file)
    aspect_extract.generate_noun_to_doc_list_dict()
    aspect_extract.generate_aspect()
    aspect_extract.redundancy_pruning()
    aspect_extract.print_aspect_dict('ttttt.txt')



