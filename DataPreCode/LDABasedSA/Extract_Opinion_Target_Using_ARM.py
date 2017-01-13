__author__ = 'Jun'
#coding=utf8
import os
import xmlAPI

def is_chinese(uchar):
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False

def detect_chinese_uchar(in_uchar):
    is_chinese_uchar = True
    for uchar in in_uchar:
        if is_chinese(uchar): continue
        else:
            is_chinese_uchar = False
            break
    return is_chinese_uchar


class sentenceInfo:
    def __init__(self):
        self.word_list = []
        self.pos_list = []
        self.aspect_dict = {}



class AspectExtractBasedOnARM:
    def __init__(self,
                 in_review_file = '',
                 sentiment_word_file = '',
                 nw_adverb_file = '',
                 stop_word_file = '',
                 minimum_support_value = 0.005,
                 p_support_value = 0.3):
        self.in_review_file = in_review_file
        self.sentiment_word_file = sentiment_word_file
        self.nw_adverb_file = nw_adverb_file
        self.stop_word_file = stop_word_file
        self.senti_word_dict = {}
        self.nw_adverb_dict = {}
        self.stop_word_dict = {}
        self.delete_word_dict = {}              # delete low frequency word
        self.all_sentence_list = []             # each sentence object is a sentenceInfo
        self.aspect_dict = {}
        self.minimum_support_value = minimum_support_value
        self.p_support_value = p_support_value

    def load_all_sentence(self):
        if os.path.exists(self.in_review_file) is False:
            print 'load_all_sentence Failed......'
            return False

        print 'before load_xml_file ......'
        all_dat_list = xmlAPI.load_xml_data(self.in_review_file)
        print 'after load_xml_file ......'

        for temp_dat in all_dat_list:
            sen_info = sentenceInfo()
            sen_info.word_list = temp_dat.conForDoc['segmentation'].split(' ')
            sen_info.pos_list = temp_dat.conForDoc['postag'].split(' ')
            self.all_sentence_list.append(sen_info)
        return True

    def load_sentiment_word(self):
        if os.path.exists(self.sentiment_word_file):
            file_con = open(self.sentiment_word_file,'r').readlines()
            for line_con in file_con:
                line_con = line_con.replace('\n','').replace('\r','')
                word_con_list = line_con.split('\t')
                if len(word_con_list) != 2: continue
                sen_word = word_con_list[0].decode('utf-8')
                self.senti_word_dict[sen_word] = word_con_list[1]

    def load_stop_word(self):
        if os.path.exists(self.stop_word_file):
            file_con = open(self.stop_word_file,'r').readlines()
            for line_con in file_con:
                line_con = line_con.replace('\n','').replace('\r','')
                self.stop_word_dict[line_con.decode('utf-8')] = 1

    def load_nw_adverb_word(self):
        if os.path.exists(self.nw_adverb_file):
            file_con = open(self.nw_adverb_file,'r').readlines()
            for line_con in file_con:
                line_con = line_con.replace('\n','').replace('\r','')
                word_con_list = line_con.split('\t')
                if len(word_con_list) != 2: continue
                self.nw_adverb_dict[word_con_list[0].decode('utf-8')] = word_con_list[1]

    def add_dict_value(self,dict,key,value = 1):
        if dict.has_key(key):
            dict[key] = dict[key] + value
        else:
            dict[key] = value

    def delete_low_fre_and_stop_word(self,fre_value = 1, is_need_delete_stop_word = True):
        word_count_dict = {}
        for sen_info in self.all_sentence_list:
            for i in range(0,len(sen_info.word_list)):
                word = sen_info.word_list[i]
                pos = sen_info.pos_list[i]
                if pos == 'VA': continue
                if self.senti_word_dict.has_key(word): continue
                if self.nw_adverb_dict.has_key(word): continue
                if self.aspect_dict.has_key(word): continue
                self.add_dict_value(word_count_dict, word)
        for word,value in word_count_dict.items():
            if value <= fre_value:
                self.delete_word_dict[word] = 1

        for sen_info in self.all_sentence_list:
            new_word_list = []
            new_pos_list = []
            for i in range(0,len(sen_info.word_list)):
                word = sen_info.word_list[i]
                pos = sen_info.pos_list[i]
                if self.delete_word_dict.has_key(word): continue
                if is_need_delete_stop_word:
                    if self.stop_word_dict.has_key(word):
                        continue
                new_word_list.append(word)
                new_pos_list.append(pos)
            sen_info.word_list = new_word_list
            sen_info.pos_list = new_pos_list

    def get_aspect(self,aspect_number = 150):
        word_to_all_times_dict = {}
        word_to_n_times_dict = {}
        word_to_vj_times_dict = {}
        word_to_other_times_dict = {}

        for sen_info in self.all_sentence_list:
            #print len(sen_info.word_list)
            for i in range(0,len(sen_info.word_list)):
                word = sen_info.word_list[i]
                pos = sen_info.pos_list[i]

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
            if len(target) == 1: value = -10000
            elif detect_chinese_uchar(target) == False: value = -2000
            elif self.senti_word_dict.has_key(target): value = -5000
            elif self.delete_word_dict.has_key(target): value = -3000
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
            temp_str_list.append(word)
            temp_str_list.append(str(word_to_all_times_dict[word]))
            temp_str_list.append(str(word_to_n_times_dict[word]))
            temp_str_list.append(str(word_to_vj_times_dict[word]))
            temp_str_list.append(str(word_to_other_times_dict[word]))
            temp_str_list.append(str(word_to_score_dict[word]))
            #temp_str_list.append(str(detect_chinese_uchar(word)))
            out_file_list.append('\t'.join(temp_str_list))
        open('word_nn_sorted.txt','w+').write('\n'.join(out_file_list))

    def get_aspect_phrase(self):
        aspect_phrase_2_times = {}
        aspect_2_times = {}
        for sen_info in self.all_sentence_list:
            for i in range(0,len(sen_info.word_list)):
                if sen_info.aspect_dict.has_key(sen_info.word_list[i]):
                    self.add_dict_value(aspect_2_times,sen_info.word_list[i])

                if i + 1 < len(sen_info.word_list):
                    if sen_info.aspect_dict.has_key(sen_info.word_list[i]) and sen_info.aspect_dict.has_key(sen_info.word_list[i+1]):
                        aspect_phrase = sen_info.word_list[i] + sen_info.word_list[i+1]
                        self.add_dict_value(aspect_phrase_2_times,aspect_phrase,1)

                if i + 2 < len(sen_info.word_list):
                    word_i = sen_info.word_list[i]
                    word_i1 = sen_info.word_list[i+1]
                    pos_i1 = sen_info.pos_list[i+1]
                    word_i2 = sen_info.word_list[i+2]
                    if sen_info.aspect_dict.has_key(word_i1) and sen_info.aspect_dict.has_key(word_i2):
                        aspect_phrase = word_i1 + word_i2
                        self.add_dict_value(aspect_phrase_2_times,aspect_phrase,1)
                    if sen_info.aspect_dict.has_key(word_i) and sen_info.aspect_dict.has_key(word_i1):
                        aspect_phrase = word_i + word_i1
                        self.add_dict_value(aspect_phrase_2_times,aspect_phrase,1)
                    if sen_info.aspect_dict.has_key(word_i) and sen_info.aspect_dict.has_key(word_i1) and sen_info.aspect_dict.has_key(word_i2):
                        aspect_phrase = word_i + word_i1 + word_i2
                        self.add_dict_value(aspect_phrase_2_times,aspect_phrase,1)
                    if sen_info.aspect_dict.has_key(word_i) and pos_i1 == 'DEC' and sen_info.aspect_dict.has_key(word_i2):
                        aspect_phrase = word_i + word_i1 + word_i2
                        self.add_dict_value(aspect_phrase_2_times,aspect_phrase,1)

        out_file_list = []
        sorted_word_pair = sorted(aspect_phrase_2_times.iteritems(), key=lambda d:d[1], reverse = True)
        for word_pair in sorted_word_pair:
            out_file_list.append(word_pair[0] + '\t' + str(word_pair[1]))
        open('aspect_phrase2.txt','w+').write('\n'.join(out_file_list))

        out_file_list = []
        sorted_word_pair = sorted(aspect_2_times.iteritems(), key=lambda d:d[1], reverse = True)
        for word_pair in sorted_word_pair:
            out_file_list.append(word_pair[0] + '\t' + str(word_pair[1]))
        open('aspect_sorted.txt','w+').write('\n'.join(out_file_list))


    def get_sen_aspect(self):
        word_to_all_times_dict = {}
        word_to_n_times_dict = {}
        word_to_vj_times_dict = {}
        word_to_other_times_dict = {}

        for sen_info in self.all_sentence_list:
            for i in range(0,len(sen_info.word_list)):
                word = sen_info.word_list[i]
                pos = sen_info.pos_list[i]
                self.add_dict_value(word_to_all_times_dict,word)
                self.add_dict_value(word_to_n_times_dict,word,0)
                self.add_dict_value(word_to_vj_times_dict,word,0)
                self.add_dict_value(word_to_other_times_dict,word,0)
                if pos == 'NR' or pos == 'NN':
                    self.add_dict_value(word_to_n_times_dict,word)
                elif pos == 'VV' or pos == 'VE' or pos == 'VA' or pos == 'JJ':
                    self.add_dict_value(word_to_vj_times_dict,word)
                else:
                    self.add_dict_value(word_to_other_times_dict,word)

        word_to_score_dict = {}
        for target,value in word_to_all_times_dict.items():
            value = word_to_n_times_dict[target] - word_to_other_times_dict[target] - word_to_vj_times_dict[target]
            if len(target) <= 3: value = -10000
            if self.senti_word_dict.has_key(target): value = -5000
            word_to_score_dict[target] = value



        sorted_word_pair = sorted(word_to_score_dict.iteritems(), key=lambda d:d[1], reverse = True)
        word_2_order_dict = {}
        for i in range(0,len(sorted_word_pair)):
            order = i + 1
            word_2_order_dict[sorted_word_pair[i][0]] = order

        for sen_info in self.all_sentence_list:
           sen_noun_dict = {}
           for i in range(0,len(sen_info.word_list)):
               word = sen_info.word_list[i]
               pos = sen_info.pos_list[i]
               if pos == 'NN' or pos == 'NR':
                   sen_noun_dict[word] = word_to_score_dict[word]
           sorted_word_pair = sorted(sen_noun_dict.iteritems(), key=lambda d:d[1], reverse = True)
           for word_pair in sorted_word_pair:
               if word_2_order_dict[word_pair[0]] <= 150:
                   sen_info.aspect_dict[word_pair[0]] = 1
           print sen_info.aspect_dict



if __name__ == '__main__':

    in_review_file = './OutData/all_dat.xml'
    sentiment_word_file = './Data/sentiment_word_list.txt'
    nw_adverb_file = './Data/nw_adverb.txt'
    stop_word_file = './Data/stop_word_list.txt'
    aspect_extract = AspectExtractBasedOnARM(in_review_file = in_review_file,
                                             sentiment_word_file = sentiment_word_file,
                                             nw_adverb_file = nw_adverb_file,
                                             stop_word_file = stop_word_file)

    aspect_extract.load_all_sentence()
    aspect_extract.load_sentiment_word()
    aspect_extract.load_nw_adverb_word()
    aspect_extract.load_stop_word()
    aspect_extract.get_aspect()
    aspect_extract.delete_low_fre_and_stop_word(is_need_delete_stop_word=True)


    #aspect_extract.delete_low_fre_word()
    aspect_extract.get_sen_aspect()
    #aspect_extract.get_sen_aspect_and_context()
    #aspect_extract.print_sen_aspect_and_context()
    #aspect_extract.print_sen_content_with_aspect()
    #aspect_extract.print_sen_sentiword()
