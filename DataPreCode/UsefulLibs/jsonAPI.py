#encoding=utf-8
import json



# -------------------------------------------------------------------- #
# 将无结构数据转化成XML数据
# XML数据结构类型：
#    comment_id                          评论ID，
#    user_id                             用户ID，发布评论的用户ID
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
# -------------------------------------------------------------------- #


def print_out_dat_json_visual(dat_list,json_con_visual_file):
    # 由于json里面的文件的汉字都是unicode编码的，人工阅读不变，于是顺便生成一个适合人阅读的文件
    out_con_list = []
    for each_dat in dat_list:
        temp_str = 'comment_id\t' + each_dat['comment_id']
        out_con_list.append(temp_str)
        temp_str = 'user_id\t' + each_dat['user_id']
        out_con_list.append(temp_str)
        temp_str = 'movie_name\t' + each_dat['movie_name']
        out_con_list.append(temp_str)
        temp_str = 'senti_label\t' + each_dat['senti_label']
        out_con_list.append(temp_str)
        temp_str = 'movie_type\t' + each_dat['movie_type']
        out_con_list.append(temp_str)
        temp_str = 'user_info\t' + each_dat['user_info']
        out_con_list.append(temp_str)
        out_con_list.append('con_for_doc_dict:')
        temp_str = '\tcontent\t' + each_dat['con_for_doc_dict']['content']
        out_con_list.append(temp_str)
        temp_str = '\tsegmentation\t' + each_dat['con_for_doc_dict']['segmentation']
        out_con_list.append(temp_str)
        temp_str = '\tpostag\t' + each_dat['con_for_doc_dict']['postag']
        out_con_list.append(temp_str)
        temp_str = '\tdependency\t' + each_dat['con_for_doc_dict']['dependency']
        out_con_list.append(temp_str)
        out_con_list.append('con_for_sen_list:')
        for i in range(0,len(each_dat['con_for_sen_list'])):
            temp_dict = each_dat['con_for_sen_list'][i]
            out_con_list.append('Sen ' + str(i+1) + ' :')
            temp_str = '\tcontent\t' + temp_dict['content']
            out_con_list.append(temp_str)
            temp_str = '\tsegmentation\t' + temp_dict['segmentation']
            out_con_list.append(temp_str)
            temp_str = '\tpostag\t' + temp_dict['postag']
            out_con_list.append(temp_str)
            temp_str = '\tdependency\t' + temp_dict['dependency']
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

def load_json(json_file):
    data = json.loads(open(json_file,'r').read())
    # data is encoded by unicode
    return data


def load_json_movie_dat(json_file):
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

if __name__ == '__main__':
    out_json_file = '../../../ExpData/MovieData/JsonData/xmlDatForComments.json'
    dd = load_json(out_json_file)
    print dd['data'][0]
    temp_str = dd['data'][0]['con_for_doc_dict']['content']
