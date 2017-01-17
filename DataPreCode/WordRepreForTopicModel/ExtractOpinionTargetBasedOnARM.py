#coding=utf8

# -------------------------------------------------------------------- #
# 功能：利用频繁项挖掘的方法找出作为名词的评价对象，并且找附近的形容词作为评价词，
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
        self.doc_info_list = []
        self.minimum_support_value = minimum_support_value
        self.p_support_value = p_support_value

    def load_json_file(self):
        print 'before load_json_file ......'
        all_review_list = jsonAPI.load_json_movie_dat(self.in_json_dat_file)
        print 'after load_json_file ......'
        for review in all_review_list:
            doc_info = DocInfo()
            doc_info.word_list = review['con_for_doc_dict']['segmentation'].split(' ')
            doc_info.pos_list = review['con_for_doc_dict']['postag'].split(' ')
            self.doc_info_list.append(doc_info)

    def print_doc_list(self,out_file):
        out_file_con_list = []
        for doc_info in self.doc_info_list:
            out_file_con_list.append(' '.join(doc_info.word_list))
        open(out_file,'w+').write('\n'.join(out_file_con_list))


if __name__ == '__main__':

    movie_type = 'Comedy'
    in_json_dat_file = '../../../ExpData/MovieData/JsonDatForEachCat/' + movie_type + '.json'
    aspect_extract = AspectExtractBasedOnARM(in_json_dat_file = in_json_dat_file)
    aspect_extract.load_json_file()
    aspect_extract.print_doc_list('aaaaa.txt')

