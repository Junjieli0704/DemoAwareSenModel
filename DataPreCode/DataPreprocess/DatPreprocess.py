#encoding=utf-8


# -------------------------------------------------------------------- #
# 对数据进行预处理的文件，包含功能：
#   - 删除相似句子
#   - 删除乱码句子
#   - 按照句号切分句子
#   - 导入切分好的句子的依存分析结果
#   - 整合收集seg，pos和dep的结果，到一个json文件中
# Time: 2017-02-25
# -------------------------------------------------------------------- #

import sys
sys.path.append("../UsefulLibs")
import usefulAPI, xmlAPI, jsonAPI




def get_dat_struct_dict():
    struct_dict = {}
    struct_dict['comment_id'] = ''
    struct_dict['user_id'] = ''
    struct_dict['movie_name'] = ''
    struct_dict['senti_label'] = ''
    struct_dict['user_info'] = ''
    struct_dict['movie_type'] = ''
    struct_dict['is_delete'] = False
    struct_dict['content_raw'] = ''
    struct_dict['content_seg'] = []
    return struct_dict

def get_sen_dict():
    sen_dict = {}
    sen_dict['dep'] = ''
    sen_dict['seg'] = ''
    sen_dict['raw'] = ''
    sen_dict['pos'] = ''
    return sen_dict

def get_doc_dict():
    doc_dict = {}
    doc_dict['raw_con'] = ''
    doc_dict['sen_list'] = []
    return doc_dict

