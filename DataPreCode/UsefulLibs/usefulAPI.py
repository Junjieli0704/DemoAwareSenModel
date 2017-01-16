#coding=utf-8
import os
import time
import shutil
import datetime
# A list of useful API

# Make a dir
def mk_dir(path):
    path = path.strip()
    path = path.rstrip("\\")
    is_exist = os.path.exists(path)
    if not is_exist:
        temp_str = path + ' create successfully!'
        print temp_str
        os.makedirs(path)
        return True
    else:
        #temp_str = path + ' is already be there!'
        #print temp_str
        return False

def is_file_exist(file_name):
    return os.path.exists(file_name);

def get_file_size(file_name):
    if is_file_exist(file_name):
        return os.path.getsize(file_name);
    else:
        print 'File is not exist!'
        return -1;

# Get all file name in the directory
# input:
#    dir: the directory
#    is_contain_dir: determine whether the fileName has the directory (False is default value);
# output: fileNameList
def get_dir_files(dir,is_contain_dir = False):
    file_list = []
    if os.path.exists(dir):
        dir_file_list = os.listdir(dir);
        for dir_file in dir_file_list:
            if is_contain_dir:    file_list.append(dir + dir_file);
            else:     file_list.append(dir_file);
    return file_list;

def get_current_date_time():
    return time.strftime('%Y-%m-%d_%H_%M_%S')

def get_current_date_time2():
    return time.strftime('%Y_%m_%d_%H_%M_%S')

def get_current_date():
    return time.strftime('%Y-%m-%d')

# Calculate dateStr = Now - diff_date_num
def get_date_diffnum_from_now(diff_date_num):
    curr_date = datetime.datetime.now();
    delta_date = datetime.timedelta(days = diff_date_num);
    return (curr_date - delta_date).strftime("%Y-%m-%d");


def file_copy(src_file,dst_file):
    shutil.copyfile(src_file, dst_file)

# Calculate the difference between two dates (LeftDateStr - rightDateStr)
# LeftDateStr = '2015-05-18 22:22:22'
# RightDateStr = '2015-05-08 22:13:15'
# ans = 10 days
# if ans is 'NULL': it means a error in the function
def get_diff_date(left_date_str,right_date_str):
    try:
        left_year = int(left_date_str.split('-')[0])
        left_mon = int(left_date_str.split('-')[1])
        left_day = int(left_date_str.split('-')[2].split(' ')[0]);
        right_year = int(right_date_str.split('-')[0])
        right_mon = int(right_date_str.split('-')[1])
        right_day = int(right_date_str.split('-')[2].split(' ')[0]);
        left_date = datetime.datetime(left_year, left_mon, left_day)
        right_date = datetime.datetime(right_year, right_mon, right_day)
        diff_date_num =  (left_date - right_date).days
        return diff_date_num;
    except Exception,e:
        temp_str = 'An error is found in compute usefulAPI.getDiffDate()';
        print temp_str
        temp_str = 'para: LeftDateStr: ' + left_date_str
        print temp_str
        temp_str = 'para: RightDateStr: ' + right_date_str
        print temp_str
        print temp_str
        return 'NULL'

def is_chinese(uchar):
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False

def detect_chinese_uchar(in_uchar):
    is_chinese_uchar = True
    for uchar in in_uchar:
        if is_chinese(uchar): continue
        else:
            is_chinese_uchar = False
            break
    return is_chinese_uchar



if __name__ == '__main__':
    pass