#encoding=utf-8

'''
CommentID
UserID
MovieName
UserInfo
SentiLabel
MovieType
MovieCommentCon_Doc
	Content
	Segmentation
	PosTag
	Dependency
MovieCommentCon_Sen
	Sentence_1
		Content
		Segmentation
		PosTag
		Dependency
	Sentence_2
		Content
		Segmentation
		PosTag
		Dependency
'''

import xmlAPI
import usefulAPI
import sys

reload(sys)
sys.setdefaultencoding('utf8')

def get_con_dat_dict():
    temp_dict = {}
    temp_dict['content'] = ''
    temp_dict['segmentation'] = ''
    temp_dict['postag'] = ''
    temp_dict['dependency'] = ''
    temp_dict['aspect'] = ''
    return temp_dict


class DataStruct:
    def __init__(self):
        self.commentID = ''
        self.userID = ''
        self.movieName = ''
        self.sentiLabel = ''
        self.userInfo = ''
        self.movieType = ''
        self.conForDoc = {}
        self.outConForSenList = []



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
            line_con = line_con.replace('\r','').replace('\n','')
            line_con = line_con.decode('utf-8').encode('utf-8')
            word_con_list = line_con.split('\t')
            if len(word_con_list) != 6: continue
            if word_con_list[0] == 'CommentID': continue
            temp_struct = DataStruct()
            temp_struct.commentID = word_con_list[0]
            temp_struct.userID = word_con_list[1]
            temp_struct.movieName = word_con_list[2]
            temp_struct.userInfo = word_con_list[3]
            temp_struct.sentiLabel = word_con_list[4]
            temp_struct.movieType = self.movie_name_to_type_dict[temp_struct.movieName]
            if self.get_user_info_no_null_times(temp_struct.userInfo) == 0: continue
            temp_struct.conForDoc = self.get_con_dict_from_content(word_con_list[5])
            self.all_dat_list.append(temp_struct)
        print "load_data_struct() finished......"

    def get_con_dict_from_content(self,temp_content):
        word_list = []
        pos_list = []
        for word_pos in temp_content.split(' '):
            word_pos_list = word_pos.split('/')
            if len(word_pos_list) == 2:
                word_list.append(word_pos_list[0])
                pos_list.append(word_pos_list[1])
            elif len(word_pos_list) == 3:
                if word_pos_list[2] == 'PU':
                    word_list.append('/')
                    pos_list.append('PU')
                else:
                    word_list.append(word_pos_list[0] + '/' + word_pos_list[1])
                    pos_list.append(word_pos_list[2])
        temp_dict = get_con_dat_dict()
        temp_dict['content'] = ''.join(word_list)
        temp_dict['segmentation'] = ' '.join(word_list)
        temp_dict['postag'] = ' '.join(pos_list)
        temp_dict['dependency'] = 'NULL'
        return temp_dict


    def get_user_info_no_null_times(self,user_info_str):
        no_null_times = 0
        for temp_str in user_info_str.split('_'):
            if temp_str.split('/')[1] != 'NULL':
                if temp_str.split('/')[0] != 'Label':
                    no_null_times = no_null_times + 1


        return no_null_times


    def delete_head_end_kongge(self,temp_str):
        new_str_list = []
        temp_str_list = temp_str.split(' ')
        for t_str in temp_str_list:
            if t_str == '': continue
            new_str_list.append(t_str)
        return ' '.join(new_str_list)

    def generate_sentence_for_one_dat(self,temp_dat):
        comment_con = temp_dat.conForDoc['segmentation']
        split_char_list = ['。','？','?','!','！','…','～','...']
        for split_char in split_char_list:
            comment_con = comment_con.replace(split_char,'。')
        temp_list = comment_con.split('。')
        for temp_str in temp_list:
            temp_str = self.delete_head_end_kongge(temp_str)
            if temp_str == '': continue
            if len(temp_str.split(' ')) < 2: continue
            if len(temp_str.split(' ')) > 42:
                temp_str = temp_str.replace(',','，')
                connect_words = ['但是','可是','然而','不过']
                for connect_word in connect_words:
                    temp_str = temp_str.replace(connect_word,'，' + connect_word)
                temp_str_list = temp_str.split('，')
                for t_str in temp_str_list:
                    t_str = self.delete_head_end_kongge(t_str)
                    if len(t_str.split(' ')) < 2: continue
                    if len(t_str.split(' ')) > 42:
                        print len(t_str.split(' '))
                    if t_str == '': continue
                    temp_dict = get_con_dat_dict()
                    temp_dict['content'] = ''.join(t_str.split(' '))
                    temp_dict['segmentation'] = t_str
                    temp_dict['postag'] = 'NULL'
                    temp_dict['dependency'] = 'NULL'
                    temp_dat.outConForSenList.append(temp_dict)
            else:
                temp_dict = get_con_dat_dict()
                temp_dict['content'] = ''.join(temp_str.split(' '))
                temp_dict['segmentation'] = temp_str
                temp_dict['postag'] = 'NULL'
                temp_dict['dependency'] = 'NULL'
                temp_dat.outConForSenList.append(temp_dict)

    def generate_sentences(self):
        for temp_dat in self.all_dat_list:
            self.generate_sentence_for_one_dat(temp_dat)


    def load_all_sentence(self):
        sen_number_to_comment_id_dict = {}
        line_con_list = open(self.in_review_file,'r').readlines()
        for i in range(0,len(line_con_list)):
            line_con = line_con_list[i].replace('\r','').replace('\n','')
            comment_id = line_con.split(' ')[0]
            sen_number = i + 1
            sen_number_to_comment_id_dict[sen_number] = comment_id

        dp_line_con_list = open(self.in_review_dep_file,'r').readlines()
        is_after_load_comment_id = False
        is_after_load_content = False
        is_after_load_dep_res = False
        for line_con in dp_line_con_list:
            line_con = line_con.replace('\r','').replace('\n','')
            word_con_list = line_con.split(' ')
            if is_after_load_comment_id == False:
                if word_con_list[0] == 'Parsing':
                    if word_con_list[1] == '[sent.':
                        comment_id = sen_number_to_comment_id_dict[int(word_con_list[2])]
                        is_after_load_comment_id = True
                        sen_info = sentenceInfo()
                        sen_info.comment_id = comment_id
                        self.all_sentence_list.append(sen_info)
            elif is_after_load_comment_id and is_after_load_content == False:
                if word_con_list[0] == 'Sentence' or word_con_list[0] == 'FactoredParser:': continue
                curr_sen_info = self.all_sentence_list[len(self.all_sentence_list) - 1]
                for word in word_con_list:
                    if len(word.split('/')) == 2:
                        curr_sen_info.word_list.append(word.split('/')[0])
                        curr_sen_info.pos_list.append(word.split('/')[1])
                is_after_load_content = True
                if len(curr_sen_info.word_list) == 1:
                    is_after_load_comment_id = False
                    is_after_load_content = False
                    is_after_load_dep_res = False
            elif is_after_load_comment_id and is_after_load_content and is_after_load_dep_res == False:
                temp_con = line_con.replace('(','-').replace(', ','-').replace(')','-');
                temp_list = temp_con.split('-')
                curr_sen_info = self.all_sentence_list[len(self.all_sentence_list) - 1]
                if len(temp_list) == 6:
                    if temp_list[1] == 'ROOT': continue
                    dep_dict = {}
                    dep_dict['rel'] = temp_list[0]
                    dep_dict['left'] = int(temp_list[2]) - 1
                    dep_dict['right'] = int(temp_list[4]) - 1
                    curr_sen_info = self.all_sentence_list[len(self.all_sentence_list) - 1]
                    curr_sen_info.dp_list.append(dep_dict)
                elif line_con == '' and len(curr_sen_info.dp_list) > 0:
                    is_after_load_comment_id = False
                    is_after_load_content = False
                    is_after_load_dep_res = False


    def print_temp_dat(self):
        for temp_dat in self.all_dat_list:
            print temp_dat.commentID
            print temp_dat.userID
            print temp_dat.movieName
            print temp_dat.sentiLabel
            print temp_dat.userInfo
            print temp_dat.movieType
            print temp_dat.conForDoc
            print temp_dat.outConForSenList
            break

    def change_dict_to_str(self,temp_dict,mode = 'alldat'):
        if mode == 'alldat':
            temp_str = ''
            for (key,value) in temp_dict.items():
                temp_str = temp_str + key + '-_-' + value + '-_-'
            return temp_str
        elif mode == 'segmentation':
            return temp_dict['segmentation']

    def print_out_all_dat(self,out_file):
        out_con_list = []
        for temp_dat in self.all_dat_list:
            out_con_list.append(temp_dat.commentID)
            out_con_list.append(temp_dat.userID)
            out_con_list.append(temp_dat.movieName)
            out_con_list.append(temp_dat.sentiLabel)
            out_con_list.append(temp_dat.userInfo)
            out_con_list.append(temp_dat.movieType)
            out_con_list.append(self.change_dict_to_str(temp_dat.conForDoc))
            for temp_dict in temp_dat.outConForSenList:
                out_con_list.append(self.change_dict_to_str(temp_dict))
        open(out_file,'w+').write('\n'.join(out_con_list))

    def print_out_split_sen_dat(self,out_file):
        out_con_list = []
        for temp_dat in self.all_dat_list:
            for temp_dict in temp_dat.outConForSenList:
                out_con_list.append(self.change_dict_to_str(temp_dict,mode='segmentation'))
        open(out_file,'w+').write('\n'.join(out_con_list))

    def print_out_xml_file(self,dat_list,out_file):
        xmlAPI.print_out_all_dat_list(dat_list,out_file)


    def load_dependency_file(self,sen_dep_file):
        dep_info_list = []
        dp_line_con_list = open(sen_dep_file,'r').readlines()
        is_after_load_sen_number = False
        is_after_load_content = False
        is_after_load_dep_res = False
        dep_content_list = []
        for i in range(0,len(dp_line_con_list)):
            line_con = dp_line_con_list[i]
            line_con = line_con.replace('\r','').replace('\n','')
            word_con_list = line_con.split(' ')
            if is_after_load_sen_number == False:
                if word_con_list[0] == 'Parsing':
                    if word_con_list[1] == '[sent.':
                        is_after_load_sen_number = True
            elif is_after_load_sen_number and is_after_load_content == False:
                if word_con_list[0] == 'Sentence' or word_con_list[0] == 'FactoredParser:': continue
                word_list = []
                for word in word_con_list:
                    if len(word.split('/')) == 2:
                        word_list.append(word.split('/')[0])
                is_after_load_content = True
                if len(word_list) == 1:
                    is_after_load_sen_number = False
                    is_after_load_content = False
                    is_after_load_dep_res = False
                    dep_info_list.append('NULL')
            elif is_after_load_sen_number and is_after_load_content and is_after_load_dep_res == False:
                temp_con = line_con.replace('(','-').replace(', ','-').replace(')','-')
                temp_list = temp_con.split('-')
                if len(temp_list) == 6:
                    if temp_list[1] != 'ROOT':
                        dep_content_list.append(temp_con)
                elif len(temp_list) == 1 and len(dep_content_list) > 0:
                    is_after_load_sen_number = False
                    is_after_load_content = False
                    is_after_load_dep_res = False
                    dep_info_list.append('****'.join(dep_content_list))
                    dep_content_list = []
        sen_number = 0
        for dat_info in self.all_dat_list:
            if len(dat_info.outConForSenList) != 0:
                for sen_info in dat_info.outConForSenList:
                    if sen_number >= len(dep_info_list):
                        print 'error in sen_number >= len(dep_info_list):'
                    sen_info['dependency'] = dep_info_list[sen_number]
                    sen_number = sen_number + 1

    def split_dat_accord_type(self, out_file_fold):
        movie_type_to_dat_list_dict = {}
        for temp_dat in self.all_dat_list:
            movie_type_list = temp_dat.movieType.split('/')
            for movie_type in movie_type_list:
                if movie_type_to_dat_list_dict.has_key(movie_type) == False:
                    movie_type_to_dat_list_dict[movie_type] = []
                movie_type_to_dat_list_dict[movie_type].append(temp_dat)

        usefulAPI.mkDir(out_file_fold)

        for movie_type, dat_list in movie_type_to_dat_list_dict.items():
            out_file = out_file_fold + movie_type + '.xml'
            self.print_out_xml_file(dat_list,out_file)



