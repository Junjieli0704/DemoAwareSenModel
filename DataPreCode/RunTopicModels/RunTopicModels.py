#encoding=utf-8

# -------------------------------------------------------------------- #
# 使用主题模型的运行文件来运行模型
# 运行的模型有以下几类：
#  ***  LDA：    简单的词袋模型，文档表示成一堆词汇
#  ***  JST：    简单的词袋模型，文档表示成一堆词汇 + 情感词典作为情感信息的因素
#       ASUM：   每个句子单独有一个主题，句子内容是词袋模型 + 情感词典作为情感信息的因素
#       USTM_W： 简单的词袋模型，文档表示成一堆词汇 + 情感词典作为情感信息的因素 + 用户信息
#       USTM_S： 每个句子单独有一个主题，句子内容是词袋模型 + 情感词典作为情感信息的因素 + 用户信息
#       D_PLDA： 篇章表示成评价对象pair的组合 + 情感词典作为情感信息的因素
#       DSTM：   篇章表示成评价对象pair的组合 + 情感词典作为情感信息的因素 + 用户信息
# Release Time: 2017-03-15 08:59
# -------------------------------------------------------------------- #

import os
import sys


def get_out_dir(data_file,num_topics,model_name):
    out_dir = os.path.dirname(data_file) + '/'
    out_dir = out_dir + model_name + '_nt_' + num_topics + '/'
    return out_dir



def run_lda(model_status = 'est',
            save_model_name = 'model',
            out_dir = '',
            data_file = 'test.txt',
            log_file = 'log.txt',
            alpha_value = '0.05',
            beta_value = '0.05',
            num_topics = '30',
            num_iters = '100',
            word_map_file = 'wordmap.txt',
            top_words_num = '20'):

    cmd_path_list = []

    exe_path = os.path.dirname(os.path.dirname(os.getcwd())) + '\TopicBasedModels\LDA\\bin\Release\LDA.exe'
    cmd_path_list.append(exe_path)

    if out_dir == '':
        out_dir = get_out_dir(data_file,num_topics,'LDA')

    cmd_path_list.append('-ms')
    cmd_path_list.append(model_status)
    cmd_path_list.append('-dir')
    cmd_path_list.append(out_dir)
    cmd_path_list.append('-mn')
    cmd_path_list.append(save_model_name)
    cmd_path_list.append('-df')
    cmd_path_list.append(data_file)
    cmd_path_list.append('-lf')
    cmd_path_list.append(log_file)
    cmd_path_list.append('-alpha')
    cmd_path_list.append(alpha_value)
    cmd_path_list.append('-beta')
    cmd_path_list.append(beta_value)
    cmd_path_list.append('-nt')
    cmd_path_list.append(num_topics)
    cmd_path_list.append('-ni')
    cmd_path_list.append(num_iters)
    cmd_path_list.append('-wmf')
    cmd_path_list.append(word_map_file)
    cmd_path_list.append('-tw')
    cmd_path_list.append(top_words_num)
    cmd_path = ' '.join(cmd_path_list)
    print cmd_path
    os.system(cmd_path)

def run_jst(model_status = 'est',
            save_model_name = 'model',
            data_file = 'test.txt',
            senti_word_file = 'senti.txt',
            out_dir = '',
            log_file = 'log.txt',
            alpha_value = '0.05',
            beta_value = '0.05',
            gamma_value = '0.05',
            num_topics = '30',
            num_iters = '100',
            word_map_file = 'wordmap.txt',
            top_words_num = '20'):

    cmd_path_list = []

    exe_path = os.path.dirname(os.path.dirname(os.getcwd())) + '\TopicBasedModels\JST\\bin\Release\JST.exe'
    cmd_path_list.append(exe_path)

    if out_dir == '':
        out_dir = get_out_dir(data_file,num_topics,'JST')

    cmd_path_list.append('-ms')
    cmd_path_list.append(model_status)
    cmd_path_list.append('-dir')
    cmd_path_list.append(out_dir)
    cmd_path_list.append('-mn')
    cmd_path_list.append(save_model_name)
    cmd_path_list.append('-df')
    cmd_path_list.append(data_file)
    cmd_path_list.append('-slf')
    cmd_path_list.append(senti_word_file)
    cmd_path_list.append('-lf')
    cmd_path_list.append(log_file)
    cmd_path_list.append('-alpha')
    cmd_path_list.append(alpha_value)
    cmd_path_list.append('-beta')
    cmd_path_list.append(beta_value)
    cmd_path_list.append('-gamma')
    cmd_path_list.append(gamma_value)
    cmd_path_list.append('-nt')
    cmd_path_list.append(num_topics)
    cmd_path_list.append('-ni')
    cmd_path_list.append(num_iters)
    cmd_path_list.append('-wmf')
    cmd_path_list.append(word_map_file)
    cmd_path_list.append('-tws')
    cmd_path_list.append(top_words_num)
    cmd_path = ' '.join(cmd_path_list)
    print cmd_path
    os.system(cmd_path)

