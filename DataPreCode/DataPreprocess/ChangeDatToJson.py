#encoding=utf-8


# -------------------------------------------------------------------- #
# 将无结构数据转化成XML数据
# XML数据结构类型：
#    comment_id                          评论ID，
#    user_iD                             用户ID，发布评论的用户ID
#    movie_name                          电影名称
#    user_info                           用户信息
#    senti_label                         句子标签，褒贬
#    movie_type                          电影类型
#    con_for_doc_dict                    记录整篇文档内容
#        content                            文档内容
#        segmentation                       分词结果
#        postag                             POSTag结果
#        dependency                         依存分析结果
#    con_for_sen_list                    记录每个句子
#        sentence_1
#            content
#            segmentation
#            postag
#            dependency
#        Sentence_2
#            content
#            segmentation
#            postag
#            dependency
# Time: 2017-01-13
# -------------------------------------------------------------------- #

import sys
sys.path.append("../UsefulLibs")
import usefulAPI, xmlAPI, jsonAPI

# 用dict定义我们的数据，是为了后面能很方便的转换成json
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
            temp_struct = get_dat_struct_dict()
            temp_struct['comment_id'] = word_con_list[0]
            temp_struct['user_id'] = word_con_list[1]
            temp_struct['movie_name'] = word_con_list[2]
            temp_struct['user_info'] = word_con_list[3]
            temp_struct['senti_label'] = word_con_list[4]
            temp_struct['movie_type'] = self.movie_name_to_type_dict[temp_struct['movie_name']]
            if self.get_user_info_no_null_times(temp_struct['user_info']) == 0: continue
            temp_struct['con_for_doc_dict'] = self.get_con_dict_from_content(word_con_list[5])
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
        comment_con = temp_dat['con_for_doc_dict']['segmentation']
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
                    temp_dat['con_for_sen_list'].append(temp_dict)
            else:
                temp_dict = get_con_dat_dict()
                temp_dict['content'] = ''.join(temp_str.split(' '))
                temp_dict['segmentation'] = temp_str
                temp_dict['postag'] = 'NULL'
                temp_dict['dependency'] = 'NULL'
                temp_dat['con_for_sen_list'].append(temp_dict)

    def generate_sentences(self):
        for temp_dat in self.all_dat_list:
            self.generate_sentence_for_one_dat(temp_dat)

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
            for temp_dict in temp_dat['con_for_sen_list']:
                out_con_list.append(self.change_dict_to_str(temp_dict))
        open(out_file,'w+').write('\n'.join(out_con_list))

    def print_out_split_sen_dat(self,out_file):
        out_con_list = []
        for temp_dat in self.all_dat_list:
            for temp_dict in temp_dat['con_for_sen_list']:
                out_con_list.append(self.change_dict_to_str(temp_dict,mode='segmentation'))
        open(out_file,'w+').write('\n'.join(out_con_list))



    def print_out_json_file(self,dat_list = [], out_file = 'out.txt'):
        if len(dat_list) == 0:
            dat_list = self.all_dat_list
        jsonAPI.print_out_dat_json(dat_list,out_file)
        jsonAPI.print_out_dat_json_visual(dat_list,out_file.replace('.json','.jsonVis'))

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
            if len(dat_info['con_for_sen_list']) != 0:
                for sen_info in dat_info['con_for_sen_list']:
                    if sen_number >= len(dep_info_list):
                        print 'error in sen_number >= len(dep_info_list):'
                    sen_info['dependency'] = dep_info_list[sen_number]
                    sen_number = sen_number + 1


    # -------------------------------------------------------------------- #
    # Fun: Generate movie data for each category (Love, Comedy and so on).
    #      从所有数据中，生成每个类别的数据
    # Time: 2017-01-16
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

        usefulAPI.mk_dir(out_file_fold)
        for movie_type, id_list in movie_type_to_id_list_dict.items():
            id_list = list(set(id_list))
            dat_list = []
            for i in id_list:
                dat_list.append(self.all_dat_list[i])
            out_file = out_file_fold + movie_type + '.json'
            self.print_out_json_file(dat_list,out_file)