def get_user_comment_times(movie_comment_file,out_file):
    line_con_list = open(movie_comment_file,'r').readlines()
    user_id_dict = {}
    for line_con in line_con_list:
        line_con = line_con.replace('\r','').replace('\n','')
        line_con = line_con.decode('utf-8').encode('utf-8')
        word_con_list = line_con.split('\t')
        if len(word_con_list) != 6: continue
        if word_con_list[0] == 'CommentID': continue
        user_id = word_con_list[1]
        if user_id_dict.has_key(user_id):
            user_id_dict[user_id] = user_id_dict[user_id] + 1
        else:
            user_id_dict[user_id] = 1
    dict= sorted(user_id_dict.iteritems(), key=lambda d:d[1], reverse = True)
    out_file_con_list = []
    for temp_dict in dict:
        file_con = temp_dict[0] + '\t' + str(temp_dict[1])
        out_file_con_list.append(file_con)
    open(out_file,'w+').write('\n'.join(out_file_con_list))




if __name__ == '__main__':
    '''
    movie_comment_file = './Data/DataForDemoGroupSensitiveAspectMining.txt'
    movie_info_file = './Data/DataForDemoGroupSensitiveAspectMining_AllMovieInfo.txt'
    preDat = PropressingDat(movie_comment_file,movie_info_file)
    preDat.load_movie_dat_info()
    preDat.load_data_struct()
    preDat.generate_sentences()
    preDat.load_dependency_file('./OutData/split_sen_dp.txt')
    #preDat.print_out_all_dat('./OutData/all_dat.txt')
    #preDat.print_out_split_sen_dat('./OutData/split_sen.txt')
    preDat.print_out_xml_file(preDat.all_dat_list,'./OutData/all_dat.xml')
    preDat.split_dat_accord_type('./TypeData/')
    '''

    get_user_comment_times('./Data/DataForDemoGroupSensitiveAspectMining.txt','tttt.txt')
