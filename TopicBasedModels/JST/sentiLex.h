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


#ifndef SENTILEX_H
#define SENTILEX_H

#include "map_type.h"
#include "constants.h"
#include <fstream>
#include "strtokenizer.h"
#include <stdlib.h>

class sentiLex
{
    public:
        sentiLex();
        ~sentiLex();

        // map of word / word prior info [string => sentiment lab ID, sentiment label distribution]
        mapword2prior word2senLabelDis;

        // map of word / word prior info [word ID => sentiment lab ID, sentiment label distribition]
        mapwordid2prior wordid2senLabelDis;

        int read_senti_lexicon(string senti_lex_file);

        int load_non_senti_word_prior(mapword2id* word2id);

        int get_wordid2senLabelDis(mapword2id* word2id);

        //int print_out_word2senLabelDis_res(string out_file);

        int get_word_senlabel(int wordid){

            mapwordid2prior::iterator wordid2senti_iter;

            wordid2senti_iter = wordid2senLabelDis.find(wordid);

            if (wordid2senti_iter != wordid2senLabelDis.end())
                return wordid2senti_iter->second.id;
            else
                return -1;

        }




};

#endif // SENTILEX_H
