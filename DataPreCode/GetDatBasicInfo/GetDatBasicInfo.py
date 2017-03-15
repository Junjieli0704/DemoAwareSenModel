#encoding=utf-8


# -------------------------------------------------------------------- #
# 获取数据集的一些基本信息：名称、褒贬数目、长度之类
# Time: 2017-01-16
# -------------------------------------------------------------------- #

import sys
sys.path.append("../UsefulLibs")
import usefulAPI, jsonAPI

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
        self.len_dis_dict = {}
        self.each_movie_dis_dict = {}
        self.attr_value_to_pos_num_dict = {}
        self.attr_value_to_neg_num_dict = {}
        self.attr_value_to_pos_per_dict = {}
        self.attr_value_to_all_num_dict = {}
        self.attr_value_to_all_num_per_dict = {}


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
            # cat 为 'movie'     ：意味着每部电影的数据放一起，并一起统计
            # cat 为 'category'  ：意味着每个类型的电影数据放一起，并一起统计
            # cat 为 'all'       ：意味着数据集的所有数据放一起，并一起统计
            if cat == 'movie':
                key_list.append(each_dat['movie_name'])
            elif cat == 'category':
                key_list = each_dat['movie_type'].split('/')
            elif cat == 'all':
                key_list.append('all')
            else:
                key_list.append(each_dat['movie_name'])
            for key in key_list:
                if self.cat_to_dat_list_dict.has_key(key) == False:
                    self.cat_to_dat_list_dict[key] = []
                self.cat_to_dat_list_dict[key].append(i)

    def compute_each_cat_basic_info(self,cat = 'movie'):
        self.all_dat_list = jsonAPI.load_json_dat(self.dat_json_file)
        usefulAPI.mk_dir(self.out_file_fold)
        self.get_each_cat_list(cat)
        for cat, dat_id_list in self.cat_to_dat_list_dict.items():
            movie_info = self.compute_basic_info(cat , dat_id_list)
            out_file = self.out_file_fold + 'DatBasicInfo_' + cat + '.txt'
            self.print_all_dat_to_file(movie_info,out_file)


    def init_len_distri_dict(self,movie_info):
        movie_info.len_dis_dict['0-9'] = 0
        movie_info.len_dis_dict['10-19'] = 0
        movie_info.len_dis_dict['20-29'] = 0
        movie_info.len_dis_dict['30-39'] = 0
        movie_info.len_dis_dict['40+'] = 0


    def add_len_distri_dict(self,movie_info,len_num):
        if len_num < 10:
            movie_info.len_dis_dict['0-9'] = movie_info.len_dis_dict['0-9'] + 1
        elif len_num < 20:
            movie_info.len_dis_dict['10-19'] = movie_info.len_dis_dict['10-19'] + 1
        elif len_num < 30:
            movie_info.len_dis_dict['20-29'] = movie_info.len_dis_dict['20-29'] + 1
        elif len_num < 40:
            movie_info.len_dis_dict['30-39'] = movie_info.len_dis_dict['30-39'] + 1
        else:
            movie_info.len_dis_dict['40+'] = movie_info.len_dis_dict['40+'] + 1

    def compute_basic_info(self,cat,dat_id_list):
        movie_info = MovieInfor()
        movie_info.category = cat
        self.init_len_distri_dict(movie_info)
        voca_dict = {}
        len_list = []
        for i in dat_id_list:
            temp_dat = self.all_dat_list[i]
            movie_name = temp_dat['movie_name']
            if movie_info.each_movie_dis_dict.has_key(movie_name) == False:
                movie_info.each_movie_dis_dict[movie_name] = 0
            movie_info.each_movie_dis_dict[movie_name] = movie_info.each_movie_dis_dict[movie_name] + 1
            movie_info.all_num = movie_info.all_num + 1
            if temp_dat['senti_label'] == 'POS':
                movie_info.pos_num = movie_info.pos_num + 1
            else:
                movie_info.neg_num = movie_info.neg_num + 1
            user_con_list = temp_dat['doc_dict']['seg_con'].split(' ')
            self.add_len_distri_dict(movie_info,len(user_con_list))
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
        con_list.append('--------------------------------------------------')
        con_list.append('max_len\t' +str(movie_info.max_len))
        con_list.append('aver_len\t' +str(movie_info.aver_len))
        con_list.append('min_len\t' +str(movie_info.min_len))
        con_list.append('--------------------------------------------------')
        con_list.append('len 0-9:\t' + str(movie_info.len_dis_dict['0-9']))
        con_list.append('len 10-19:\t' + str(movie_info.len_dis_dict['10-19']))
        con_list.append('len 20-29:\t' + str(movie_info.len_dis_dict['20-29']))
        con_list.append('len 30-39:\t' + str(movie_info.len_dis_dict['30-39']))
        con_list.append('len 40+:\t' + str(movie_info.len_dis_dict['40+']))
        con_list.append('--------------------------------------------------')
        con_list.append('voca_len\t' +str(movie_info.voca_len))
        con_list.append('--------------------------------------------------')
        con_list.append('each_movie_numbers:')
        for movie_name, number in movie_info.each_movie_dis_dict.items():
            temp_str = movie_name.encode('utf-8') + ': ' + str(number)
            con_list.append(temp_str)
        con_list.append('--------------------------------------------------')
        con_list.append('AttributeValueToProb_Info:        ')
        con_list.append('AttributeValue\tPosNum\tNegNum\tPOSPer\tAllNum\tAllPer')

        attr_value_to_pos_num_dict = movie_info.attr_value_to_pos_num_dict
        attr_value_to_neg_num_dict = movie_info.attr_value_to_neg_num_dict
        attr_value_to_pos_per_dict = movie_info.attr_value_to_pos_per_dict
        attr_value_to_all_num_dict = movie_info.attr_value_to_all_num_dict
        attr_value_to_all_num_per_dict = movie_info.attr_value_to_all_num_per_dict

        for key,value in attr_value_to_pos_num_dict.items():
            key_str = key.encode('utf-8')
            temp_list = []
            temp_list.append(key_str)
            temp_list.append(str(attr_value_to_pos_num_dict[key]))
            temp_list.append(str(attr_value_to_neg_num_dict[key]))
            temp_list.append(str(attr_value_to_pos_per_dict[key]))
            temp_list.append(str(attr_value_to_all_num_dict[key]))
            temp_list.append(str(attr_value_to_all_num_per_dict[key]))
            con_list.append('\t'.join(temp_list))

        open(out_file,'w+').write('\n'.join(con_list))

if __name__ == '__main__':

    all_dat_json_file = '../../../ExpData/MovieData/JsonDat/JsonData/MovieStructDataForComments_DSEE.json'
    out_file_fold = '../../../ExpData/MovieData/JsonDat/BasicInfo/'
    GetDatBasicInfo = GetDatBasicInfo(all_dat_json_file,out_file_fold)
    GetDatBasicInfo.compute_each_cat_basic_info(cat = 'category')
    GetDatBasicInfo.compute_each_cat_basic_info(cat = 'movie')
    GetDatBasicInfo.compute_each_cat_basic_info(cat = 'all')