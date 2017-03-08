#encoding=utf-8

# -------------------------------------------------------------------- #
# 将无结构数据转化json数据
# json 数据结构类型：
# 每篇文本转化成一个 dict (struct_dict)，该dict包含了文本、用户以及电影的基本信息
#    struct_dict['comment_id']                          评论ID，
#    struct_dict['user_id']                             用户ID，发布评论的用户ID
#    struct_dict['movie_name']                          电影名称
#    struct_dict['user_info']                           用户信息
#    struct_dict['senti_label']                         句子标签，褒贬
#    struct_dict['movie_type']                          电影类型
#    struct_dict['doc_dict']                            内容dict，包含原始数据、分词、词性标注、依存分析
#        struct_dict['doc_dict']['raw_con']             原始数据
#        struct_dict['doc_dict']['sen_list'] = []       每个小句的信息
#        struct_dict['doc_dict']['sen_list'][0]         第一个小句的基本信息
#        struct_dict['doc_dict']['sen_list'][0]['raw']  第一个小句的 raw 信息
#        struct_dict['doc_dict']['sen_list'][0]['seg']  第一个小句的 seg 信息
#        struct_dict['doc_dict']['sen_list'][0]['pos']  第一个小句的 pos 信息
#        struct_dict['doc_dict']['sen_list'][0]['dep']  第一个小句的 dep 信息
# Time: 2017-02-25
# -------------------------------------------------------------------- #

import sys
sys.path.append("../UsefulLibs")
import json, jsonAPI, usefulAPI
def get_dat_struct_dict():
    struct_dict = {}
    struct_dict['comment_id'] = ''
    struct_dict['user_id'] = ''
    struct_dict['movie_name'] = ''
    struct_dict['senti_label'] = ''
    struct_dict['user_info'] = ''
    struct_dict['movie_type'] = ''
    struct_dict['doc_dict'] = {}
    return struct_dict

class ChangeDatToJson:
    def __init__(self,movie_struct_comment_file,movie_info_file,comment_json_file):
        self.comment_json_file = comment_json_file
        self.movie_struct_comment_file = movie_struct_comment_file
        self.movie_info_file = movie_info_file
        self.comment_dat_list = []
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
        print "load_movie_dat_info() finished......"

    def load_comment_json_file(self):
        data = json.loads(open(self.comment_json_file,'r').read())
        self.comment_dat_list = data['data']
        print "load_comment_json_file() finished......"

    def load_data_struct(self):
        line_con_list = open(self.movie_struct_comment_file,'r').readlines()
        for line_con in line_con_list:
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
            self.all_dat_list.append(temp_struct)
        print "load_data_struct() finished......"

    def generate_all_dat_to_json(self,out_json_file):
        for temp_struct, comment_dat in zip(self.all_dat_list,self.comment_dat_list):
            temp_struct['doc_dict'] = comment_dat
        jsonAPI.print_out_dat_json(self.all_dat_list,out_json_file)
        jsonAPI.print_out_struct_dat_json_visual(self.all_dat_list,out_json_file.replace('json','jsonVis'))

    # -------------------------------------------------------------------- #
    # Fun: Generate movie data for each category (Love, Comedy and so on).
    #      从所有数据中，生成每个类别的数据
    # Time: 2017-02-25
    # -------------------------------------------------------------------- #
    def split_dat_accord_type(self, out_file_fold):
        movie_type_to_id_list_dict = {}
        for i in range(0,len(self.all_dat_list)):
            temp_dat = self.all_dat_list[i]
            movie_type_list = temp_dat['movie_type'].split('/')
            for movie_type in movie_type_list:
                if movie_type_to_id_list_dict.has_key(movie_type) == False:
                    movie_type_to_id_list_dict[movie_type] = []
                movie_type_to_id_list_dict[movie_type].append(i)

        for movie_type, id_list in movie_type_to_id_list_dict.items():
            id_list = list(set(id_list))
            dat_list = []
            for i in id_list:
                dat_list.append(self.all_dat_list[i])
            out_file = out_file_fold + movie_type + '.json'
            jsonAPI.print_out_dat_json(dat_list,out_file)
            jsonAPI.print_out_struct_dat_json_visual(dat_list,out_file.replace('json','jsonVis'))



if __name__ == '__main__':

    in_raw_dat_filefold = '../../../ExpData/MovieData/RawData/'
    in_movie_struct_file = in_raw_dat_filefold + 'Raw/MovieStructDataForComments_DeleteSameEncodeError.txt'
    in_movie_info_file = in_raw_dat_filefold + 'Raw/MovieInfo.txt'
    comment_json_file = in_raw_dat_filefold + 'Raw/RawSenDataForComments_DSEE_SegPosDep.json'

    out_json_dat_filefold = '../../../ExpData/MovieData/JsonDat/'
    out_json_file = out_json_dat_filefold + 'JsonData/MovieStructDataForComments_DSEE.json'

    change_dat_to_json = ChangeDatToJson(in_movie_struct_file,in_movie_info_file,comment_json_file)
    change_dat_to_json.load_movie_dat_info()
    change_dat_to_json.load_data_struct()
    change_dat_to_json.load_comment_json_file()
    change_dat_to_json.generate_all_dat_to_json(out_json_file)
    change_dat_to_json.split_dat_accord_type('../../../ExpData/MovieData/JsonDat/JsonData/')
