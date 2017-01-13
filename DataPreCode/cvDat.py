#encoding=utf-8
#对数据进行交叉验证的划分
import random

from UsefulLibs import usefulAPI


class CvDat:
    def __init__(self,movie_content_file,movie_demo_file,out_file_fold):
        self.movie_content_file = movie_content_file
        self.movie_demo_file = movie_demo_file
        self.out_file_fold = out_file_fold
        self.comment_id_list = []
        self.comment_id_to_content = {}
        self.comment_id_to_demo = {}

    def load_content_data(self):
        line_con_list = open(self.movie_content_file,'r').readlines()
        for line_con in line_con_list:
            line_con = line_con.replace('\r','').replace('\n','')
            word_con_list = line_con.split(' ')
            comment_id = word_con_list[0]
            movie_content = ' '.join(word_con_list).replace(comment_id + ' ','')
            self.comment_id_list.append(comment_id)
            self.comment_id_to_content[comment_id] = movie_content

        line_con_list = open(self.movie_demo_file,'r').readlines()
        for line_con in line_con_list:
            line_con = line_con.replace('\r','').replace('\n','')
            word_con_list = line_con.split(' ')
            temp_comment_id = word_con_list[0]
            comment_id = temp_comment_id.replace('_demo','')
            movie_demo_content = ' '.join(word_con_list).replace(temp_comment_id + ' ','')
            self.comment_id_to_demo[comment_id] = movie_demo_content


    def split_cross_vali_dat(self,split_num,out_file):
        #pos_list, neg_list = self.get_pos_neg_list(all_dat_list)
        comment_id_list = self.comment_id_list
        random.shuffle(comment_id_list)
        random.shuffle(comment_id_list)
        train_list = []
        test_list = []
        end_value_list = []
        for i in range(0,split_num):
            end_value_list.append((len(comment_id_list) / split_num) * (i+1))

        diff_num = len(comment_id_list) - (len(comment_id_list) / split_num) * split_num
        if diff_num != 0:
            for i in range(0,split_num):
                if i < diff_num:
                    end_value_list[i] = end_value_list[i] + i + 1
                else:
                    end_value_list[i] = end_value_list[i] + diff_num

        # Get Each CommentID to cv_TestNum
        comment_id_to_num_dict = {}
        test_num = 0
        for i in range(0,len(comment_id_list)):
            if i >= end_value_list[test_num]:
                test_num = test_num + 1
            comment_id_to_num_dict[comment_id_list[i]] = test_num

        # Initial trainList testList
        for i in range(0,split_num):
            train_list.append([])
            test_list.append([])

        for j in range(0,len(comment_id_list)):
            comment_id = comment_id_list[j]
            test_num = comment_id_to_num_dict[comment_id]
            for i in range(0,split_num):
                if i == test_num:
                    test_list[i].append(comment_id)
                else:
                    train_list[i].append(comment_id)

        usefulAPI.mkDir(self.out_file_fold)

        self.print_train_test_list_to_file(self.out_file_fold + out_file,train_list,test_list)

    def print_train_test_list_to_file(self,out_file,train_list,test_list):
        fw = open(out_file,'w+')
        for i in range(0,len(train_list)):
            temp_str = 'cv_' + str(len(train_list)) + '_' + str(i+1) + '_train_' + str(len(train_list[i])) + ' '
            fw.write(temp_str)
            fw.write(' '.join(train_list[i]))
            fw.write('\n')
            temp_str = 'cv_' + str(len(train_list)) + '_' + str(i+1) + '_test_' + str(len(test_list[i])) + ' '
            fw.write(temp_str)
            fw.write(' '.join(test_list[i]))
            fw.write('\n')
        fw.close()

    def load_cross_vali_dat(self,movie_type):
        in_file = self.out_file_fold + 'cvID_' + movie_type + '.txt'
        train_list = []
        test_list = []
        train_id_list = []
        test_id_list = []
        line_con_list = open(in_file,'r').readlines()
        for line_con in line_con_list:
            line_con = line_con.replace('\r','').replace('\n','')
            word_con_list = line_con.split(' ')
            if len(word_con_list) < 1: continue
            if word_con_list[0].find('train') != -1:
                for i in range(1,len(word_con_list)):
                    train_id_list.append(word_con_list[i])
            elif word_con_list[0].find('test') != -1:
                for i in range(1,len(word_con_list)):
                    test_id_list.append(word_con_list[i])
                train_list.append(train_id_list)
                test_list.append(test_id_list)
                train_id_list = []
                test_id_list = []
        return train_list,test_list

    def print_out_cv_data(self,movie_type,out_cv_file_fold):
        self.load_content_data()
        train_list,test_list = self.load_cross_vali_dat(movie_type)
        usefulAPI.mkDir(out_cv_file_fold)
        for i in range(0,len(train_list)):
            movie_content_file = self.movie_content_file.split('/')[-1]
            movie_demo_file = self.movie_demo_file.split('/')[-1]
            train_id_list = train_list[i]
            test_id_list = test_list[i]
            out_con_list = []
            for train_id in train_id_list:
                out_con_list.append(train_id + ' ' + self.comment_id_to_content[train_id])
            out_file = movie_content_file.replace('.txt','') + '_train_' + str(len(train_list)) + '_' + str(i+1) + '.txt'
            out_file = out_cv_file_fold + out_file
            open(out_file,'w+').write('\n'.join(out_con_list))

            out_con_list = []
            for train_id in train_id_list:
                out_con_list.append(train_id + '_demo ' + self.comment_id_to_demo[train_id])
            out_file = movie_demo_file.replace('.txt','') + '_train_' + str(len(train_list)) + '_' + str(i+1) + '.txt'
            out_file = out_cv_file_fold + out_file
            open(out_file,'w+').write('\n'.join(out_con_list))

            out_con_list = []
            for test_id in test_id_list:
                out_con_list.append(test_id + ' ' + self.comment_id_to_content[test_id])
            out_file = movie_content_file.replace('.txt','') + '_test_' + str(len(train_list)) + '_' + str(i+1) + '.txt'
            out_file = out_cv_file_fold + out_file
            open(out_file,'w+').write('\n'.join(out_con_list))

            out_con_list = []
            for test_id in test_id_list:
                out_con_list.append(test_id + '_demo ' + self.comment_id_to_demo[test_id])
            out_file = movie_demo_file.replace('.txt','') + '_test_' + str(len(train_list)) + '_' + str(i+1) + '.txt'
            out_file = out_cv_file_fold + out_file
            open(out_file,'w+').write('\n'.join(out_con_list))

