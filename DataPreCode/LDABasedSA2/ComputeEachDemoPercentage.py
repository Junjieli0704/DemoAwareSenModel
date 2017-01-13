#encoding=utf-8

def add_dict_value(dict,key,value = 1):
    if dict.has_key(key):
        dict[key] = dict[key] + value
    else:
        dict[key] = value


def load_comment_file(movie_comment_file):
    user_demo_dict_to_num = {}
    line_con_list = open(movie_comment_file,'r').readlines()
    for line_con in line_con_list:
        line_con = line_con.replace('\n','').replace('\r','')
        word_con_list = line_con.split('\t')
        if len(word_con_list) != 6: continue
        if word_con_list[0] == 'UserInfo': continue
        user_info_str = word_con_list[3]
        for temp_str in user_info_str.split('_'):
            if temp_str.split('/')[0] == 'Label': continue
            add_dict_value(user_demo_dict_to_num,temp_str)
    return user_demo_dict_to_num

def get_percentage(user_demo_dict_to_num,str = 'Loc'):
    age_demo_to_num_dict = {}
    age_demo_to_per_dict = {}
    all_number = 0
    for user_demo,number in user_demo_dict_to_num.items():
        if user_demo.find(str) == -1: continue
        age_demo_to_num_dict[user_demo] = number
        all_number = all_number + number

    for age_demo,num in age_demo_to_num_dict.items():
        age_demo_to_per_dict[age_demo] = float(num) / float(all_number)
    return age_demo_to_num_dict,age_demo_to_per_dict

def get_each_demo_percentage(movie_comment_file,out_file):
    out_line_list = []
    user_demo_dict_to_num = load_comment_file(movie_comment_file)
    str_list = ['Age','Loc','Sex','Edu']
    for temp_str in str_list:
        demo_to_num_dict,demo_to_per_dict = get_percentage(user_demo_dict_to_num,temp_str)
        for demo, num in demo_to_num_dict.items():
            per = demo_to_per_dict[demo]
            temp_str = demo + '\t' + str(num) + '\t' + str(per)
            out_line_list.append(temp_str)
    open(out_file,'w+').write('\n'.join(out_line_list))

if __name__ == '__main__':
    movie_comment_file = './Data/DataForDemoGroupSensitiveAspectMining.txt'
    get_each_demo_percentage(movie_comment_file,'./OutData/EachDemoPercentage.txt')
