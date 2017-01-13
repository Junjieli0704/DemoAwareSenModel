#coding=utf8
import os
import xmlAPI
import usefulAPI

# -------------------------------------------------------------------- #
# 利用频繁项挖掘的方法找出作为名词的评价对象，并且找附近的形容词作为评价词，
# 进而抽取评价短语对
# 添加时间： 2017-01-04 10:17
# 添加时间2： 2017-01-10 15:16
# -------------------------------------------------------------------- #



class DocInfo:
    def __init__(self):
        self.word_list = []
        self.pos_list = []
        self.aspect_list = []
        self.aspect_place_list = []

class AspectExtractBasedOnARM:
    def __init__(self,
                 in_xml_file,
                 minimum_support_value = 0.005,
                 p_support_value = 0.3):
        self.in_xml_file = in_xml_file
        self.doc_info_list = []
        self.minimum_support_value = minimum_support_value
        self.p_support_value = p_support_value

    def load_xml_file(self):
        print 'before load_xml_file ......'
        all_review_list = xmlAPI.load_xml_data(self.in_xml_file)
        print 'after load_xml_file ......'
        for review in all_review_list:
            doc_info = DocInfo()
            doc_info.word_list = review.conForDoc['segmentation'].split(' ')
            doc_info.pos_list = review.conForDoc['postag'].split(' ')
            self.doc_info_list.append(doc_info)

    def print_doc_list(self,out_file):
        out_file_con_list = []
        for doc_info in self.doc_info_list:
            out_file_con_list.append(' '.join(doc_info.word_list))
        open(out_file,'w+').write('\n'.join(out_file_con_list))


if __name__ == '__main__':

    in_movie_dat_xml_file = './OutData/all_dat_Comedy.xml'
    #sentiment_word_file = './Data/sentiment_word_list.txt'
    #nw_adverb_file = './Data/nw_adverb.txt'
    #stop_word_file = './Data/stop_word_list.txt'
    aspect_extract = AspectExtractBasedOnARM(in_xml_file = in_movie_dat_xml_file)
    aspect_extract.load_xml_file()
    aspect_extract.print_doc_list('aaaaa.txt')