class PropressingDat:

    def __init__(self,movie_comment_file,movie_info_file):
        self.movie_comment_file = movie_comment_file
        self.movie_info_file = movie_info_file
        self.all_dat_list = []
        self.movie_name_to_type_dict = {}

    def load_movie_dat_info(self):
        line_con_list = open(self.movie_info_file,'r').readlines()
        for line_con in line_con_list:
            line_con = line_con.replace('\n','').replace('\r','')
            word_con_list = line_con.split('\t')
            if len(word_con_list) != 11: continue
            movie_name_eng = word_con_list[0].replace(' ','_')
            movie_type = word_con_list[3]
            if self.movie_name_to_type_dict.has_key(movie_name_eng):
                continue
            self.movie_name_to_type_dict[movie_name_eng] = movie_type

    def load_data_struct(self):
        line_con_list = open(self.movie_comment_file,'r').readlines()
        for line_con in line_con_list:
            #line_con = line_con.strip().decode('utf-8').encode('utf-8')
            line_con = line_con.strip()
            word_con_list = line_con.split('\t')
            if len(word_con_list) != 6: continue
            if word_con_list[0] == 'CommentID': continue
            temp_struct = get_dat_struct_dict()
            temp_struct['comment_id'] = word_con_list[0]
            temp_struct['user_id'] = word_con_list[1]
            temp_struct['movie_name'] = word_con_list[2]
            temp_struct['user_info'] = word_con_list[3]
            temp_struct['senti_label'] = word_con_list[4]
            temp_struct['movie_type'] = self.movie_name_to_type_dict[temp_struct['movie_name']]
            temp_struct['content_raw'] = word_con_list[5]
            #if self.get_user_info_no_null_times(temp_struct['user_info']) == 0:
            #    temp_struct['is_delete'] = True

            self.all_dat_list.append(temp_struct)
        print "load_data_struct() finished......"

    def get_user_info_no_null_times(self,user_info_str):
        no_null_times = 0
        for temp_str in user_info_str.split('_'):
            if temp_str.split('/')[1] != 'NULL':
                if temp_str.split('/')[0] != 'Label':
                    no_null_times = no_null_times + 1
        return no_null_times

    def get_data_info_str(self,temp_dat,data_info_mode = ''):
        if data_info_mode == 'raw':
            return temp_dat['content_raw']
        elif data_info_mode == 'all':
            temp_list = []
            temp_list.append(temp_dat['comment_id'])
            temp_list.append(temp_dat['user_id'])
            temp_list.append(temp_dat['movie_name'])
            temp_list.append(temp_dat['user_info'])
            temp_list.append(temp_dat['senti_label'])
            temp_list.append(temp_dat['content_raw'])
            return '\t'.join(temp_list)

    def print_out_dat_info(self,out_file,data_info_mode = 'raw'):
        out_line_con_list = []
        if data_info_mode == 'all':
            out_line_con_list.append('CommentID\tUserID\tMovieName\tUserInfo\tSentiLabel\tMovieComment')
        for temp_dat in self.all_dat_list:
            if temp_dat['is_delete']: continue
            out_line_con_list.append(self.get_data_info_str(temp_dat,data_info_mode))
        open(out_file,'w+').write('\n'.join(out_line_con_list))

    def load_word_seg_file(self,in_file):
        line_con_list = open(in_file,'r').readlines()
        if len(line_con_list) == len(self.all_dat_list):
            for i in range(0,len(line_con_list)):
                self.all_dat_list[i]['content_seg'] = line_con_list[i].strip().split(' ')

    def compute_two_list_simi_score(self,word_list_1,word_list_2,is_need_print = False):
        word_list_1 = list(set(word_list_1))
        word_list_2 = list(set(word_list_2))
        same_word_list = word_list_1 + word_list_2
        same_word_list = list(set(same_word_list))
        res = float(len(same_word_list)) / float(len(word_list_1) + len(word_list_2))
        if res <= 0.5 and is_need_print:
            print ' '.join(word_list_1).decode('utf-8')
            print ' '.join(word_list_2).decode('utf-8')
            print len(same_word_list)
            print len(word_list_1)
            print len(word_list_2)
            print res
        return res

    # -------------------------------------------------- #
    # 找到分过词的句子中特别相似，简直到相同的句子，然后将其删除
    # Time: 2017-02-22
    # -------------------------------------------------- #
    def delete_simi_sen(self,simi_file = 'simi.txt'):
        comment_id_to_word_list_dict = {}
        movie_name_to_comment_id_list_dict = {}
        for temp_dat in self.all_dat_list:
            movie_name = temp_dat['movie_name']
            if movie_name_to_comment_id_list_dict.has_key(movie_name) == False:
                movie_name_to_comment_id_list_dict[movie_name] = []
            comment_id_str = temp_dat['comment_id']
            movie_name_to_comment_id_list_dict[movie_name].append(comment_id_str)
            comment_id_to_word_list_dict[comment_id_str] = temp_dat['content_seg']

        comment_id_to_group_comment_id_dict = {}
        movie_num = 1
        for movie_name, comment_id_str_list in movie_name_to_comment_id_list_dict.items():
            print str(movie_num) + ' / ' + str(len(movie_name_to_comment_id_list_dict.items())) + ' --> ' + movie_name
            for i in range(0,len(comment_id_str_list)):
                if i % 100 == 0: print str(i) + ' / ' + str(len(comment_id_str_list))
                for j in range(i+1,len(comment_id_str_list)):
                    fir_id_str = comment_id_str_list[i]
                    sec_id_str = comment_id_str_list[j]
                    fir_id_con = comment_id_to_word_list_dict[fir_id_str]
                    sec_id_con = comment_id_to_word_list_dict[sec_id_str]
                    score = self.compute_two_list_simi_score(fir_id_con,sec_id_con)
                    if score <= 0.6:
                        is_find_fir_id_str = comment_id_to_group_comment_id_dict.has_key(fir_id_str)
                        is_find_sec_id_str = comment_id_to_group_comment_id_dict.has_key(sec_id_str)
                        if is_find_fir_id_str and is_find_sec_id_str: continue
                        elif is_find_fir_id_str and is_find_sec_id_str == False:
                            comment_id_to_group_comment_id_dict[sec_id_str] = comment_id_to_group_comment_id_dict[fir_id_str]
                        elif is_find_sec_id_str and is_find_fir_id_str == False:
                            comment_id_to_group_comment_id_dict[fir_id_str] = comment_id_to_group_comment_id_dict[sec_id_str]
                        elif is_find_fir_id_str == False and is_find_sec_id_str == False:
                            comment_id_to_group_comment_id_dict[sec_id_str] = fir_id_str
            movie_num = movie_num + 1

        group_comment_id_to_comment_id_list_dict = {}
        for comment_id,group_comment_id in comment_id_to_group_comment_id_dict.items():
            if group_comment_id_to_comment_id_list_dict.has_key(group_comment_id) == False:
                group_comment_id_to_comment_id_list_dict[group_comment_id] = []
            group_comment_id_to_comment_id_list_dict[group_comment_id].append(comment_id)

        # 在 simi_file 中 输出相似句子
        out_file_con_list = []
        for group_comment_id, comment_id_list in group_comment_id_to_comment_id_list_dict.items():
            out_file_con_list.append('-------------------------------------------------------------')
            out_file_con_list.append(group_comment_id + '\t-->\t' + ' '.join(comment_id_list))
            out_file_con_list.append(group_comment_id + '\t' + str(' '.join(comment_id_to_word_list_dict[group_comment_id])))
            for temp_comment_id in comment_id_list:
                out_file_con_list.append(temp_comment_id + '\t' + str(' '.join(comment_id_to_word_list_dict[temp_comment_id])))
        open(simi_file,'w+').write('\n'.join(out_file_con_list))

        # 在 dele_file 中 输出要删除的
        dele_comment_id_dict = {}
        for group_id, id_list in group_comment_id_to_comment_id_list_dict.items():
            dele_comment_id_dict[group_id] = 1
            for temp_id in id_list:
                dele_comment_id_dict[temp_id] = 1

        for temp_dat in self.all_dat_list:
            if dele_comment_id_dict.has_key(temp_dat['comment_id']):
                temp_dat['is_delete'] = True

    def delete_encoding_error_sen(self):
        for temp_dat in self.all_dat_list:
            #print temp_dat['content_raw'].decode('utf-8')
            #print temp_dat['content_raw'].decode('utf-8')
            #print s[0]
            try:
                print temp_dat['content_raw'].decode('utf-8')
            except:
                temp_dat['is_delete'] = True

