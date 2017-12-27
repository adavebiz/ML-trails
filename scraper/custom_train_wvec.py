
from __future__ import print_function

import logging
import os
import sys
import multiprocessing
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

def train(input_file,output_file,output_file2):

    model = Word2Vec(LineSentence(input_file), size=200, window=5, min_count=5,
                     workers=multiprocessing.cpu_count())

    model.save(output_file)
    model.wv.save_word2vec_format(output_file2, binary=False)


def main():
	input_file = '../../scrapedata/' +'legal_Administrative_centre.txt'
	print (input_file)
	train(input_file,'./of1','./of2')

main()