def get_raw_txt_dat(in_movie_comment_file,out_movie_comment_file):
    line_con_list = open(in_movie_comment_file,'r').readlines()
    out_line_con_list = []
    for line_con in line_con_list:
        word_con_list = line_con.split('\t')
        if len(word_con_list) != 6: continue
        if word_con_list[5] == 'MovieComment_POS': continue
        new_word_list = []
        for word in word_con_list[5].split(' '):
            if word.find('/') == -1: continue
            if len(word.split('/')) == 2:
                new_word_list.append(word.split('/')[0])
            elif len(word.split('/')) == 3:
                new_word_list.append('/')
        word_con_list.pop()
        word_con_list.append(''.join(new_word_list))
        out_line_con_list.append('\t'.join(word_con_list))
    open(out_movie_comment_file,'w+').write('\n'.join(out_line_con_list))

def get_raw_txt(in_movie_comment_file,out_movie_comment_file):
    line_con_list = open(in_movie_comment_file,'r').readlines()
    out_line_con_list = []
    for line_con in line_con_list:
        word_con_list = line_con.split('\t')
        if len(word_con_list) != 6: continue
        if word_con_list[0] == 'CommentID': continue
        out_line_con_list.append(''.join(word_con_list[5].strip()))
    open(out_movie_comment_file,'w+').write('\n'.join(out_line_con_list))

def get_movie_name(in_movie_comment_file,out_movie_comment_file):
    line_con_list = open(in_movie_comment_file,'r').readlines()
    out_line_con_list = []
    for line_con in line_con_list:
        word_con_list = line_con.split('\t')
        if len(word_con_list) != 6: continue
        if word_con_list[0] == 'CommentID': continue
        out_line_con_list.append(''.join(word_con_list[2].strip()))
    open(out_movie_comment_file,'w+').write('\n'.join(out_line_con_list))

def check_user_dict(in_file,out_file):
    in_line_con_list = open(in_file,'r').readlines()
    con_dict = {}
    out_line_con_list = []
    for line_con in in_line_con_list:
        line_con = line_con.strip()
        if con_dict.has_key(line_con): continue
        con_dict[line_con] = 1
        out_line_con_list.append(line_con)
    open(out_file,'w+').write('\n'.join(out_line_con_list))

def check_senti_word_in_src_dat(senti_word_file = '../../../ExpData/SentiWordDat/ReviseSentiWord/revise_sentiment_word_list.txt',
                                txt_dat_file = '../../../ExpData/MovieData/RawData/RawSenDataForComments.txt'):
    senti_line_con_list = open(senti_word_file,'r').readlines()
    txt_dat_con_list = open(txt_dat_file,'r').readlines()
    senti_dict = {}
    senti_list = []
    for con in senti_line_con_list:
        con = con.strip()
        senti_word = con.split('\t')[0]
        if senti_dict.has_key(senti_word):continue
        senti_dict[senti_word] = 0
        senti_list.append(senti_word)

    for i in range(0,len(txt_dat_con_list)):
        if i % 100 == 0:
            print str(i) + ' / ' + str(len(txt_dat_con_list))
        dat_con = txt_dat_con_list[i].strip()
        for senti_word in senti_list:
            if dat_con.find(senti_word) == -1: continue
            #print dat_con.count(senti_word)
            senti_dict[senti_word] = dat_con.count(senti_word) + senti_dict[senti_word]
        #if i > 100 : break

    out_line_con_list = []

    for key,value in senti_dict.items():
        if value < 10: continue
        out_line_con_list.append(key + '\t' + str(value))

    open('test.txt','w+').write('\n'.join(out_line_con_list))
    senti_list = sorted(senti_dict, cmp=lambda x,y:cmp(x[1],y[1]),reverse=True)

    '''
    #print senti_dict

    senti_list = sorted(senti_dict, cmp=lambda x,y:cmp(x[1],y[1]),reverse=True)

    print senti_list[0].decode('utf-8')
    print senti_list[1].decode('utf-8')


    #out_line_con_list = [couple[0] + '\t' + str(couple[1]) for couple in senti_list]
    out_line_con_list = [str(couple[1]) for couple in senti_list]
    open('test.txt','w+').write('\n'.join(out_line_con_list))
    '''