# -----------------------------------------------------------
# 从原始的数据中删除两类评论
#   1. 重复的评论删掉
#   2. utf-8 encode error的评论删掉，这样的句子会出现不知所谓的方框
# -----------------------------------------------------------
def delete_same_encode_error_sen():
    in_raw_dat_filefold = '../../../ExpData/MovieData/RawData/'
    in_movie_struct_file = in_raw_dat_filefold + 'Raw/MovieStructDataForComments.txt'
    in_movie_info_file = in_raw_dat_filefold + 'Raw/MovieInfo.txt'
    raw_content_file = in_raw_dat_filefold + 'Raw/RawSenDataForComments.txt'

    preDat = PropressingDat(in_movie_struct_file,in_movie_info_file)
    preDat.load_movie_dat_info()
    preDat.load_data_struct()
    preDat.print_out_dat_info(raw_content_file)

    # 用分词工具将 raw_content_file 给分词 并输出到 --> seg_content_file
    seg_content_file = in_raw_dat_filefold + 'Urheen_Res/RawSenDataForComments_Urheen_seg.txt'
    # 再导入分词结果
    preDat.load_word_seg_file(seg_content_file)
    delete_same_encode_error_file = in_raw_dat_filefold + 'Raw/MovieStructDataForComments_DeleteSameEncodeError.txt'
    # 再依据分词结果删除相同的句子
    preDat.delete_simi_sen()
    preDat.delete_encoding_error_sen()
    preDat.print_out_dat_info(delete_same_encode_error_file,data_info_mode = 'all')

# -----------------------------------------------------------
# ~ 分词也会出错，于是把~替换成。#
# -----------------------------------------------------------
def word_file_preprocessing(raw_content_file):
    line_con_list = open(raw_content_file,'r').readlines()
    out_list = []
    for line_con in line_con_list:
        line_con = line_con.strip().replace('~','。').replace('～','。')
        line_con = line_con.replace('…','。')
        out_list.append(line_con)
    open(raw_content_file,'w+').write('\n'.join(out_list))

