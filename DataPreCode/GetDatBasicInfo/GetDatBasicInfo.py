#encoding=utf-8


# -------------------------------------------------------------------- #
# 获取数据集的一些基本信息：名称、褒贬数目、长度之类
# Time: 2017-01-16
# -------------------------------------------------------------------- #

import sys
sys.path.append("../UsefulLibs")
import usefulAPI, xmlAPI, jsonAPI

class MovieInfor:
    def __init__(self):
        self.category = ''                  #可以每部电影是一个category，也可以每个电影类型是一个category
        self.pos_num = 0
        self.neg_num = 0
        self.all_num = 0
        self.max_len = 0
        self.aver_len = 0.0
        self.min_len = 0
        self.voca_len = 0.0
        self.attr_value_to_pos_num_dict = {}
        self.attr_value_to_neg_num_dict = {}
        self.attr_value_to_pos_per_dict = {}
        self.attr_value_to_all_num_dict = {}
        self.attr_value_to_all_num_per_dict = {}

'''
def get_con_dat_dict():
    dat_dict = {}
    dat_dict['content'] = ''
    dat_dict['segmentation'] = ''
    dat_dict['postag'] = ''
    dat_dict['dependency'] = ''
    return dat_dict

def get_dat_struct_dict():
    struct_dict = {}
    struct_dict['comment_id'] = ''
    struct_dict['user_id'] = ''
    struct_dict['movie_name'] = ''
    struct_dict['senti_label'] = ''
    struct_dict['user_info'] = ''
    struct_dict['movie_type'] = ''
    struct_dict['con_for_doc_dict'] = {}
    struct_dict['con_for_sen_list'] = []
    return struct_dict
'''

