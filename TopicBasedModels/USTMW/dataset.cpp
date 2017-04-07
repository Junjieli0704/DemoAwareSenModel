/*
 * Copyright (C) 2007 by
 *
 * 	Xuan-Hieu Phan
 *	hieuxuan@ecei.tohoku.ac.jp or pxhieu@gmail.com
 * 	Graduate School of Information Sciences
 * 	Tohoku University
 *
 * GibbsLDA++ is a free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published
 * by the Free Software Foundation; either version 2 of the License,
 * or (at your option) any later version.
 *
 * GibbsLDA++ is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with GibbsLDA++; if not, write to the Free Software Foundation,
 * Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA.
 */

#include <stdio.h>
#include <stdlib.h>
#include "constants.h"
#include "strtokenizer.h"
#include "dataset.h"

using namespace std;

int dataset::write_wordmap(string wordmapfile, mapword2id * pword2id) {
    FILE * fout = fopen(wordmapfile.c_str(), "w");
    if (!fout) {
        printf("Cannot open file %s to write!\n", wordmapfile.c_str());
        return 1;
    }

    mapword2id::iterator it;
    fprintf(fout, "%d\n", pword2id->size());
        for (it = pword2id->begin(); it != pword2id->end(); it++) {
        fprintf(fout, "%s %d\n", (it->first).c_str(), it->second);
    }
    fclose(fout);
    return 0;
}

int dataset::read_wordmap(string wordmapfile, mapword2id * pword2id) {
    pword2id->clear();

    FILE * fin = fopen(wordmapfile.c_str(), "r");
    if (!fin) {
        printf("Cannot open file %s to read!\n", wordmapfile.c_str());
        return 1;
    }

    char buff[BUFF_SIZE_SHORT];
    string line;

    fgets(buff, BUFF_SIZE_SHORT - 1, fin);
    int nwords = atoi(buff);

    for (int i = 0; i < nwords; i++) {
        //cout<<i<<endl;
        fgets(buff, BUFF_SIZE_SHORT - 1, fin);
        line = buff;
        //cout<<line<<endl;
        strtokenizer strtok(line, " \t\r\n");
        //cout<<"ffffff"<<endl;
        if (strtok.count_tokens() != 2) {
            continue;
        }
        //cout<<"eeeeee"<<endl;

        pword2id->insert(pair<string, int>(strtok.token(0), atoi(strtok.token(1).c_str())));
    }

    fclose(fin);

    return 0;
}

int dataset::read_wordmap(string wordmapfile, mapid2word * pid2word) {
    pid2word->clear();

    FILE * fin = fopen(wordmapfile.c_str(), "r");
    if (!fin) {
        printf("Cannot open file %s to read!\n", wordmapfile.c_str());
        return 1;
    }

    char buff[BUFF_SIZE_SHORT];
    string line;

    fgets(buff, BUFF_SIZE_SHORT - 1, fin);
    int nwords = atoi(buff);

    for (int i = 0; i < nwords; i++) {
        fgets(buff, BUFF_SIZE_SHORT - 1, fin);
        line = buff;

        strtokenizer strtok(line, " \t\r\n");
        if (strtok.count_tokens() != 2) {
            continue;
        }

        pid2word->insert(pair<int, string>(atoi(strtok.token(1).c_str()), strtok.token(0)));
    }

    fclose(fin);

    return 0;
}

int dataset::read_data(string dfile, string wordmapfile, string mode = "word") {

    bdocs.clear();
    numDocs = 0;
    ifstream filestring(dfile.c_str());
    if (!filestring.good()){
        printf("Cannot open file %s to read!\n", dfile.c_str());
        return 1;
    }

	string line;
	while (getline(filestring,line)){
		if(line.empty()) continue;
		bdocs.push_back(line);
        numDocs++;
	}

	if (numDocs > 0) {
        if (mode == "word")
            this->analyze_corpus(wordmapfile);
	}

	filestring.close();
	return 0;
}

int dataset::analyze_corpus(string wordmapfile) {

    if (docs) {
		release_space();
		docs = new document*[numDocs];
    }
	else {
		docs = new document*[numDocs];
	}

    mapword2id::iterator it;

    for (int i = 0; i < (int)bdocs.size(); ++i) {
		string line = bdocs.at(i);
		strtokenizer strtok(line, " \t\r\n");    // \t\r\n are the separators
		int length = strtok.count_tokens();

		if (length <= 0) {
			printf("Invalid (empty) document!\n");
			release_space();
			numDocs = vocabSize = 0;
			return 1;
		}

		int docLength = length - 1;  // the first word is document name/id
        corpusSize += docLength;
        // allocate memory for the new document_i
        document * pdoc = new document(docLength);
        pdoc->docID = strtok.token(0);

        // generate ID for the tokens in the corpus, and assign each word token with the corresponding vocabulary ID.
        for (int j = 0; j < docLength; j++) {
            string token_word = strtok.token(j+1);
            it = word2id.find(token_word);
            if (it == word2id.end()) {
                // word not found, i.e., new word
                pdoc->words[j] = word2id.size();
                id2word.insert(pair<int,string>(word2id.size(),token_word));
                word2id.insert(pair<string, int>(token_word, word2id.size()));
            }
            else pdoc->words[j] = it->second;
        }
        add_doc(pdoc, i);
    }


    // write word map to file
    if (write_wordmap(wordmapfile, &word2id)) {
        return 1;
    }

      // update number of words
    vocabSize = word2id.size();
    aveDocLength = corpusSize/numDocs;
    return 0;
}