def get_raw_word_content_to_urheen():
    in_raw_dat_filefold = '../../../ExpData/MovieData/RawData/'
    in_movie_struct_file = in_raw_dat_filefold + 'Raw/MovieStructDataForComments_DeleteSameEncodeError.txt'
    in_movie_info_file = in_raw_dat_filefold + 'Raw/MovieInfo.txt'
    raw_content_file = in_raw_dat_filefold + 'Raw/RawSenDataForComments_DSEE.txt'

    preDat = PropressingDat(in_movie_struct_file,in_movie_info_file)
    preDat.load_movie_dat_info()
    preDat.load_data_struct()
    preDat.print_out_dat_info(raw_content_file)
    word_file_preprocessing(raw_content_file)

def get_sen_over_flag_dict(level = '1'):
    sen_flag_file = '../../../ExpData/UserDat/sentence_split_sym.txt'
    sen_over_flag_dict = {}
    in_file_con_list = open(sen_flag_file,'r').readlines()
    for line_con in in_file_con_list:
        line_con = line_con.strip()
        sym , level_num = line_con.split('\t')
        if level_num == level:
            sen_over_flag_dict[sym] = 1
    return sen_over_flag_dict

# -------------------------------------------------- #
# 将POS文件，进行划分句子，为了能更好做依存分析
# 输入：
#      in_word_pos_file --> postag 文件
#      并且通过 split_pos_content 分别提取每句话的 seg 和 pos
# 输出：
#      out_sen_file          --> 按照句号划分后小句的文件，用来做 dependency parser
#      src_to_tgt_file       --> 记录了 原来一句话分成了几个小句的文件
#      short_sen_to_pos_file --> 记录了每个小句对应的 postag 标签
# Time: 2017-02-25
# -------------------------------------------------- #
def split_sentence(in_word_pos_file = '',out_sen_file = '',src_to_tgt_file = '',short_sen_to_pos_file = ''):
    if in_word_pos_file == '':
        in_word_pos_file = '../../../ExpData/MovieData/RawData/Urheen_Res/RawSenDataForComments_DSEE_Urheen_pos.txt'
    if out_sen_file == '':
        out_sen_file = '../../../ExpData/MovieData/RawData/Urheen_Res/RawDSEEUrheenSeg_SenSplit.txt'
    if src_to_tgt_file == '':
        src_to_tgt_file = '../../../ExpData/MovieData/RawData/Urheen_Res/RawDSEEUrheenSeg_SenSplit_SrcToTgt.txt'
    if short_sen_to_pos_file == '':
        short_sen_to_pos_file = '../../../ExpData/MovieData/RawData/Urheen_Res/RawDSEEUrheenSeg_SplitSenToPOS.txt'

    src_to_tgt_list_dict = {}
    out_line_con_list = []
    in_line_con_list = open(in_word_pos_file,'r').readlines()
    short_sen_to_pos_dict = {}
    sen_con_list = []
    sen_over_flag_dict = get_sen_over_flag_dict(level='1')
    for line_con in in_line_con_list:
        line_con = line_con.strip()
        word_con_list, pos_list = split_pos_content(line_con)
        tgt_list = []
        src_to_tgt_list_dict[' '.join(word_con_list)] = []
        sen_con_list.append(' '.join(word_con_list))
        temp_sen_list = []
        temp_pos_list = []
        for i in range(0,len(word_con_list)):
            word_con = word_con_list[i]
            temp_sen_list.append(word_con)
            temp_pos_list.append(pos_list[i])
            if i == len(word_con_list) - 1 or sen_over_flag_dict.has_key(word_con):
                sen_str_len = len(temp_sen_list)
                if sen_str_len == 1:
                    continue
                else:
                    tgt_list.append(' '.join(temp_sen_list))
                    out_line_con_list.append(' '.join(temp_sen_list))
                    short_sen_to_pos_dict[' '.join(temp_sen_list)] = ' '.join(temp_pos_list)
                    temp_sen_list = []
                    temp_pos_list = []
        src_to_tgt_list_dict[' '.join(word_con_list)] = tgt_list

    out_src_to_tgt_con_list = []
    for sen_con in sen_con_list:
        out_src_to_tgt_con_list.append(sen_con + '-*-*-' + '-*-*-'.join(src_to_tgt_list_dict[sen_con]))

    out_short_sen_to_pos_list = []
    for short_sen,short_pos in short_sen_to_pos_dict.items():
        out_short_sen_to_pos_list.append(short_sen + '\t' + short_pos)

    open(out_sen_file,'w+').write('\n'.join(out_line_con_list))
    open(src_to_tgt_file,'w+').write('\n'.join(out_src_to_tgt_con_list))
    open(short_sen_to_pos_file,'w+').write('\n'.join(out_short_sen_to_pos_list))

