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

#ifndef	_DATASET_H
#define	_DATASET_H

#include <string>
#include <vector>
#include <map>
#include <fstream>
#include "map_type.h"

using namespace std;

struct word_phrase{
    int head_word;
    int modify_word;
};

class document {
public:
    word_phrase* phrases;               // used for phrase-based LDA
    int * words;                        // used for word-based LDA
    int length;
    string docID;

    document() {
        words = NULL;
        length = 0;
    }

    document(int length) {
        this->length = length;
        words = new int[length];
        phrases = new word_phrase[length];
    }

    document(vector<int> & doc) {
        this->length = doc.size();
        this->words = new int[length];
        for (int i = 0; i < length; i++) {
            this->words[i] = doc[i];
        }
    }

    document(vector<int> & doc, string docID) {
		this->length = doc.size();
        this->words = new int[length];
        for (int i = 0; i < length; i++) {
            this->words[i] = doc[i];
        }
        this->docID = docID;
	}

	int is_contain_word(int temp_word){
	    if (length == 0) return 0;
	    for (int i = 0; i < length; i++){
            if (temp_word == words[i]) return 1;
	    }
	    return 0;
	}

	void release_space(){
        if (words)
            delete words;
        if (phrases)
            delete phrases;

	}

    ~document() {
        release_space();
    }
};

class dataset {
public:
    document ** docs;               // store training data vocab ID
    document ** _docs;              // used only for inference
    vector<string> bdocs;           // for buffering dataset


    mapword2id word2id_train;
    mapid2word id2word_train;
    mapword2id demo2id_train;

    map<int, int> _id2id;   // also used only for inference (wordid in testdata -> wordid in traindata)
    map<int, int> id2_id;   // also used only for inference (wordid in traindata -> wordid in testdata)

    int numDocs;            // number of documents
	int aveDocLength;       // average document length
	int vocabSize;          // number of vocab
	int corpusSize;

    dataset() {
        docs = NULL;
        _docs = NULL;
        this->numDocs = 0;
        this->vocabSize = 0;
        this->corpusSize = 0;
    }

    dataset(int M) {
        this->numDocs = M;
        this->vocabSize = 0;
        this->corpusSize = 0;
        docs = new document*[numDocs];
        _docs = NULL;
    }

    ~dataset() {
       release_space();
    }

    void release_space() {
        if (docs) {
            for (int i = 0; i < numDocs; i++){
                if (docs[i]){
                    docs[i]->release_space();
                    delete docs[i];
                }
            }
        }
        delete docs;
        docs = NULL;

        if (_docs) {
            for (int i = 0; i < numDocs; i++) {
                if (_docs[i]){
                    _docs[i]->release_space();
                    delete _docs[i];
                }
            }
        }
        delete _docs;
        _docs = NULL;

    }

    void add_doc(document * doc, int idx) {
        if (0 <= idx && idx < numDocs) {
            docs[idx] = doc;
        }
    }

    void _add_doc(document * doc, int idx) {
        if (0 <= idx && idx < numDocs) {
            _docs[idx] = doc;
        }
    }

    static int write_wordmap(string wordmapfile, mapword2id * pword2id);
    static int read_wordmap(string wordmapfile, mapword2id * pword2id);
    static int read_wordmap(string wordmapfile, mapid2word * pid2word);

    int read_traindata(string dfile, string wordmapfile, string mode);
    int read_testdata(string dfile, string wordmapfile);


    int change_id2id(int _w){
        return _id2id.find(_w)->second;}

    int changeid2_id(int w){
        return id2_id.find(w)->second;}

    string get_str_from_id(int word_id){
        mapid2word::iterator it = id2word_train.find(word_id);
        if (it != id2word_train.end())
            return it->second;
        else
            return "ERROR NULL";
    }

    int get_id_from_str(string str){
        mapword2id::iterator it = word2id_train.find(str);
        if (it != word2id_train.end())
            return it->second;
        else
            return -1;
    }


private:
    int analyze_train_corpus(string wordmapfile);
    int analyze_test_corpus(string wordmapfile);
};












#endif