def check_senti_word_in_segpos_dat(senti_word_file = '../../../ExpData/SentiWordDat/ReviseSentiWord/revise_sentiment_word_list.txt',
                                   senti_to_num_in_src_file = './test.txt',
                                   seg_file = '../../../ExpData/MovieData/RawData/Urheen_Res/RawSenDataForComments_Urheen_seg.txt',
                                   out_file = 'out.txt'):
    senti_to_num_in_src_dict = {}
    senti_to_polarity_dict = {}
    senti_to_num_in_seg_dict = {}
    out_line_con_list = []
    out_line_con_list.append('senti\tnum_in_src\tnum_in_postag\tpolarity')
    for con in open(senti_word_file,'r').readlines():
        con = con.strip()
        senti_word = con.split('\t')[0]
        senti_to_polarity_dict[senti_word] = con.split('\t')[1]
        senti_to_num_in_seg_dict[senti_word] = 0
        senti_to_num_in_src_dict[senti_word] = 0

    for con in open(senti_to_num_in_src_file,'r').readlines():
        con = con.strip()
        senti_word = con.split('\t')[0]
        senti_to_num_in_src_dict[senti_word] = int(con.split('\t')[1])

    for con in open(seg_file,'r').readlines():
        con = con.strip()
        word_list = con.split(' ')
        for word in word_list:
            if senti_to_num_in_seg_dict.has_key(word):
                senti_to_num_in_seg_dict[word] = senti_to_num_in_seg_dict[word] + 1

    for senti_word, polarity in senti_to_polarity_dict.items():
        if senti_to_num_in_src_dict[senti_word] == 0: continue
        if len(senti_word) <= 4: continue
        temp_list = []
        temp_list.append(senti_word)
        temp_list.append(str(senti_to_num_in_src_dict[senti_word]))
        temp_list.append(str(senti_to_num_in_seg_dict[senti_word]))
        temp_list.append(senti_to_polarity_dict[senti_word])
        out_line_con_list.append('\t'.join(temp_list))
    open(out_file,'w+').write('\n'.join(out_line_con_list))







if __name__ == '__main__':

    #check_user_dict('../../../ExpData/UserDat/user_dict.txt','../../../ExpData/UserDat/user_dict.txt')
    #check_senti_word_in_src_dat()


    check_senti_word_in_segpos_dat()
    '''
    in_raw_dat_filefold = '../../../ExpData/MovieData/RawData/'
    in_movie_struct_file = in_raw_dat_filefold + 'MovieStructDataForComments.txt'
    in_raw_movie_comment_file = in_raw_dat_filefold + 'RawSenDataForComments.txt'

    in_movie_info_file = in_raw_dat_filefold + 'MovieInfo.txt'
    #in_dep_file = in_raw_dat_filefold + 'DepForSenSplit.txt'
    #out_sen_file = in_raw_dat_filefold + 'SenSplitForRawTxt.txt'
    out_json_file = '../../../ExpData/MovieData/JsonData/jsonDatForComments.json'
    out_movie_comment_file = in_raw_dat_filefold + 'RawSenDataForComments.txt'
    out_movie_comment_con_file = in_raw_dat_filefold + 'SenDataForComments.txt'
    get_raw_txt(in_movie_struct_file,in_raw_movie_comment_file)
    '''
    in_raw_dat_filefold = '../../../ExpData/MovieData/RawData/'
    in_movie_struct_file = in_raw_dat_filefold + 'MovieStructDataForComments.txt'
    in_movie_name_file = in_raw_dat_filefold + 'RawMovieNameForComments.txt'
    get_movie_name(in_movie_struct_file,in_movie_name_file)


    '''
    preDat = PropressingDat(in_movie_comment_file,in_movie_info_file)
    preDat.load_movie_dat_info()
    preDat.load_data_struct()
    preDat.generate_sentences()
    preDat.print_out_split_sen_dat(out_sen_file)
    # 如果没有现成的依存分析结果，可以使用依存分析器分析下 out_sen_file，得到的结果然后在load_dependency_file
    preDat.load_dependency_file(in_dep_file)
    preDat.print_out_json_file(out_file=out_json_file)

    out_each_category_dat_filefold = '../../../ExpData/MovieData/JsonDatForEachCat/'
    preDat.split_dat_accord_type(out_each_category_dat_filefold)
    '''