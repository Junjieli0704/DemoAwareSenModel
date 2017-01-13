#encoding=utf-8


import xmlAPI
import sys
import os

reload(sys)
sys.setdefaultencoding('utf8')

class GenerateLDADat:
    def __init__(self,in_movie_dat_xml_file):
        self.in_movie_dat_xml_file = in_movie_dat_xml_file
        self.all_dat_list = []
        self.aspect_list = []
        self.delete_word_dict = {}
        self.senti_word_dict = {}

    def load_xml_file(self):
        print 'before load_xml_file ......'
        self.all_dat_list = xmlAPI.load_xml_data(self.in_movie_dat_xml_file)
        print 'after load_xml_file ......'

    def load_senti_file(self,senti_file):
        if os.path.exists(senti_file):
            in_line_con_list = open(senti_file,'r').readlines()
            for line_con in in_line_con_list:
                line_con = line_con.replace('\n','').replace('\r','')
                word_list = line_con.split('\t')
                if len(word_list) == 2:
                    word = word_list[0]
                    score = int(word_list[1])
                    self.senti_word_dict[word] = score

    def generate_delete_word_dict(self,common_value = 0.3,rare_value = 2,is_need_pruncation = True):
        word_to_times_dict = {}
        for temp_dat in self.all_dat_list:
            word_list = temp_dat.conForDoc['segmentation'].split(' ')
            pos_list = temp_dat.conForDoc['postag'].split(' ')
            for i in range(0,len(word_list)):
                word = word_list[i]
                if is_need_pruncation and pos_list[i] == 'PU':
                    self.delete_word_dict[word] = 1
                    continue
                if word_to_times_dict.has_key(word) == False:
                    word_to_times_dict[word] = 1
                else:
                    word_to_times_dict[word] = word_to_times_dict[word] + 1

        for word, times in word_to_times_dict.items():
            if self.senti_word_dict.has_key(word): continue
            elif times < rare_value:
                self.delete_word_dict[word] = 1
            elif times > len(self.all_dat_list) * common_value:
                self.delete_word_dict[word] = 1


    def generate_out_dat_lda_file(self,
                              mode = 'Doc',
                              sentiment_word_file = '',
                              common_value = 1.0,
                              rare_value = 5,
                              is_need_pruncation = False,
                              is_need_processing = True,
                              out_dat_file = 'dat.txt'):

        self.load_senti_file(sentiment_word_file)
        self.delete_word_dict = {}
        self.generate_delete_word_dict(common_value,rare_value,is_need_pruncation)
        if is_need_processing == False:
            self.delete_word_dict = {}
        if mode == 'Doc':
            out_line_con_list = []
            for temp_dat in self.all_dat_list:
                temp_str = temp_dat.commentID + ' '
                temp_word_list = []
                for word in temp_dat.conForDoc['segmentation'].split(' '):
                    if self.delete_word_dict.has_key(word): continue
                    else: temp_word_list.append(word)
                temp_str = temp_str + ' '.join(temp_word_list)
                out_line_con_list.append(temp_str)
            open(out_dat_file,'w+').write('\n'.join(out_line_con_list))

        elif mode == 'Sen':
            out_line_con_list = []
            for temp_dat in self.all_dat_list:
                commment_id = temp_dat.commentID
                for i in range(0,len(temp_dat.outConForSenList)):
                    temp_word_list = []
                    temp_word_list.append(commment_id + '_s' + str(i+1))
                    for word in temp_dat.outConForSenList[i]['segmentation'].split(' '):
                        if self.delete_word_dict.has_key(word): continue
                        else: temp_word_list.append(word)
                    out_line_con_list.append(' '.join(temp_word_list))
            open(out_dat_file,'w+').write('\n'.join(out_line_con_list))


    def generate_out_demo_lda_file(self,out_demo_file = 'dat.txt'):
        out_dem_line_con_list = []
        for temp_dat in self.all_dat_list:
            temp_str = temp_dat.commentID + 'demo '
            temp_word_list = []
            for temp_info in temp_dat.userInfo.split('_'):
                if len(temp_info.split('/')) == 2:
                   attribute = temp_info.split('/')[0]
                   value = temp_info.split('/')[1]
                   if attribute == 'Sex' or attribute == 'Loc' or attribute == 'Age':
                       if value != 'NULL':
                           temp_word_list.append(temp_info)
            temp_str = temp_str + ' '.join(temp_word_list)
            out_dem_line_con_list.append(temp_str)
        open(out_demo_file,'w+').write('\n'.join(out_dem_line_con_list))


if __name__ == '__main__':

    in_movie_dat_xml_file = './OutData/all_dat_Comedy.xml'
    out_lda_dat_file = 'test_doc.txt'
    out_lda_demo_file = 'test_demo.txt'

    generLDADat = GenerateLDADat(in_movie_dat_xml_file)
    generLDADat.load_xml_file()
    '''
    for mode in ['Doc','Sen']:
        for common_value in [0.2,0.25,0.3,0.35,0.4,0.45,0.5]:
            for is_need_prun in [True,False]:
                for rare_value in [1,2,3,4,5,10]:
                    out_lda_dat_file = './TempDat/Comedy_' + mode + '_Rare_' + str(rare_value) + '_Prun_' + str(is_need_prun) + '_ComValue_' + str(common_value) + '.txt'
                    generLDADat.generate_out_dat_lda_file(mode=mode,
                                                      out_dat_file=out_lda_dat_file,
                                                      rare_value=rare_value,
                                                      is_need_pruncation = is_need_prun,
                                                      common_value = common_value,
                                                      is_need_processing=False)
    '''
    generLDADat.generate_out_dat_lda_file(mode='Doc',
                                          rare_value=5,
                                          is_need_pruncation = False,
                                          common_value = 1.0,
                                          is_need_processing= False)

    generLDADat.generate_out_demo_lda_file(out_demo_file=out_lda_demo_file)
    


    #generLDADat.generate_out_dat_lda_file(mode='Doc',out_dat_file=out_lda_dat_file)
    #generLDADat.generate_out_demo_lda_file(out_demo_file=out_lda_demo_file)
    #generLDADat.generate_out_dat_lda_file(mode='Sen',out_dat_file=out_lda_dat_file)
    #generLDADat.generate_out_demo_lda_file(out_demo_file=out_lda_demo_file)


