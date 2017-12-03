
# gensim modules
from gensim import utils
from gensim.models.doc2vec import LabeledSentence, TaggedDocument
from gensim.models import Doc2Vec
# random
from random import shuffle
# classifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_similarity
from gensim.models import word2vec
from gensim.models.keyedvectors import KeyedVectors
import numpy as np

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import nltk
import re


class text_classifier:

	model = None
	def __init__(self):
		model_path='../data/GoogleNews-vectors-negative300.bin'
		self.model = KeyedVectors.load_word2vec_format(model_path, binary=True)  # C binary format
		print (self.model.similarity('mutton','mutton'))



	# main solution for the baseline

	def get_subj_verbs(self,sent):
		useful_words = []
		stopWords = set(stopwords.words('english'))
		text = word_tokenize(sent)
		tags = nltk.pos_tag(text)
		
		for tagged_word in tags:
			w,pos = tagged_word
			# TODO: experiment with different POS
			if pos in ['NN','VB','VBP'] and (re.match('^[\w-]+$', w) is not None):
				useful_words.append(w)
		return useful_words


	def get_para_feature_words(self,text):
		'''The words are selected from the para that make the neural net feats'''
		sent_tokenize_list = sent_tokenize(text)

		sv_list = []
		for sent in sent_tokenize_list:
			items = self.get_subj_verbs(sent)
			sv_list.append(items)
		return (sv_list)
		
	def get_flattened_list(self,list_contents):
		return [item for sublist in list_contents for item in sublist]
		
	def classify(self,para):
		
		class_word = ['legal','sports','health']
		class_count = {}
		for key in class_word:
			class_count[key]=0
		
		feature_words=[]
		feature_words = self.get_para_feature_words(para)
		feature_words_flat = self.get_flattened_list(feature_words)
		
		for w in feature_words_flat:

				best_class = None
				similarity_score = -100
				# get max similarity class
				for c in class_word:
					score = -100
					try:
						score = self.model.similarity(w, c)
					except:
						#TODO:  see how to handle this; idea1 : create own model for this
						# add to a dictionary for the class determined
						print ('{} not found'.format(w))

					if(similarity_score < score):
						similarity_score = score
						best_class = c

				# print ('best class is :'+str(best_class))
				# update class count
				if best_class is not None:
					class_count[best_class] = class_count[best_class] + 1

		majority_class = None
		max_count = 0
		for k in class_count:
			#print (k,class_count[k])
			if(max_count<class_count[k]):
				max_count = class_count[k]
				majority_class = k

		
		#print ('sentence={}... , label = {} '.format(para[:20],majority_class))
		return majority_class


#classifier = text_classifier()
