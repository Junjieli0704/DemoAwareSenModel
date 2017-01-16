#encoding=utf-8

# -------------------------------------------------------------------- #
# 获取不同用户属性发表评论的差异性
# 输入N条评论及其用户属性
# 设定要观察的用户属性：性别，年龄？
# 找出评论中特定的属性下，不同维度的用户的用词差异（男 VS 女， 中年人 VS 老年人）
# Time: 2017-01-16 10:26
# -------------------------------------------------------------------- #

import sys
sys.path.append("../UsefulLibs")
import usefulAPI, jsonAPI

class UserDatInfo:
    def __init__(self):
        self.gender = 'NULL'
        self.age = 'NULL'
        self.location = 'NULL'
        self.content = ''


class GetDemoSpecWords:
    def __init__(self,dat_json_file):
        self.dat_json_file = dat_json_file
        self.all_dat_list = []
        self.cat_to_dat_id_list_dict = {}       # 'Comedy' -> [0, 4, 5, 8, 10]
        self.cat_to_dat_info_list_dict = {}     # 'Comedy' -> [UserDatInfo1, UserDatInfo2]

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
                if self.cat_to_dat_id_list_dict.has_key(key) == False:
                    self.cat_to_dat_id_list_dict[key] = []
                    self.cat_to_dat_info_list_dict[key] = []
                self.cat_to_dat_id_list_dict[key].append(i)


    def load_all_dat(self,cat = 'movie'):
        self.all_dat_list = jsonAPI.load_json_movie_dat(self.dat_json_file)
        self.get_each_cat_list(cat)
        for cat, dat_id_list in self.cat_to_dat_id_list_dict.items():
            for i in dat_id_list:
                each_dat = self.all_dat_list[i]
                usr_dat_info = UserDatInfo()
                user_info_str = each_dat['user_info']
                #Sex/女_Loc/二线_Age/NULL_Edu/NULL_Label/健康-文艺-新闻资讯-美食-星座命理-旅游
                for user_info in user_info_str.split('_'):
                    attribute,value = user_info.split('/')
                    if attribute == 'Sex':
                        usr_dat_info.gender = value
                    elif attribute == 'Loc':
                        usr_dat_info.location = value
                    elif attribute == 'Age':
                        usr_dat_info.age = value
                usr_dat_info.content = each_dat['con_for_doc_dict']['segmentation']
                if self.cat_to_dat_info_list_dict.has_key(cat) == False:
                    self.cat_to_dat_info_list_dict[cat] = []
                self.cat_to_dat_info_list_dict[cat].append(usr_dat_info)

    def generate_spec_words_for_demo(self,out_file_fold,demo_input = 'gender'):

        for category, usr_dat_info_list in self.cat_to_dat_info_list_dict.items():
            print category
            demo_value_list = []
            demo2conlist = {}
            for usr_dat in usr_dat_info_list:
                demo_str = usr_dat.gender
                if demo_input == 'location':
                    demo_str = usr_dat.location
                elif demo_input == 'age':
                    demo_str = usr_dat.age
                if demo_str == 'NULL': continue
                if demo2conlist.has_key(demo_str) == False:
                    demo2conlist[demo_str] = []
                    demo_value_list.append(demo_str)
                demo2conlist[demo_str].append(usr_dat.content)

            word_demo_to_times = {}
            demo_to_times = {}
            for demo, con_list in demo2conlist.items():
                for content in con_list:
                    if demo_to_times.has_key(demo) == False:
                        demo_to_times[demo] = 0.0
                    demo_to_times[demo] = demo_to_times[demo] + 1.0
                    for word in content.split(' '):
                        key = word + '$' + demo
                        if word_demo_to_times.has_key(key) == False:
                            word_demo_to_times[key] = 0.0
                        word_demo_to_times[key] = word_demo_to_times[key] + 1.0
            '''
            # 归一化次数
            for word_demo , times in word_demo_to_times.items():
                demo = word_demo.split('$')[1]
                if demo == '':
                    print word_demo
                times = times / demo_to_times[demo]
                word_demo_to_times[word_demo] = times
            '''
            out_file_con_list = []
            intro_line_con_list = ['Word']
            basic_info_line_con_list = ['All']
            for demo in demo_value_list:
                times = demo_to_times[demo]
                intro_line_con_list.append(demo)
                basic_info_line_con_list.append(str(times))
            out_file_con_list.append('\t'.join(intro_line_con_list))
            out_file_con_list.append('\t'.join(basic_info_line_con_list))

            for word_demo , times in word_demo_to_times.items():
                word = word_demo.split('$')[0]
                con_list = []
                con_list.append(word)
                for demo in demo_value_list:
                    word_demo_new = word + '$' + demo
                    if word_demo_to_times.has_key(word_demo_new) == True:
                        con_list.append(str(word_demo_to_times[word_demo_new]))
                    else:
                        con_list.append('0')
                out_file_con_list.append('\t'.join(con_list))
            usefulAPI.mk_dir(out_file_fold)
            out_file = out_file_fold + demo_input + '_' + category + '.txt'
            open(out_file,'w+').write('\n'.join(out_file_con_list))

if __name__ == '__main__':
    dat_json_file = '../../../ExpData/MovieData/JsonData/jsonDatForComments.json'
    out_file_fold = '../../../ExpData/MovieData/JsonDatInfo/DemoSpecWordInfo/'
    get_demo_sprc_words = GetDemoSpecWords(dat_json_file)
    get_demo_sprc_words.load_all_dat(cat = 'category')
    get_demo_sprc_words.generate_spec_words_for_demo(out_file_fold,demo_input='age')