# -------------------------------------------------- #
# split_sentence 的 辅助函数， 从 word/pos 文本中提取 word 和 pos
# Time: 2017-02-25
# -------------------------------------------------- #
def split_pos_content(pos_content):
    word_list = []
    pos_list = []
    for word_pos in pos_content.split(' '):
        temp_list = word_pos.split('/')
        if len(temp_list) == 2:
            word_list.append(temp_list[0])
            pos_list.append(temp_list[1])
        elif len(temp_list) == 3:
            if temp_list[0] == '' and temp_list[1] == '':
                word_list.append('/')
                pos_list.append(temp_list[2])
            else:
                word_list.append(temp_list[0] + '/' + temp_list[1])
                pos_list.append(temp_list[2])

    return word_list, pos_list


# -------------------------------------------------- #
# 将一个大文件分解成几个小文件，为了能并行做stanford parser
# Time: 2017-02-24
# -------------------------------------------------- #
def split_file(in_file,split_num = 10):
    in_line_con_list = open(in_file,'r').readlines()
    out_line_con_list_list = []
    out_file_list = []
    for i in range(0,split_num):
        out_line_con_list_list.append([])
        out_file_list.append(in_file.replace('.txt','') + '_split_' + str(i+1) + '_' + str(split_num) + '.txt')
    for k in range(0,len(in_line_con_list)):
        line_con = in_line_con_list[k].strip()
        out_line_con_list_list[ k % split_num].append(line_con)

    for k in range(0,split_num):
        open(out_file_list[k],'w+').write('\n'.join(out_line_con_list_list[k]))

# -------------------------------------------------- #
# 导入依存分析的结果，并输出句子与依存分析对应的数据
# Time: 2017-02-25
# -------------------------------------------------- #
def load_stanford_dep_res():
    sen_file_list = []
    dep_file_list = []
    file_fold = '../../../ExpData/MovieData/RawData/Stanford_Parser_Res/'
    out_file = file_fold + 'parser_out_dict.txt'
    for i in range(1,5):
        sen_file_list.append(file_fold + 'out_split_' + str(i) + '_4.txt')
        dep_file_list.append(file_fold + 'parser_out_split_' + str(i) + '_4.txt')

    sen_con_to_dep_dict = {}
    for sen_file,dep_file in zip(sen_file_list,dep_file_list):
        load_stanford_dep_file(sen_file,dep_file,sen_con_to_dep_dict)

    print len(sen_con_to_dep_dict)

    # 这个dict的长度可能和所有文件行数和不同，原因在于dict的key有重复。

    out_line_con_list = []
    for key,value in sen_con_to_dep_dict.items():
        out_line_con_list.append(key + '\t' + value)
    open(out_file,'w+').write('\n'.join(out_line_con_list))


    return sen_con_to_dep_dict

