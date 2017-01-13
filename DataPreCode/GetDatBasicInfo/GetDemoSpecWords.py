#encoding=utf-8

# -------------------------------------------------------------------- #
# 获取不同用户属性发表评论的差异性
# 输入N条评论及其用户属性
# 设定要观察的用户属性：性别，年龄？
# 找出评论中特定的属性下，不同维度的用户的用词差异（男 VS 女， 中年人 VS 老年人）
# 添加时间： 2016-12-28 15:40
# -------------------------------------------------------------------- #

class UserDatInfo:
    def __init__(self):
        self.gender = 'NULL'
        self.age = 'NULL'
        self.location = 'NULL'
        self.content = ''


class GetDemoSpecWords:
    def __init__(self,dat_file,demo_file):
        self.dat_file = dat_file
        self.demo_file = demo_file
        self.all_usr_dat_list = []

    def load_dat(self):
        dat_con_list = open(self.dat_file,'r').readlines()
        demo_con_list = open(self.demo_file,'r').readlines()
        if len(dat_con_list) == len(demo_con_list):
            for i in range(0,len(dat_con_list)):
                usr_dat_info = UserDatInfo()
                dat_con = dat_con_list[i].strip()
                usr_dat_info.content = dat_con
                demo_con = demo_con_list[i].strip()
                for demo_str in demo_con.split(' '):
                    demo_list = demo_str.split('/')
                    if len(demo_list) == 1: continue
                    if demo_list[0] == 'Sex':
                        usr_dat_info.gender = demo_str
                    elif demo_list[0] == 'Loc':
                        usr_dat_info.location = demo_str
                    elif demo_list[0] == 'Age':
                        usr_dat_info.age = demo_str
                self.all_usr_dat_list.append(usr_dat_info)

    def get_spec_words_for_gender(self):
        demo2conlist = {}
        for usr_dat in self.all_usr_dat_list:
            if usr_dat.gender == 'NULL': continue
            if demo2conlist.has_key(usr_dat.gender) == False:
                demo2conlist[usr_dat.gender] = []
            demo2conlist[usr_dat.gender].append(usr_dat.content)

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

        for demo , times in demo_to_times.items():
            temp_str = demo + '\t' + str(times)
            out_file_con_list.append(temp_str)

        for word_demo , times in word_demo_to_times.items():
            word = word_demo.split('$')[0]
            temp_str = word
            for demo,times in demo_to_times.items():
                word_demo_new = word + '$' + demo
                if word_demo_to_times.has_key(word_demo_new) == True:
                    temp_str = temp_str + '\t' + demo + '\t' + str(word_demo_to_times[word_demo_new])
                else:
                    temp_str = temp_str + '\t' + demo + '\t0'
            out_file_con_list.append(temp_str)
        open('tetete.txt','w+').write('\n'.join(out_file_con_list))




if __name__ == '__main__':
    get_demo_sprc_words = GetDemoSpecWords('test_doc.txt','test_demo.txt')
    get_demo_sprc_words.load_dat()
    get_demo_sprc_words.get_spec_words_for_gender()



