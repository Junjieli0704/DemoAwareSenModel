#coding=utf-8
import time

def get_current_time():
    time_str = time.strftime('%H:%M:%S')
    hour = int(time_str.split(':')[0])
    min = int(time_str.split(':')[1])
    sec = int(time_str.split(':')[2])
    return get_time_dict(hour,min,sec)



def get_time_dict(hour = 0,min = 0, sec = 0):
    time_dict = {}
    time_dict['hour'] = hour
    time_dict['min'] = min
    time_dict['sec'] = sec
    return time_dict

def print_time_dict(time_dict):
    print get_time_dict_str(time_dict)

def get_time_dict_str(time_dict):
    hour_str = str(time_dict['hour'])
    min_str = str(time_dict['min'])
    sec_str = str(time_dict['sec'])
    if time_dict['hour'] / 10 == 0:
        hour_str = '0' + hour_str
    if time_dict['min'] / 10 == 0:
        min_str = '0' + min_str
    if time_dict['sec'] / 10 == 0:
        sec_str = '0' + sec_str
    temp_str = hour_str + ':' + min_str + ':' + sec_str
    return temp_str

def get_music_time_info(in_file):
    time_dic_list = []
    name_list = []
    for line_con in open(in_file,'r+').readlines():
        word_con_list = line_con.replace('\n','').replace('\r','').split('\t')
        name_list.append(word_con_list[1])
        time_dict = get_time_dict(0,int(word_con_list[2]),int(word_con_list[3]))
        time_dic_list.append(time_dict)
    return time_dic_list,name_list

def time_plus(time_dict1,time_dict2):
    sec = time_dict1['sec'] + time_dict2['sec']
    min = sec / 60
    sec = sec % 60
    min = min + time_dict1['min'] + time_dict2['min']
    hour = min / 60 + time_dict2['hour'] + time_dict1['hour']
    min = min % 60
    time_dict_res = get_time_dict(hour,min,sec)
    return time_dict_res

def get_time_list(init_time_dict,time_dic_list):
    out_time_dict_list = []
    out_time_dict_list.append(init_time_dict)
    for time_dict in time_dic_list:
        init_time_dict = out_time_dict_list[len(out_time_dict_list) - 1]
        out_time_dict_list.append(time_plus(init_time_dict,time_dict))

    for time_dict in out_time_dict_list:
        print_time_dict(time_dict)
    return out_time_dict_list


def print_out_time_info(out_time_dict_list,time_dic_list,name_list,out_file):
    out_line_con_list = []
    for i in range(0,len(out_time_dict_list) - 1):
        line_con_list = []
        line_con_list.append(str(i+1))
        line_con_list.append(name_list[i])
        line_con_list.append(get_time_dict_str(out_time_dict_list[i]))
        line_con_list.append(get_time_dict_str(time_dic_list[i]))
        line_con_list.append(get_time_dict_str(out_time_dict_list[i+1]))
        out_line_con_list.append('\t'.join(line_con_list))
    open(out_file,'w+').write('\n'.join(out_line_con_list))


if __name__ == '__main__':
    time_dic_list,name_list = get_music_time_info('ttt.txt')
    out_time_dict_list = get_time_list(get_current_time(),time_dic_list)
    print_out_time_info(out_time_dict_list,time_dic_list,name_list,'ccc.txt')