# -------------------------------------------------- #
# load_stanford_dep_res 的 辅助函数
# Time: 2017-02-25
# -------------------------------------------------- #
def load_stanford_dep_file(sen_file = '',dep_file =  '',sen_con_to_dep_dict = {}):
    if sen_file == '':
        sen_file = '../../../ExpData/MovieData/RawData/Stanford_Parser_Res/out_split_1_4.txt'
    if dep_file == '':
        dep_file = '../../../ExpData/MovieData/RawData/Stanford_Parser_Res/parser_out_split_1_4.txt'

    all_dep_list = []
    sen_line_con_list = open(sen_file,'r').readlines()
    dep_line_con_list = open(dep_file,'r').readlines()
    dep_list = []
    for line_con in dep_line_con_list:
        line_con = line_con.strip()
        if line_con.find(' ') == -1:
            all_dep_list.append('-*-*-'.join(dep_list))
            dep_list = []
        else:
            dep_list.append(line_con)

    print len(sen_line_con_list)
    print len(all_dep_list)
    for sen_con,dep_str in zip(sen_line_con_list,all_dep_list):
        sen_con = sen_con.strip()
        sen_con_to_dep_dict[sen_con] = dep_str


def load_all_doc_res(short_sen_to_dep_file = '',sen_to_short_sen_list_file = '',
                     short_sen_to_pos_tag_file = '',out_json_file = '',split_str = '-*-*-'):

    file_fold = '../../../ExpData/MovieData/RawData/'

    if short_sen_to_dep_file == '':
        short_sen_to_dep_file = file_fold + 'Stanford_Parser_Res/parser_out_dict.txt'
    if sen_to_short_sen_list_file == '':
        sen_to_short_sen_list_file = file_fold + 'Urheen_Res/RawDSEEUrheenSeg_SenSplit_SrcToTgt.txt'
    if short_sen_to_pos_tag_file == '':
        short_sen_to_pos_tag_file = file_fold + 'Urheen_Res/RawDSEEUrheenSeg_SplitSenToPOS.txt'
    if out_json_file == '':
        out_json_file = file_fold + 'Raw/RawSenDataForComments_DSEE_SegPosDep.json'


    all_doc_list = []

    short_sen_to_dep_dict = {}
    line_con_list = open(short_sen_to_dep_file,'r').readlines()
    for line_con in line_con_list:
        line_con = line_con.strip()
        short_sen,dep_str = line_con.split('\t')
        short_sen_to_dep_dict[short_sen] = dep_str

    all_sen_order_list = []
    sen_to_short_sen_list_dict = {}
    line_con_list = open(sen_to_short_sen_list_file,'r').readlines()
    for line_con in line_con_list:
        line_con = line_con.strip()
        con_list = line_con.split(split_str)
        sen = con_list[0]
        all_sen_order_list.append(sen)
        sen_to_short_sen_list_dict[sen] = []
        for k in range(1,len(con_list)):
             sen_to_short_sen_list_dict[sen].append(con_list[k])

    short_sen_to_pos_tag_dict = {}
    line_con_list = open(short_sen_to_pos_tag_file,'r').readlines()
    for line_con in line_con_list:
        line_con = line_con.strip()
        short_sen,pos_tag = line_con.split('\t')
        short_sen_to_pos_tag_dict[short_sen] = pos_tag

    for sen_con in all_sen_order_list:
        short_sen_list = sen_to_short_sen_list_dict[sen_con]
        doc = get_doc_dict()
        doc['raw_con'] = sen_con
        for short_sen in short_sen_list:
            sen_dict = get_sen_dict()
            sen_dict['dep'] = short_sen_to_dep_dict[short_sen]
            sen_dict['seg'] = short_sen
            sen_dict['raw'] = short_sen.replace(' ','')
            sen_dict['pos'] = short_sen_to_pos_tag_dict[short_sen]
            doc['sen_list'].append(sen_dict)
        all_doc_list.append(doc)

    jsonAPI.print_out_dat_json(all_doc_list,out_json_file)

if __name__ == '__main__':
    # get_raw_word_content_to_urheen()
    # delete_same_encode_error_sen()

    # split_sentence()

    # split_file('out.txt',split_num = 4)
    # load_stanford_dep_res()

    load_all_doc_res()

