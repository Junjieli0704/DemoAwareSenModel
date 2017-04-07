#encoding=utf-8
import json



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
# Time: 2017-01-25
# -------------------------------------------------------------------- #

def print_out_struct_dat_json_visual(dat_list,json_con_visual_file):
    # 由于json里面的文件的汉字都是unicode编码的，人工阅读不变，于是顺便生成一个适合人阅读的文件
    out_con_list = []
    for each_dat in dat_list:
        temp_str = "each_dat['comment_id']\t" + each_dat['comment_id']
        out_con_list.append(temp_str)
        temp_str = "each_dat['user_id']\t" + each_dat['user_id']
        out_con_list.append(temp_str)
        temp_str = "each_dat['movie_name']\t" + each_dat['movie_name']
        out_con_list.append(temp_str)
        temp_str = "each_dat['senti_label']\t" + each_dat['senti_label']
        out_con_list.append(temp_str)
        temp_str = "each_dat['movie_type']\t" + each_dat['movie_type']
        out_con_list.append(temp_str)
        temp_str = "each_dat['user_info']\t" + each_dat['user_info']
        out_con_list.append(temp_str)
        temp_str = "each_dat['doc_dict']['raw_con']\t"  + each_dat['doc_dict']['raw_con'].encode('utf-8')
        out_con_list.append(temp_str)
        temp_str = "each_dat['doc_dict']['seg_con']\t"  + each_dat['doc_dict']['seg_con'].encode('utf-8')
        out_con_list.append(temp_str)
        temp_str = "each_dat['doc_dict']['pos_con']\t"  + each_dat['doc_dict']['pos_con'].encode('utf-8')
        out_con_list.append(temp_str)
        out_con_list.append("each_dat['doc_dict']['sen_list']:")
        for i in range(0,len(each_dat['doc_dict']['sen_list'])):
            temp_dict = each_dat['doc_dict']['sen_list'][i]
            out_con_list.append('Sen ' + str(i) + ' :')
            temp_str = "\teach_dat['doc_dict']['sen_list'][" + str(i) + "]['raw']" + "\t" + temp_dict['raw'].encode('utf-8')
            out_con_list.append(temp_str)
            temp_str = "\teach_dat['doc_dict']['sen_list'][" + str(i) + "]['seg']" + "\t" + temp_dict['seg'].encode('utf-8')
            out_con_list.append(temp_str)
            temp_str = "\teach_dat['doc_dict']['sen_list'][" + str(i) + "]['pos']" + "\t" + temp_dict['pos'].encode('utf-8')
            out_con_list.append(temp_str)
            temp_str = "\teach_dat['doc_dict']['sen_list'][" + str(i) + "]['dep']" + "\t" + temp_dict['dep'].encode('utf-8')
            out_con_list.append(temp_str)
        out_con_list.append('-----------------------------------')
    open(json_con_visual_file,'w+').write('\n'.join(out_con_list))


# -------------------------------------------------------------------- #
#  doc_dict                        内容dict，包含原始数据、分词、词性标注、依存分析
#  doc_dict['raw_con']             原始数据
#  doc_dict['sen_list'] = []       每个小句的信息
#  doc_dict['sen_list'][0]         第一个小句的基本信息
#  doc_dict['sen_list'][0]['raw']  第一个小句的 raw 信息
#  doc_dict['sen_list'][0]['seg']  第一个小句的 seg 信息
#  doc_dict['sen_list'][0]['pos']  第一个小句的 pos 信息
#  doc_dict['sen_list'][0]['dep']  第一个小句的 dep 信息
# Time: 2017-01-25
# -------------------------------------------------------------------- #
def print_out_comment_dat_json_visual(dat_list,json_con_visual_file):
    # 由于json里面的文件的汉字都是unicode编码的，人工阅读不变，于是顺便生成一个适合人阅读的文件
    out_con_list = []
    for doc_dict in dat_list:
        temp_str = 'raw_con\t' + doc_dict['raw_con']
        out_con_list.append(temp_str)
        temp_str = 'seg_con\t' + doc_dict['seg_con']
        out_con_list.append(temp_str)
        temp_str = 'pos_con\t' + doc_dict['pos_con']
        out_con_list.append(temp_str)
        out_con_list.append('con_for_sen_list:')
        for i in range(0,len(doc_dict['sen_list'])):
            temp_dict = doc_dict['sen_list'][i]
            out_con_list.append('Sen ' + str(i+1) + ' :')
            temp_str = '\traw\t' + temp_dict['raw']
            out_con_list.append(temp_str)
            temp_str = '\tseg\t' + temp_dict['seg']
            out_con_list.append(temp_str)
            temp_str = '\tpos\t' + temp_dict['pos']
            out_con_list.append(temp_str)
            temp_str = '\tdep\t' + temp_dict['dep']
            out_con_list.append(temp_str)
        out_con_list.append('-----------------------------------')
    open(json_con_visual_file,'w+').write('\n'.join(out_con_list))


def print_out_dat_json(dat_list,json_file):
    temp_dict = {}
    temp_dict['data'] = dat_list
    json_str = json.dumps(temp_dict)
    open(json_file,'w+').write(json_str)

