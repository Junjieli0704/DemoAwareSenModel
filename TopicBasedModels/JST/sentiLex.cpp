/**********************************************************************
		        Joint Sentiment-Topic (JST) Model
***********************************************************************

(C) Copyright 2013, Chenghua Lin and Yulan He

Written by: Chenghua Lin, University of Aberdeen, chenghua.lin@abdn.ac.uk.
Part of code is from http://gibbslda.sourceforge.net/.

This file is part of JST implementation.

JST is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free
Software Foundation; either version 2 of the License, or (at your
option) any later version.

JST is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
USA

***********************************************************************/

#include "sentiLex.h"

sentiLex::sentiLex()
{

}

sentiLex::~sentiLex()
{

}

int sentiLex::read_senti_lexicon(string senti_lex_file) {
	word2senLabelDis.clear();
	char buff[BUFF_SIZE_SHORT];
    string line;
    vector<double> wordPrior;
    int labID;
    double tmp, val;
    int numSentiLabs;

    FILE * fin = fopen(senti_lex_file.c_str(), "r");
    if (!fin) {
		printf("Cannot read file %s!\n", senti_lex_file.c_str());
		return 1;
    }

    while (fgets(buff, BUFF_SIZE_SHORT - 1, fin) != NULL) {
		line = buff;
		strtokenizer strtok(line, " \t\r\n");

		if (strtok.count_tokens() < 1)  {
			printf("Warning! The strtok count in the lexicon line [%s] is smaller than 2!\n", line.c_str());
		}
		else {
			tmp = 0.0;
			labID = 0;
			wordPrior.clear();
			numSentiLabs = strtok.count_tokens();
			for (int k = 1; k < strtok.count_tokens(); k++) {
				val = atof(strtok.token(k).c_str());
				if (tmp < val) {
					tmp = val;
					labID = k-1;
				}
				wordPrior.push_back(val);
			}
			// labID: the maximum place in wordPrior.
			Word_Prior_Attr temp = {labID, wordPrior};  // sentiment label ID, sentiment label distribution
			word2senLabelDis.insert(pair<string, Word_Prior_Attr >(strtok.token(0), temp));
		}
    }

	if (word2senLabelDis.size() <= 0) {
		printf("Can not find any sentiment lexicon in file %s!\n", senti_lex_file.c_str());
		return 1;
	}

    fclose(fin);
    return 0;
}

int sentiLex::load_non_senti_word_prior(mapword2id* word2id){

    int labID = 0;
    vector<double> wordPrior;
    wordPrior.push_back(0.9);
    wordPrior.push_back(0.05);
    wordPrior.push_back(0.05);
    Word_Prior_Attr temp = {labID, wordPrior};  // sentiment label ID, sentiment label distribution

    mapword2id::iterator word2id_iter;


    //cout<<word2senLabelDis.size()<<endl;

    for(word2id_iter=word2id->begin(); word2id_iter!=word2id->end(); word2id_iter++){
        string word_str = word2id_iter->first;
        if (word2senLabelDis.find(word_str) == word2senLabelDis.end()){
            word2senLabelDis.insert(pair<string, Word_Prior_Attr >(word_str, temp));
            //cout<<word_str<<endl;
        }
    }

    //cout<<word2senLabelDis.size()<<endl;



    return 0;

}


int sentiLex::get_wordid2senLabelDis(mapword2id* word2id){

    if (word2id->size() == 0) {
        printf("Error in sentiLex::get_wordid2senLabelDis()\n");
        printf("The map word2id is empty.......\n");
        return 1;
    }

    mapword2prior::iterator word2senti_iter;

    for(word2senti_iter = word2senLabelDis.begin(); word2senti_iter!=word2senLabelDis.end();++word2senti_iter){
        string word_str = word2senti_iter->first;
        Word_Prior_Attr word_prior_attr = word2senti_iter->second;
        mapword2id::iterator word2id_iter;

        word2id_iter = word2id->find(word_str);
        if (word2id_iter!= word2id->end()){
            int word_id = word2id_iter->second;
            wordid2senLabelDis.insert(pair<int, Word_Prior_Attr >(word_id, word_prior_attr));
        }
    }
    return 0;

}