def get_movie_con_file(movie_type):
    movie_con_file = './DocData/Doc_' + movie_type + '_DataForLDAAspectMining.txt'
    movie_demo_file = './DocData/Demo_Doc_' + movie_type + '_DataForLDAAspectMining.txt'
    return movie_con_file,movie_demo_file


def cv_doc_data(movie_type_list):
    for movie_type in movie_type_list:
        movie_content_file,movie_demo_file = get_movie_con_file(movie_type)
        out_file_fold = './DocData/CvDat/'
        cvDat = CvDat(movie_content_file,movie_demo_file,out_file_fold)
        cvDat.load_content_data()
        out_file = 'cvID_' + movie_type + '.txt'
        cvDat.split_cross_vali_dat(split_num=10,out_file=out_file)

def cv_doc_data_to_file(movie_type_list):
    for movie_type in movie_type_list:
        movie_content_file,movie_demo_file = get_movie_con_file(movie_type)
        out_file_fold = './DocData/CvDat/'
        cvDat = CvDat(movie_content_file,movie_demo_file,out_file_fold)
        out_cv_file_fold = './DocData/' + movie_type + '/'
        cvDat.print_out_cv_data(movie_type,out_cv_file_fold)

if __name__ == '__main__':
    movie_type_list = ['Action','Adventure','Comedy','Love','Suspense']
    #movie_type_list = ['Action']
    cv_doc_data(movie_type_list)
    cv_doc_data_to_file(movie_type_list)