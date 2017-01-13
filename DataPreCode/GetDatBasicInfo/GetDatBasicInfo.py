#encoding=utf-8
from cvDat import *
import usefulAPI


class MovieInfor:
    def __init__(self):
        self.movie_name = ''
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




class GetDatBasicInfo:
    def __init__(self,movie_comment_file):
        self.movie_comment_file = movie_comment_file
        self.out_file_fold = ''
        self.cvDat = None

    def initial(self):
        self.cvDat = CvDat(self.movie_comment_file)
        self.cvDat.load_data_struct()
        self.out_file_fold = './' + self.movie_comment_file.split('/')[1] + '/' + self.movie_comment_file.split('/')[2] + '/DatBasicInfo/'

    def compute_each_movie_basic_info(self):
        self.initial()
        usefulAPI.mkDir(self.out_file_fold)
        for movie_name, movie_dat_list in self.cvDat.movie_name_dict.items():
            movie_info = self.compute_basic_info(movie_name,movie_dat_list)
            out_file = self.out_file_fold + 'DatBasicInfo_' + movie_name + '.txt'
            self.print_all_dat_to_file(movie_info,out_file)

    def compute_basic_info(self,movie_name,movie_dat_list):
        movie_info = MovieInfor()
        movie_info.movie_name = movie_name
        voca_dict = {}
        len_list = []
        for temp_struct in movie_dat_list:
            movie_info.all_num = movie_info.all_num + 1
            if temp_struct.sentiLabel == 'POS':
                movie_info.pos_num = movie_info.pos_num + 1
            else:
                movie_info.neg_num = movie_info.neg_num + 1
            user_con_list = temp_struct.commentCon.split(' ')
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

        self.compute_useinfo_prob(movie_info,movie_dat_list)

        return movie_info

    def add_num_to_dict(self,dict,key,value = 1):
        if dict.has_key(key):
            dict[key] = dict[key] + value
        else:
            dict[key] = 1

    def compute_useinfo_prob(self,movie_info,movie_dat_list):
        for temp_struct in movie_dat_list:
            temp_user_info_content = temp_struct.userInfo
            add_pos_num = 0
            add_neg_num = 0
            if temp_struct.sentiLabel == 'POS': add_pos_num = 1
            else:                               add_neg_num = 1

            for temp_str in temp_user_info_content.split('_'):
                if temp_str.split('/')[0] == 'Label': continue
                self.add_num_to_dict(movie_info.attr_value_to_pos_num_dict,temp_str,add_pos_num)
                self.add_num_to_dict(movie_info.attr_value_to_neg_num_dict,temp_str,add_neg_num)

        for temp_key,pos_num in movie_info.attr_value_to_pos_num_dict.items():
            neg_num = movie_info.attr_value_to_neg_num_dict[temp_key]
            pos_per = float(pos_num) / float(pos_num + neg_num)
            all_num = pos_num + neg_num
            all_num_per = float(pos_num + neg_num) / float(len(movie_dat_list))
            movie_info.attr_value_to_pos_per_dict[temp_key] = pos_per
            movie_info.attr_value_to_all_num_dict[temp_key] = all_num
            movie_info.attr_value_to_all_num_per_dict[temp_key] = all_num_per

    def print_all_dat_to_file(self,movie_info,out_file):
        con_list = []
        con_list.append('Basic_Info:        ')
        con_list.append('movie_name\t' +str(movie_info.movie_name))
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
            temp_list.append(key)
            temp_list.append(str(attr_value_to_pos_num_dict[key]))
            temp_list.append(str(attr_value_to_neg_num_dict[key]))
            temp_list.append(str(attr_value_to_pos_per_dict[key]))
            temp_list.append(str(attr_value_to_all_num_dict[key]))
            temp_list.append(str(attr_value_to_all_num_per_dict[key]))
            con_list.append('\t'.join(temp_list))
        open(out_file,'w+').write('\n'.join(con_list))






if __name__ == '__main__':

    #movie_comment_file = './Data/Datset_Old/allMovie_Out_delete_3.txt'
    movie_comment_file = './Data/DataForDemoGroupSensitiveAspectMining.txt'
    GetDatBasicInfo = GetDatBasicInfo(movie_comment_file)
    GetDatBasicInfo.compute_each_movie_basic_info()

