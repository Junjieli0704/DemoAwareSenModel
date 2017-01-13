import json


def print_out_all_dat_list(dat_list,json_file):
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

if __name__ == '__main__':
    '''
    temp_dict = {}
    temp_dict['eee'] = {}
    temp_dict['eee']['ff'] = 1
    temp_dict['eee']['eg'] = 2
    temp_dict['kk'] = 5
    print_out_json(temp_dict,'te.json')
    load_json('te.json')
    '''

    out_xml_file = '../../../ExpData/XMLData/xmlDatForComments.json'
    dd = load_json(out_xml_file)
    print dd['data'][0]
    temp_str = dd['data'][0]['con_for_doc_dict']['content']
    #temp_str = temp_str.encode('utf-8')
    #print temp_str
    #temp_str = temp_str.encode('gbk')
    #print temp_str
    temp_str = temp_str.decode('utf-8')
    print temp_str