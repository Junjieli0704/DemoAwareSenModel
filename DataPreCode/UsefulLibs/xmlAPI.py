from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import dump
import xml.dom.minidom as minidom

from DatTransXML import ChangeDatToXML


def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for e in elem:
            indent(e, level+1)
        if not e.tail or not e.tail.strip():
            e.tail = i
    if level and (not elem.tail or not elem.tail.strip()):
        elem.tail = i
    return elem

def print_out_all_dat_list(all_dat_list,out_file = 'temp.xml'):
    ele_tree = ElementTree()
    root_paper_tree = Element('REVIEWS')
    ele_tree._setroot(root_paper_tree)
    for dat_info in all_dat_list:
        temp_review_ele = Element('REVIEW')
        SubElement(temp_review_ele,'CommentID').text = dat_info.commentID
        #SubElement(temp_review_ele,'UserID').text = dat_info.userID
        SubElement(temp_review_ele,'MovieName').text = dat_info.movieName
        SubElement(temp_review_ele,'UserInfo').text = dat_info.userInfo
        SubElement(temp_review_ele,'SentiLabel').text = dat_info.sentiLabel
        SubElement(temp_review_ele,'MovieType').text = dat_info.movieType
        temp_doc_ele = Element('CommentContentDoc')
        SubElement(temp_doc_ele,'Content').text = dat_info.conForDoc['content']
        SubElement(temp_doc_ele,'Segmentation').text = dat_info.conForDoc['segmentation']
        SubElement(temp_doc_ele,'PosTag').text = dat_info.conForDoc['postag']
        SubElement(temp_doc_ele,'Dependency').text = dat_info.conForDoc['dependency']
        temp_review_ele._children.append(temp_doc_ele)
        if len(dat_info.outConForSenList) != 0:
            temp_sens_ele = Element('CommentContentSens')
            for sen_info in dat_info.outConForSenList:
                temp_sen_ele = Element('CommentContentSen')
                SubElement(temp_sen_ele,'Content').text = sen_info['content']
                SubElement(temp_sen_ele,'Segmentation').text = sen_info['segmentation']
                SubElement(temp_sen_ele,'PosTag').text = sen_info['postag']
                SubElement(temp_sen_ele,'Dependency').text = sen_info['dependency']
                temp_sens_ele._children.append(temp_sen_ele)
            temp_review_ele._children.append(temp_sens_ele)
        root_paper_tree.append(temp_review_ele)
        #break
    dump(indent(root_paper_tree))
    ele_tree.write(out_file,'utf-8')
    #ele_tree.write(out_file)

def load_xml_data(in_file):
    dom = minidom.parse(in_file)
    review_info_node_list = dom.getElementsByTagName("REVIEW")
    all_review_list = []
    for review_info_node in review_info_node_list:
        review_info = ChangeDatToXML.DataStruct()
        review_info.commentID = review_info_node.getElementsByTagName("CommentID")[0].childNodes[0].nodeValue
        review_info.movieName = review_info_node.getElementsByTagName("MovieName")[0].childNodes[0].nodeValue
        review_info.userInfo = review_info_node.getElementsByTagName("UserInfo")[0].childNodes[0].nodeValue
        review_info.sentiLabel = review_info_node.getElementsByTagName("SentiLabel")[0].childNodes[0].nodeValue
        review_info.movieType = review_info_node.getElementsByTagName("MovieType")[0].childNodes[0].nodeValue
        review_info.conForDoc = ChangeDatToXML.get_con_dat_dict()
        review_info.conForDoc['content'] = review_info_node.getElementsByTagName("CommentContentDoc")[0].getElementsByTagName("Content")[0].childNodes[0].nodeValue
        review_info.conForDoc['segmentation'] = review_info_node.getElementsByTagName("CommentContentDoc")[0].getElementsByTagName("Segmentation")[0].childNodes[0].nodeValue
        review_info.conForDoc['postag'] = review_info_node.getElementsByTagName("CommentContentDoc")[0].getElementsByTagName("PosTag")[0].childNodes[0].nodeValue
        review_info.conForDoc['dependency'] = review_info_node.getElementsByTagName("CommentContentDoc")[0].getElementsByTagName("Dependency")[0].childNodes[0].nodeValue
        sen_info_node_list = review_info_node.getElementsByTagName("CommentContentSen")
        if len(sen_info_node_list) != 0:
            for sen_info_node in sen_info_node_list:
                sen_info_dict = ChangeDatToXML.get_con_dat_dict()
                sen_info_dict['content'] = sen_info_node.getElementsByTagName("Content")[0].childNodes[0].nodeValue
                sen_info_dict['segmentation'] = sen_info_node.getElementsByTagName("Segmentation")[0].childNodes[0].nodeValue
                sen_info_dict['postag'] = sen_info_node.getElementsByTagName("PosTag")[0].childNodes[0].nodeValue
                sen_info_dict['dependency'] = sen_info_node.getElementsByTagName("Dependency")[0].childNodes[0].nodeValue
                review_info.outConForSenList.append(sen_info_dict)
        all_review_list.append(review_info)

    return all_review_list


if __name__=="__main__":

    all_review_list = load_xml_data('./OutData/all_dat.xml')

    print_out_all_dat_list(all_review_list,'./OutData/all_dat2.xml')

