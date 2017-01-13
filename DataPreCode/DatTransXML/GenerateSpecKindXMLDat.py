#encoding=utf-8


from UsefulLibs import xmlAPI

'''
    Fun: Generate movie data for a specific category (Love, Comedy and so on).
    Time: 2016-12-09
'''

class GenerateSpecKindXMLDat:
    def __init__(self,in_xml_dat_file,out_xml_dat_file,spec_kind = 'Love'):
        self.in_xml_dat_file = in_xml_dat_file
        self.out_xml_dat_file = out_xml_dat_file
        self.spec_kind = spec_kind
        self.in_dat_list = []
        self.out_dat_list = []

    def load_xml_file(self):
        print 'before load_xml_file ......'
        self.in_dat_list = xmlAPI.load_xml_data(self.in_xml_dat_file)
        print 'after load_xml_file ......'

    def generate_out_dat_file(self):
        for temp_dat in self.in_dat_list:
            if temp_dat.movieType.find(self.spec_kind) != -1:
                self.out_dat_list.append(temp_dat)
        print 'len of ' + self.spec_kind + ' = ' + str(len(self.out_dat_list))
        xmlAPI.print_out_all_dat_list(self.out_dat_list,self.out_xml_dat_file)

    def print_different_kind_movie_numbers(self):
        #movie_kind_to_movie_name_list_dict = {}
        movie_kind_to_comment_number_dict = {}
        for temp_dat in self.in_dat_list:
            temp_kind_list = temp_dat.movieType.split('/')
            temp_kind_list = list(set(temp_kind_list))
            for temp_kind in temp_kind_list:
                if movie_kind_to_comment_number_dict.has_key(temp_kind):
                    movie_kind_to_comment_number_dict[temp_kind] = movie_kind_to_comment_number_dict[temp_kind] + 1
                else:
                    movie_kind_to_comment_number_dict[temp_kind] = 1
        for key,value in movie_kind_to_comment_number_dict.items():
            print key + '\t' + str(value)




if __name__ == '__main__':

    in_xml_dat_file = './OutData/all_dat.xml'
    out_xml_dat_file = './OutData/all_dat_Comedy.xml'
    generateSpecKindXMLDat = GenerateSpecKindXMLDat(in_xml_dat_file,out_xml_dat_file,spec_kind='Comedy')
    generateSpecKindXMLDat.load_xml_file()
    generateSpecKindXMLDat.generate_out_dat_file()
    generateSpecKindXMLDat.print_different_kind_movie_numbers()
