#coding=utf8

# -------------------------------------------------------------------- #
# 描述： 情感词典对这项工作比较重要，除了LDA其他的模型都用到了情感词典，因此完善
#       情感词典是一件非常重要的事情。
# 功能： 对情感词典过滤
# 输入： 原始情感词典 + 电影评论数据
# 输出： 情感词典中出现在电影评论里面超过N次的词汇，进行人工过滤
# 添加时间： 2017-01-04 15:43
# Revise Time: 2017-01-16 16:53
# -------------------------------------------------------------------- #

import os
import sys
sys.path.append("../UsefulLibs")
import usefulAPI, jsonAPI

class FilterSentiWord:
    def __init__(self,in_json_dat_file):
        self.in_json_dat_file = in_json_dat_file
        self.senti_word_2_pola_dict = {}
        self.senti_word_2_times_dict = {}
        self.con_list = []


    def load_json_file(self):
        print 'before load_json_file ......'
        all_review_list = jsonAPI.load_json_movie_dat(self.in_json_dat_file)
        print 'after load_json_file ......'
        for review in all_review_list:
            content = review['con_for_doc_dict']['segmentation']
            self.con_list.append(content)

    def load_sentiment_word(self,senti_word_file):
        if os.path.exists(senti_word_file):
            file_con = open(senti_word_file,'r').readlines()
            for line_con in file_con:
                line_con = line_con.strip()
                word_con_list = line_con.split('\t')
                if len(word_con_list) != 2: continue
                sen_word = word_con_list[0]
                self.senti_word_2_pola_dict[sen_word] = int(word_con_list[1])
                self.senti_word_2_times_dict[sen_word] = 0
            return 1
        else:
            print 'Error! Sentiment word file is not exist.'
            return -1

# -------------------------------------------------------------------- #
# 两种统计方法：
# EachTime --> 出现一次计数加一，统计每个情感词出现了多少次
# EachDoc  --> 每篇文档，每个情感词计数最多加一，统计每个情感词出现了多少篇文档
# 添加时间： 2017-01-04 16:02
# -------------------------------------------------------------------- #
    def count_senti_word(self,mode = 'EachTime'):
        for con in self.con_list:
            word_list = con.split(' ')
            if mode == 'EachDoc':
                word_list = list(set(word_list))
            for word in word_list:
                if self.senti_word_2_times_dict.has_key(word):
                    self.senti_word_2_times_dict[word] = self.senti_word_2_times_dict[word] + 1

    def print_out_word_sort(self,out_file,thres_times = 20):
        out_file_con_list = []
        sort_group_list= sorted(self.senti_word_2_times_dict.iteritems(), key=lambda d:d[1], reverse = True)
        for sort_group in sort_group_list:
            if sort_group[1] <= thres_times: continue
            temp_str = sort_group[0] + '\t' + str(sort_group[1]) + '\t' + str(self.senti_word_2_pola_dict[sort_group[0]])
            out_file_con_list.append(temp_str)
        open(out_file,'w+').write('\n'.join(out_file_con_list))

    def print_con_list(self,out_file):
        out_file_con_list = []
        for content in self.con_list:
            out_file_con_list.append(content)
        open(out_file,'w+').write('\n'.join(out_file_con_list))


# src_sen_file：         原始的情感词典文件
# problem_senti_file：   人工纠正后的情感词典标注
# out_sen_file：         修正后的情感词典文件
# lda_senti_file：       修正后的情感词典文件，LDA形式
def fileter_senti_word(src_sen_file,problem_senti_file,out_sen_file,lda_senti_file):
    error_senti_word_2_pola_dict = {}
    file_con = open(problem_senti_file,'r').readlines()
    for line_con in file_con:
        line_con = line_con.strip()
        word_con_list = line_con.split('\t')
        if len(word_con_list) != 4: continue
        if word_con_list[3] == 'D':
            error_senti_word_2_pola_dict[word_con_list[0]] = 1

    in_file_con_list = open(src_sen_file,'r').readlines()
    out_sen_con_list = []
    out_lda_senti_list = []
    for line_con in in_file_con_list:
        line_con = line_con.replace('\n','').replace('\r','')
        word_con_list = line_con.split('\t')
        if len(word_con_list) != 2: continue
        senti_word = word_con_list[0]
        score = word_con_list[1]
        if error_senti_word_2_pola_dict.has_key(senti_word): continue
        out_sen_con_list.append(line_con)
        if score == '1':
            out_lda_senti_list.append(senti_word + '\t0.05\t0.9\t0.05')
        elif score == '-1':
            out_lda_senti_list.append(senti_word + '\t0.05\t0.05\t0.9')
    open(out_sen_file,'w+').write('\n'.join(out_sen_con_list))
    open(lda_senti_file,'w+').write('\n'.join(out_lda_senti_list))


if __name__ == '__main__':

    in_json_dat_file = '../../../ExpData/MovieData/JsonData/jsonDatForComments.json'
    sentiment_word_file = '../../../ExpData/SentiWordDat/OriginSentiWord/sentiment_word_list.txt'
    filter_senti_word_file = '../../../ExpData/SentiWordDat/ReviseSentiWord/filter_senti_word.txt'

    filter_sen_word = FilterSentiWord(in_json_dat_file = in_json_dat_file)
    filter_sen_word.load_json_file()
    filter_sen_word.load_sentiment_word(sentiment_word_file)
    filter_sen_word.count_senti_word()
    filter_sen_word.print_out_word_sort(filter_senti_word_file)

    # 生成 filter_senti_word_file 文件之后，人工过滤
    # 如果哪一行觉得有问题，添加一下\tD，没有问题就不用管
    # 然后调用 fileter_senti_word 来生成新的情感词典文件

    revise_senti_file = '../../../ExpData/SentiWordDat/ReviseSentiWord/revise_sentiment_word_list.txt'
    lda_senti_file = '../../../ExpData/SentiWordDat/ReviseSentiWord/revise_sentiment_word_list_LDA.txt'
    fileter_senti_word(sentiment_word_file,filter_senti_word_file,revise_senti_file,lda_senti_file)



