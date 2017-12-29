
from __future__ import print_function

import logging
import os
import sys
import multiprocessing
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

def train(input_file,output_file):

    model = Word2Vec(LineSentence(input_file), size=200, window=5, min_count=5,
                     workers=multiprocessing.cpu_count())
    model.save(output_file)

def main():
	input_file = '../../scrapedata/'+'merged_file.txt'
	print (input_file)
	train(input_file,'./legal.health.model')

main()