def print_out_json(dat_dict,json_file):
    json_str = json.dumps(dat_dict)
    open(json_file,'w+').write(json_str)




# 从json格式的数据文件中读入数据：
#   @json_file: 数据文件名
#   @encoding:  数据存放 utf-8 或者是 unicode
def load_json_movie_dat(json_file,encoding = 'utf-8'):
    if encoding == 'unicode':
        return json.loads(open(json_file,'r').read())['data']
    elif encoding == 'utf-8':
        data = json.loads(open(json_file,'r').read())
        old_dat_list = data['data']
        new_dat_list = []
        for old_dat in old_dat_list:
            new_dat = {}
            for key,value in old_dat.items():
                if key == 'con_for_doc_dict':
                    doc_dict = {}
                    for doc_key,doc_value in old_dat['con_for_doc_dict'].items():
                        doc_dict[doc_key] = doc_value.encode('utf-8')
                    new_dat['con_for_doc_dict'] = doc_dict
                elif key == 'con_for_sen_list':
                    sen_list = []
                    for sen_info in old_dat['con_for_sen_list']:
                        sen_dict = {}
                        for sen_key,sen_value in sen_info.items():
                            sen_dict[sen_key] = sen_value.encode('utf-8')
                        sen_list.append(sen_dict)
                    new_dat['con_for_sen_list'] = sen_list
                else:
                    new_dat[key] = value.encode('utf-8')
            new_dat_list.append(new_dat)
        return new_dat_list

'''
# 从json格式的数据文件中读入数据：
#   @json_file: 数据文件名
#   @encoding:  数据存放 utf-8 或者是 unicode
def load_json_movie_dat(json_file,encoding = 'utf-8'):
    if encoding == 'unicode':
        return json.loads(open(json_file,'r').read())['data']
    elif encoding == 'utf-8':
        data = json.loads(open(json_file,'r').read())
        old_dat_list = data['data']
        new_dat_list = []
        for old_dat in old_dat_list:
            new_dat = {}
            for key,value in old_dat.items():
                if key == 'doc_dict':
                    doc_dict = {}
                    for doc_key,doc_value in old_dat['con_for_doc_dict'].items():
                        doc_dict[doc_key] = doc_value.encode('utf-8')
                    new_dat['con_for_doc_dict'] = doc_dict
                else:
                    new_dat[key] = value.encode('utf-8')
            new_dat_list.append(new_dat)
        return new_dat_list
'''

# 从json格式的数据文件中读入数据：
#   @json_file: 数据文件名
#   @encoding:  数据存放 utf-8 或者是 unicode
#   2017-04-07 10:30 --> add encoding = 'utf-8'
def load_json_dat(json_file,encoding = 'unicode'):
    if encoding == 'unicode':
        return json.loads(open(json_file,'r').read())['data']
    elif encoding == 'utf-8':
        data = json.loads(open(json_file,'r').read())
        old_dat_list = data['data']
        new_dat_list = []
        key_list = ['user_info','user_id','comment_id','movie_name','senti_label','movie_type','doc_dict']
        for old_dat in old_dat_list:
            #print old_dat
            new_dat = {}
            for key in key_list:
                if key == 'user_info' or key == 'user_id' or key == 'comment_id' or \
                                key == 'movie_name' or key == 'senti_label' or key == 'movie_type':
                    new_dat[key] = old_dat[key].encode('utf-8')
                elif key == 'doc_dict':
                    new_dat[key] = {}
                    new_dat[key]['raw_con'] = old_dat[key]['raw_con'].encode('utf-8')
                    new_dat[key]['seg_con'] = old_dat[key]['seg_con'].encode('utf-8')
                    new_dat[key]['pos_con'] = old_dat[key]['pos_con'].encode('utf-8')
                    new_dat[key]['sen_list'] = []
                    for i in range(0,len(old_dat[key]['sen_list'])):
                        temp_dict = {}
                        temp_dict['raw'] = old_dat[key]['sen_list'][i]['raw'].encode('utf-8')
                        temp_dict['seg'] = old_dat[key]['sen_list'][i]['seg'].encode('utf-8')
                        temp_dict['pos'] = old_dat[key]['sen_list'][i]['pos'].encode('utf-8')
                        temp_dict['dep'] = old_dat[key]['sen_list'][i]['dep'].encode('utf-8')
                        new_dat[key]['sen_list'].append(temp_dict)
            new_dat_list.append(new_dat)
        '''
        # Just for Test
        print len(new_dat_list) == len(old_dat_list)
        for i in range(0,len(new_dat_list)):
            new_dat = new_dat_list[i]
            old_dat = old_dat_list[i]
            print len(new_dat['doc_dict']['sen_list']) == len(old_dat['doc_dict']['sen_list'])
            print new_dat['doc_dict']['sen_list'][0]['raw'] == old_dat['doc_dict']['sen_list'][0]['raw'].encode('utf-8')
            break
        '''
        return new_dat_list

if __name__ == '__main__':
    out_json_file = '../../../ExpData/MovieData/JsonData/xmlDatForComments.json'
    dd = load_json(out_json_file)
    print dd['data'][0]
    temp_str = dd['data'][0]['con_for_doc_dict']['content']
