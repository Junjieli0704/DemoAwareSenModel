#coding=utf8
import os
import xmlAPI
import usefulAPI

# -------------------------------------------------------------------- #
# 过滤情感词典
# 输入 原始情感词典 + 电影评论数据
# 输出 情感词典中出现在电影评论里面超过N次的词汇，进行人工过滤
# 添加时间： 2017-01-04 15:43
# -------------------------------------------------------------------- #


class FilterSentiWord:
    def __init__(self,in_xml_file):
        self.in_xml_file = in_xml_file
        self.senti_word_2_pola_dict = {}
        self.senti_word_2_times_dict = {}
        self.con_list = []


    def load_xml_file(self):
        print 'before load_xml_file ......'
        all_review_list = xmlAPI.load_xml_data(self.in_xml_file)
        print 'after load_xml_file ......'
        for review in all_review_list:
            content = review.conForDoc['segmentation']
            # 由于通过xml读入，此内容变成unicode编码的了
            # 可以通过，isinstance(content,unicode) 测试
            self.con_list.append(content)


    def load_sentiment_word(self,senti_word_file):
        if os.path.exists(senti_word_file):
            file_con = open(senti_word_file,'r').readlines()
            for line_con in file_con:
                line_con = line_con.replace('\n','').replace('\r','')
                word_con_list = line_con.split('\t')
                if len(word_con_list) != 2: continue
                # 由于前面xml文件读入的问题，已经将内容变成了unicode编码，因此这里也需要进行解码操作
                sen_word = word_con_list[0].decode('utf-8')
                self.senti_word_2_pola_dict[sen_word] = int(word_con_list[1])
                self.senti_word_2_times_dict[sen_word] = 0

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

    def print_out_word_sort(self,out_file):
        out_file_con_list = []
        sort_group_list= sorted(self.senti_word_2_times_dict.iteritems(), key=lambda d:d[1], reverse = True)
        for sort_group in sort_group_list:
            temp_str = sort_group[0] + '\t' + str(sort_group[1]) + '\t' + str(self.senti_word_2_pola_dict[sort_group[0]])
            out_file_con_list.append(temp_str)
        open(out_file,'w+').write('\n'.join(out_file_con_list))

    def print_con_list(self,out_file):
        out_file_con_list = []
        for content in self.con_list:
            out_file_con_list.append(content)
        open(out_file,'w+').write('\n'.join(out_file_con_list))



def fileter_senti_word(src_sen_file,problem_senti_file,out_sen_file,lda_senti_file):

    error_senti_word_2_pola_dict = {}
    file_con = open(problem_senti_file,'r').readlines()
    for line_con in file_con:
        line_con = line_con.replace('\n','').replace('\r','')
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
    '''
    in_movie_dat_xml_file = './OutData/all_dat.xml'
    sentiment_word_file = './Data/sentiment_word_list.txt'
    #nw_adverb_file = './Data/nw_adverb.txt'
    #stop_word_file = './Data/stop_word_list.txt'
    filter_sen_word = FilterSentiWord(in_xml_file = in_movie_dat_xml_file)
    filter_sen_word.load_xml_file()
    filter_sen_word.load_sentiment_word(sentiment_word_file)
    filter_sen_word.count_senti_word()
    filter_sen_word.print_out_word_sort('filt_sen_word.txt')
    filter_sen_word.print_con_list('con_sen.txt')
    '''
    src_sen_file = './Data/SentiWord/sentiment_word_list.txt'
    problem_senti_file = './Data/SentiWord/problem_senword.txt'
    out_sen_file = './Data/SentiWord/sentiment_word_list_human_check_freqWords.txt'
    lda_senti_file = './Data/SentiWord/sentiment_word_list_LDA.txt'
    fileter_senti_word(src_sen_file,problem_senti_file,out_sen_file,lda_senti_file)


