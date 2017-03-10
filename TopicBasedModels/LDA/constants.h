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

#ifndef _CONSTANTS_H
#define _CONSTANTS_H

#include <string>
using namespace std;

#define	BUFF_SIZE_LONG	1000000
#define	BUFF_SIZE_SHORT	512

#define	MODEL_STATUS_UNKNOWN	0
#define	MODEL_STATUS_EST	1
#define	MODEL_STATUS_INF	2

#define	MODEL_NAME_UNKNOWN	0
#define	MODEL_NAME_LDA	1
#define	MODEL_NAME_JST	2
#define	MODEL_NAME_USTM_FW_W	3
#define	MODEL_NAME_SENLDA	4
#define	MODEL_NAME_ASUM	5
#define	MODEL_NAME_D_PLDA	6


struct Model_Para
{
    int model_type;
    int model_status;
    string dir;
    string data_file;
    string save_model_name;
    double alpha;
    double beta;
    int numTopics;
    int niters;
    int twords;
    string wordmapfile;
    string log_file;
};

#endif