class GetDatBasicInfo:
    def __init__(self,dat_json_file,out_file_fold):
        self.dat_json_file = dat_json_file
        self.out_file_fold = out_file_fold
        self.all_dat_list = []
        self.cat_to_dat_list_dict = {}

    def get_each_cat_list(self,cat = 'movie'):
        for i in range(0,len(self.all_dat_list)):
            each_dat = self.all_dat_list[i]
            key_list = []
            if cat == 'movie':
                key_list.append(each_dat['movie_name'])
            elif cat == 'category':
                key_list = each_dat['movie_type'].split('/')
            else:
                key_list.append(each_dat['movie_name'])
            for key in key_list:
                if self.cat_to_dat_list_dict.has_key(key) == False:
                    self.cat_to_dat_list_dict[key] = []
                self.cat_to_dat_list_dict[key].append(i)

    def compute_each_cat_basic_info(self,cat = 'movie'):
        self.all_dat_list = jsonAPI.load_json(self.dat_json_file)['data']
        print len(self.all_dat_list)
        usefulAPI.mk_dir(self.out_file_fold)
        self.get_each_cat_list(cat)
        for cat, dat_id_list in self.cat_to_dat_list_dict.items():
            movie_info = self.compute_basic_info(cat , dat_id_list)
            out_file = self.out_file_fold + 'DatBasicInfo_' + cat + '.txt'
            self.print_all_dat_to_file(movie_info,out_file)

    def compute_basic_info(self,cat,dat_id_list):
        movie_info = MovieInfor()
        movie_info.category = cat
        voca_dict = {}
        len_list = []
        for i in dat_id_list:
            temp_dat = self.all_dat_list[i]
            movie_info.all_num = movie_info.all_num + 1
            if temp_dat['senti_label'] == 'POS':
                movie_info.pos_num = movie_info.pos_num + 1
            else:
                movie_info.neg_num = movie_info.neg_num + 1
            user_con_list = temp_dat['con_for_doc_dict']['segmentation'].split(' ')
            len_list.append(len(user_con_list))
            for word in user_con_list:
                if voca_dict.has_key(word) == False: voca_dict[word] = 1
        movie_info.voca_len = len(voca_dict)
        len_list = sorted(len_list)
        movie_info.max_len = len_list[-1]
        movie_info.min_len = len_list[0]
        all_len = 0
        for temp_len in len_list:
            all_len = all_len + temp_len
        movie_info.aver_len = float(all_len) / float(len(len_list))
        self.compute_useinfo_prob(movie_info,dat_id_list)
        return movie_info

    def add_num_to_dict(self,dict,key,value = 1):
        if dict.has_key(key):
            dict[key] = dict[key] + value
        else:
            dict[key] = 1

    def compute_useinfo_prob(self,movie_info,dat_id_list):
        for i in dat_id_list:
            temp_struct = self.all_dat_list[i]
            temp_user_info_content = temp_struct['user_info']
            add_pos_num = 0
            add_neg_num = 0
            if temp_struct['senti_label'] == 'POS':
                add_pos_num = 1
            else:
                add_neg_num = 1

            for temp_str in temp_user_info_content.split('_'):
                if temp_str.split('/')[0] == 'Label': continue
                self.add_num_to_dict(movie_info.attr_value_to_pos_num_dict,temp_str,add_pos_num)
                self.add_num_to_dict(movie_info.attr_value_to_neg_num_dict,temp_str,add_neg_num)

        for temp_key,pos_num in movie_info.attr_value_to_pos_num_dict.items():
            neg_num = movie_info.attr_value_to_neg_num_dict[temp_key]
            pos_per = float(pos_num) / float(pos_num + neg_num)
            all_num = pos_num + neg_num
            all_num_per = float(pos_num + neg_num) / float(len(dat_id_list))
            movie_info.attr_value_to_pos_per_dict[temp_key] = pos_per
            movie_info.attr_value_to_all_num_dict[temp_key] = all_num
            movie_info.attr_value_to_all_num_per_dict[temp_key] = all_num_per

    def print_all_dat_to_file(self,movie_info,out_file):
        con_list = []
        con_list.append('Basic_Info:        ')
        con_list.append('movie_name\t' +str(movie_info.category))
        con_list.append('all_num\t' +str(movie_info.all_num))
        con_list.append('pos_num\t' +str(movie_info.pos_num))
        con_list.append('neg_num\t' +str(movie_info.neg_num))
        con_list.append('max_len\t' +str(movie_info.max_len))
        con_list.append('aver_len\t' +str(movie_info.aver_len))
        con_list.append('min_len\t' +str(movie_info.min_len))
        con_list.append('voca_len\t' +str(movie_info.voca_len))
        con_list.append('\n')

        con_list.append('AttributeValueToProb_Info:        ')
        con_list.append('AttributeValue\tPosNum\tNegNum\tPOSPer\tAllNum\tAllPer')

        attr_value_to_pos_num_dict = movie_info.attr_value_to_pos_num_dict
        attr_value_to_neg_num_dict = movie_info.attr_value_to_neg_num_dict
        attr_value_to_pos_per_dict = movie_info.attr_value_to_pos_per_dict
        attr_value_to_all_num_dict = movie_info.attr_value_to_all_num_dict
        attr_value_to_all_num_per_dict = movie_info.attr_value_to_all_num_per_dict

        for key,value in attr_value_to_pos_num_dict.items():
            temp_list = []
            temp_list.append(key.encode('utf-8'))
            temp_list.append(str(attr_value_to_pos_num_dict[key]))
            temp_list.append(str(attr_value_to_neg_num_dict[key]))
            temp_list.append(str(attr_value_to_pos_per_dict[key]))
            temp_list.append(str(attr_value_to_all_num_dict[key]))
            temp_list.append(str(attr_value_to_all_num_per_dict[key]))
            con_list.append('\t'.join(temp_list))

        open(out_file,'w+').write('\n'.join(con_list))


if __name__ == '__main__':

    all_dat_json_file = '../../../ExpData/MovieData/JsonData/jsonDatForComments.json'
    out_file_fold = '../../../ExpData/MovieData/JsonDatBasicInfo/'
    GetDatBasicInfo = GetDatBasicInfo(all_dat_json_file,out_file_fold)
    GetDatBasicInfo.compute_each_cat_basic_info(cat = 'category')
    GetDatBasicInfo.compute_each_cat_basic_info(cat = 'movie')
