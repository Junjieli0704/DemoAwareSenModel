#encoding=utf-8
#对数据进行交叉验证的划分
from UsefulLibs import usefulAPI


class DataStruct:
    def __init__(self):
        self.commentID = ''
        self.userID = ''
        self.movieName = ''
        self.sentiLabel = ''
        self.commentCon = ''
        self.userInfo = ''
        self.outConForDoc = ''           # sentence list or sentence
        self.outConForSenList = []       # sentence list or sentence
        self.movieType = ''




class PropressingDat:
    def __init__(self,movie_comment_file,sentiment_word_file,movie_info_file):
        self.movie_comment_file = movie_comment_file
        self.sentiment_word_file = sentiment_word_file
        self.movie_info_file = movie_info_file
        self.sentiment_dict = {}
        self.all_dat_list = []
        self.movie_name_to_dat_list_dict = {}
        self.movie_type_to_dat_list_dict = {}
        self.comment_id_to_dat_dict = {}
        self.movie_name_to_type_dict = {}
        self.movie_type_to_name_list_dict = {}
        self.delete_word_dict = {}

    def load_movie_dat_info(self):
        line_con_list = open(self.movie_info_file,'r').readlines()
        for line_con in line_con_list:
            line_con = line_con.replace('\n','').replace('\r','')
            word_con_list = line_con.split('\t')
            if len(word_con_list) != 11: continue
            movie_name_eng = word_con_list[0].replace(' ','_')
            movie_type = word_con_list[3]
            self.movie_name_to_type_dict[movie_name_eng] = movie_type
            if movie_type.find('/') == -1:
                if movie_type == 'NULL': continue
                self.add_dict_value_list(self.movie_type_to_name_list_dict,movie_type,movie_name_eng)
            else:
                for temp_type in movie_type.split('/'):
                    if temp_type == 'NULL': continue
                    self.add_dict_value_list(self.movie_type_to_name_list_dict,temp_type,movie_name_eng)
        print "load_movie_dat_info() finished......"
        #print self.movie_name_to_type_dict
        #print self.movie_type_to_name_list_dict

    def load_data_struct(self):
        line_con_list = open(self.movie_comment_file,'r').readlines()
        for line_con in line_con_list:
            line_con = line_con.replace('\r','').replace('\n','')
            word_con_list = line_con.split('\t')
            if len(word_con_list) != 6: continue
            if word_con_list[0] == 'CommentID': continue
            temp_struct = DataStruct()
            temp_struct.commentID = word_con_list[0]
            temp_struct.userID = word_con_list[1]
            temp_struct.movieName = word_con_list[2]
            temp_struct.userInfo = word_con_list[3]
            temp_struct.sentiLabel = word_con_list[4]
            temp_struct.commentCon = word_con_list[5]
            temp_struct.movieType = self.movie_name_to_type_dict[temp_struct.movieName]
            if self.get_user_info_no_null_times(temp_struct.userInfo) == 0: continue
            self.all_dat_list.append(temp_struct)
            if self.movie_name_to_dat_list_dict.has_key(temp_struct.movieName) == False:
                self.movie_name_to_dat_list_dict[temp_struct.movieName] = []
            self.movie_name_to_dat_list_dict[temp_struct.movieName].append(temp_struct)

            if temp_struct.movieType.find('/') == -1:
                if temp_struct.movieType == 'NULL': continue
                self.add_dict_value_list(self.movie_type_to_dat_list_dict,temp_struct.movieType,temp_struct)
            else:
                for temp_type in temp_struct.movieType.split('/'):
                    if temp_type == 'NULL': continue
                    self.add_dict_value_list(self.movie_type_to_dat_list_dict,temp_type,temp_struct)

        print "load_data_struct() finished......"

    def load_sentiment_dict(self):
        in_line_con_list = open(self.sentiment_word_file,'r').readlines()
        for line_con in in_line_con_list:
            line_con = line_con.replace('\n','').replace('\r','')
            word_list = line_con.split('\t')
            if len(word_list) == 2:
                word = word_list[0]
                score = int(word_list[1])
                self.sentiment_dict[word] = score

    def add_dict_value(self,dict,key,value = 1):
        if dict.has_key(key):
            dict[key] = dict[key] + value
        else:
            dict[key] = value

    def add_dict_value_list(self,dict,key,value):
        if dict.has_key(key) == False:
            dict[key] = []
        dict[key].append(value)

    def get_user_info_no_null_times(self,user_info_str):
        no_null_times = 0
        for temp_str in user_info_str.split('_'):
            if temp_str.split('/')[1] != 'NULL':
                if temp_str.split('/')[0] != 'Label':
                    no_null_times = no_null_times + 1
        return no_null_times

    def get_delete_word_dict(self,dat_list,common_value = 0.3,rare_value = 5):
        word_to_num_dict = {}
        delete_word_dict = {}
        for temp_dat in dat_list:
            word_pos_con_list = temp_dat.commentCon.split(' ')
            for word_pos in word_pos_con_list:
                word = word_pos.split('/')[0]
                pos = word_pos.split('/')[1]
                if pos == 'PU': continue
                self.add_dict_value(word_to_num_dict,word)
        for word,number in word_to_num_dict.items():
            if self.sentiment_dict.has_key(word): continue
            if number < rare_value: delete_word_dict[word] = 1
            if number > common_value * len(dat_list):  delete_word_dict[word] = 2
        return delete_word_dict


    def get_dat_con_str(self,temp_dat,mode = 'commentIDCon'):
        if mode == 'commentIDCon':
            return temp_dat.commentID + ' ' + temp_dat.outConForDoc
        if mode == 'commentIDDemo':
            out_str = temp_dat.commentID + '_demo'
            for temp_str in temp_dat.userInfo.split('_'):
                if temp_str.split('/')[1] != 'NULL':
                    if temp_str.find('Label') == -1 and temp_str.find('Edu') == -1:
                        out_str = out_str + ' ' + temp_str
            return out_str

    def print_out_dat_list(self,out_file,temp_dat_list,mode = 'commentIDCon'):
        line_con_list = []
        for temp_dat in temp_dat_list:
            line_con_list.append(self.get_dat_con_str(temp_dat,mode))
        open(out_file,'w+').write('\n'.join(line_con_list))

    def print_out_data(self,out_file_fold,dat_list,out_file,demo_file = ''):
        if demo_file == '': demo_file = 'Demo_' + out_file
        out_file = out_file_fold + out_file
        demo_file = out_file_fold + demo_file
        self.print_out_dat_list(out_file,dat_list, mode='commentIDCon')
        self.print_out_dat_list(demo_file,dat_list, mode='commentIDDemo')

    def delete_head_end_kongge(self,temp_str):
        new_str_list = []
        temp_str_list = temp_str.split(' ')
        for t_str in temp_str_list:
            if t_str == '': continue
            #if t_str == '，' or t_str == ',': continue
            new_str_list.append(t_str)
        return ' '.join(new_str_list)

    def generate_sentence_for_one_dat(self,temp_dat,delete_word_dict):
        comment_con_list = [temp_seg_pos.split('/')[0] for temp_seg_pos in temp_dat.commentCon.split(' ')]
        new_content_list = []
        for word in comment_con_list:
            if delete_word_dict.has_key(word): continue
            new_content_list.append(word)
        comment_con = ' '.join(new_content_list)

        split_char_list = ['。','？','?','!','！','…','～','...']
        for split_char in split_char_list:
            comment_con = comment_con.replace(split_char,'。')
        temp_list = comment_con.split('。')
        for temp_str in temp_list:
            temp_str = self.delete_head_end_kongge(temp_str)
            if len(temp_str.split(' ')) < 2: continue
            elif len(temp_str.split(' ')) > 42:
                #print len(temp_str.split(' '))
                temp_str = temp_str.replace(',','，')
                connect_words = ['但是','可是','然而','不过']
                for connect_word in connect_words:
                    temp_str = temp_str.replace(connect_word,'，' + connect_word)
                temp_str_list = temp_str.split('，')
                for t_str in temp_str_list:
                    t_str = self.delete_head_end_kongge(t_str)
                    if len(t_str.split(' ')) < 2: continue
                    elif len(t_str.split(' ')) > 42:
                        print len(t_str.split(' '))
                        temp_dat.outConForSenList.append('NNNNNNNNNNNNNN')
                        temp_dat.outConForSenList.append(t_str)
                    else: temp_dat.outConForSenList.append(t_str)

            else:
                temp_dat.outConForSenList.append(temp_str)

    def generate_sentences(self,temp_dat_list,delete_word_dict = {}):
        for temp_dat in temp_dat_list:
            self.generate_sentence_for_one_dat(temp_dat,delete_word_dict)

    def print_out_sen_data(self,dat_list,out_file):
        out_file_list = []
        for temp_dat in dat_list:
            for i in range(0,len(temp_dat.outConForSenList)):
                temp_str = temp_dat.commentID + '_s' + str(i+1) + ' ' + temp_dat.outConForSenList[i]
                #temp_str = temp_dat.outConForSenList[i]
                #out_file_list.append(temp_str + "\t" + str(len(temp_str.split(" "))))
                out_file_list.append(temp_str)
        open(out_file,'w+').write('\n'.join(out_file_list))
        new_out_file = out_file.replace('.txt','') + '_content.txt'
        out_file_list = []
        for temp_dat in dat_list:
            for i in range(0,len(temp_dat.outConForSenList)):
                temp_str = temp_dat.outConForSenList[i]
                out_file_list.append(temp_str)
        open(new_out_file,'w+').write('\n'.join(out_file_list))

    def generate_doc_content(self,dat_list,is_need_prun,common_value,rare_value):
        delete_word_dict = self.get_delete_word_dict(dat_list,common_value,rare_value)
        delete_word_dict = {}
        for temp_dat in dat_list:
            new_content_list = []
            word_pos_con_list = temp_dat.commentCon.split(' ')
            for word_pos in word_pos_con_list:
                word = word_pos.split('/')[0]
                pos = word_pos.split('/')[1]
                if is_need_prun == False:
                    if pos == 'PU': continue
                if delete_word_dict.has_key(word):continue
                new_content_list.append(word_pos)
            temp_dat.outConForDoc = ' '.join(new_content_list)


    def preprocess_dat(self,out_file_fold,
                       mode = 'Doc',
                       style = 'allMovie',
                       common_value = 0.3,
                       rare_value = 2,
                       is_need_prun = True,
                       out_file = './out.txt'):
        self.load_sentiment_dict()
        self.load_movie_dat_info()
        self.load_data_struct()
        usefulAPI.mkDir(out_file_fold)
        if mode == 'Doc':
            if style == 'allMovie':
                self.generate_doc_content(self.all_dat_list,is_need_prun,common_value,rare_value)
                self.print_out_data(out_file_fold,self.all_dat_list,out_file)
            elif style == 'typeMovie':
                for type, dat_list in self.movie_type_to_dat_list_dict.items():
                    if len(self.movie_type_to_name_list_dict[type]) < 4: continue
                    print type + ' / ' + str(len(dat_list)) + ' / ' + str(len(self.movie_type_to_name_list_dict[type]))
                    self.generate_doc_content(dat_list,is_need_prun,common_value,rare_value)
                    new_out_file = mode + '_' + type + '_' + out_file
                    self.print_out_data(out_file_fold,dat_list,new_out_file)
            elif style == 'eachMovie':
                for movie_name, dat_list in self.movie_name_to_dat_list_dict.items():
                    print len(dat_list)
                    out_file1 = movie_name + '_' + out_file
                    self.generate_doc_content(dat_list,is_need_prun,common_value,rare_value)
                    self.print_out_data(out_file_fold,dat_list,out_file1)

        elif mode == 'Sen':
            if style == 'allMovie':
                #delete_word_dict = self.get_delete_word_dict(self.all_dat_list,common_value,rare_value)
                #self.generate_sentences(self.all_dat_list,delete_word_dict)
                self.generate_sentences(self.all_dat_list)
                self.print_out_sen_data(self.all_dat_list,out_file)


if __name__ == '__main__':
    movie_comment_file = './Data/DataForDemoGroupSensitiveAspectMining.txt'
    sentiment_word_file = './Data/sentiment_word_list.txt'
    movie_info_file = './Data/DataForDemoGroupSensitiveAspectMining_AllMovieInfo.txt'
    out_file_fold = './DocData6/'
    preDat = PropressingDat(movie_comment_file,sentiment_word_file,movie_info_file)
    #preDat.preprocess_dat(out_file_fold,mode = 'Doc',style='typeMovie',out_file='DataForLDAAspectMining.txt')
    preDat.preprocess_dat(out_file_fold,mode = 'Doc',style='eachMovie',out_file='DataForMiningAspectDoc.txt')

