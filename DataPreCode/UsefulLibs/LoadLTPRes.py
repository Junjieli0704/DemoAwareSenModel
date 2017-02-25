#encoding=utf-8


# -------------------------------------------------------------------- #
# 读入LTP处理好的文件
# Time: 2017-02-20
# -------------------------------------------------------------------- #

import xml.etree.cElementTree as ET
import json

def get_sentence_dict():
    sen_dict = {}
    sen_dict['content'] = ''
    sen_dict['segmentation'] = ''
    sen_dict['postag'] = ''
    sen_dict['dep_parent'] = ''
    sen_dict['dep_rel'] = ''
    return sen_dict


# -------------------------------------------------------------------- #
# 为了让LTP输出的xml文件可以被解析，需要做如下几件事
# 1. 删除<xml4nlp>行，并记录第一个出现<xml4nlp>的位置A
# 2. 删除</xml4nlp>行，并记录最后一次出现</xml4nlp>的位置B，基本是最后一行
# 3. 在位置A中添加<xml4nlp>和位置B中添加</xml4nlp>
# 4. 删除含有 <?xml version 和 <note sent= 的行
# Time: 2017-02-20
# -------------------------------------------------------------------- #

def change_ltp_file(in_file,out_file):
    out_line_con_list = []
    xml4nlp_num = 0
    line_con_list = open(in_file,'r').readlines()
    for line_con in line_con_list:
        line_con = line_con.strip()
        if line_con.find('<xml4nlp>') != -1:
            xml4nlp_num = xml4nlp_num + 1
            if xml4nlp_num > 1:
                continue
        if line_con.find('</xml4nlp>') != -1:
            continue
        if line_con.find('<?xml version') != -1:
            continue
        if line_con.find('<note sent=') != -1:
            continue
        out_line_con_list.append(line_con)
    out_line_con_list.append('</xml4nlp>')
    open(out_file,'w+').write('\n'.join(out_line_con_list))

def load_ltp_res_file(file_name):
    change_ltp_file(file_name,file_name)
    tree = ET.parse(file_name)
    print 'After Parse XML Files......'
    root = tree.getroot()
    doc_node_list = root.findall("doc")
    all_review_list = []
    for doc_node in doc_node_list:
        review_doc_dict = {}
        review_doc_dict['doc_list'] = []
        para_node_list = doc_node.findall('para')
        if len(para_node_list) == 0: continue
        for para_node in para_node_list:
            for sen_node in para_node.findall("sent"):
                sen_dict = get_sentence_dict()
                sen_dict['content'] = sen_node.get('cont')
                seg_list = []
                pos_tag_list = []
                para_list = []
                rel_list = []
                for word_node in sen_node.findall('word'):
                    seg_list.append(word_node.get('cont'))
                    pos_tag_list.append(word_node.get('pos'))
                    para_list.append(word_node.get('parent'))
                    rel_list.append(word_node.get('relate'))
                sen_dict['postag'] = ' '.join(pos_tag_list)
                sen_dict['segmentation'] = ' '.join(seg_list)
                sen_dict['dep_parent'] = ' '.join(para_list)
                sen_dict['dep_rel'] = ' '.join(rel_list)
                review_doc_dict['doc_list'].append(sen_dict)
        all_review_list.append(review_doc_dict)
    return all_review_list

def print_all_review_list(all_review_list,json_file):
    temp_dict = {}
    temp_dict['data'] = all_review_list
    json_str = json.dumps(temp_dict)
    open(json_file,'w+').write(json_str)

def print_out_all_word_seg(all_review_list,out_file):
    out_line_con_list = []
    for review in all_review_list:
        doc_list = []
        for sen in review['doc_list']:
            for word in sen['segmentation'].split(' '):
                doc_list.append(word)
        out_line_con_list.append(' '.join(doc_list).encode('utf-8'))
    open(out_file,'w+').write('\n'.join(out_line_con_list))

def print_out_all_word_segpos(all_review_list,out_file):
    out_line_con_list = []
    for review in all_review_list:
        doc_list = []
        for sen in review['doc_list']:
            for i in range(0,len(sen['segmentation'].split(' '))):
                word = sen['segmentation'].split(' ')[i]
                pos = sen['postag'].split(' ')[i]
                doc_list.append(word + '/' + pos)
        out_line_con_list.append(' '.join(doc_list).encode('utf-8'))
    open(out_file,'w+').write('\n'.join(out_line_con_list))


if __name__=="__main__":
    '''
    in_raw_dat_filefold = '../../../ExpData/MovieData/RawData/HIT_LTP_Res/'
    ltp_res_file = in_raw_dat_filefold + 'RawSenDataForComments_LTP_Res.txt'
    all_review_list = load_ltp_res_file(ltp_res_file)
    #print_all_review_list(all_review_list,'aa.json')
    #print_out_all_word_seg(all_review_list,'RawSenDataForComments_LTP_SEG_Res.txt')
    print_out_all_word_segpos(all_review_list,'RawSenDataForComments_LTP_SEGPOS_Res.txt')
    '''
    a = [5,3,4,5,6]
    print list(set(a))

    tree = ET.parse()
    print 'After Parse XML Files......'
    root = tree.getroot()
    doc_node_list = root.findall("doc")
    all_review_list = []