def run_ustm_w(model_status = 'est',
            save_model_name = 'model',
            data_file = 'test.txt',
            demo_file = 'test_demo.txt',
            senti_word_file = 'senti.txt',
            out_dir = '',
            log_file = 'log.txt',
            alpha_value = '0.05',
            beta_value = '0.05',
            gamma_value = '0.05',
            eta_value = '0.05',
            num_sentis = '3',
            num_topics = '30',
            num_iters = '100',
            word_map_file = 'word_map.txt',
            demo_map_file = 'demo_map.txt',
            top_words_num = '20'):

    cmd_path_list = []

    exe_path = os.path.dirname(os.path.dirname(os.getcwd())) + '\TopicBasedModels\USTMW\\bin\Release\USTMW.exe'
    cmd_path_list.append(exe_path)

    if out_dir == '':
        out_dir = get_out_dir(data_file,num_topics,'USTMW')

    cmd_path_list.append('-ms')
    cmd_path_list.append(model_status)
    cmd_path_list.append('-mn')
    cmd_path_list.append(save_model_name)
    cmd_path_list.append('-dir')
    cmd_path_list.append(out_dir)
    cmd_path_list.append('-df')
    cmd_path_list.append(data_file)
    cmd_path_list.append('-ddf')
    cmd_path_list.append(demo_file)
    cmd_path_list.append('-slf')
    cmd_path_list.append(senti_word_file)
    cmd_path_list.append('-lf')
    cmd_path_list.append(log_file)

    cmd_path_list.append('-alpha')
    cmd_path_list.append(alpha_value)
    cmd_path_list.append('-beta')
    cmd_path_list.append(beta_value)
    cmd_path_list.append('-gamma')
    cmd_path_list.append(gamma_value)
    cmd_path_list.append('-eta')
    cmd_path_list.append(eta_value)

    cmd_path_list.append('-nt')
    cmd_path_list.append(num_topics)
    cmd_path_list.append('-ni')
    cmd_path_list.append(num_iters)
    cmd_path_list.append('-ns')
    cmd_path_list.append(num_sentis)

    cmd_path_list.append('-wmf')
    cmd_path_list.append(word_map_file)
    cmd_path_list.append('-dmf')
    cmd_path_list.append(demo_map_file)
    cmd_path_list.append('-tws')
    cmd_path_list.append(top_words_num)
    cmd_path = ' '.join(cmd_path_list)
    print cmd_path
    os.system(cmd_path)


if __name__ == '__main__':

    data_file = '../../../ExpData/MovieData/LDAData/LDA_Style_Dat/Comedy_Doc_5_0.3_True/Comedy_Doc_5_0.3_True.txt'
    demo_file = '../../../ExpData/MovieData/LDAData/LDA_Style_Dat/Comedy_Doc_5_0.3_True/Comedy_demo.txt'
    senti_word_file = '../../../ExpData/SentiWordDat/ReviseSentiWord/revise_sentiment_word_list_LDA.txt'

    run_ustm_w(demo_file=demo_file,data_file=data_file,senti_word_file=senti_word_file,model_status='est',num_topics='30',num_iters='5')
    #run_lda(data_file=data_file,model_status='est',num_topics='30',num_iters='100')
    #run_jst(data_file=data_file,senti_word_file=senti_word_file,model_status='est',num_topics='30',num_iters='100')

