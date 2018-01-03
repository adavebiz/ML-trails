from gensim import utils
from gensim.models.doc2vec import LabeledSentence, TaggedDocument
from gensim.models import Doc2Vec
from random import shuffle
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_similarity
from gensim.models import word2vec
from gensim.models.keyedvectors import KeyedVectors
import numpy as np

class vocabulary_extender:

    '''This class is responsible for creating a extended vocabulary from sampled user keywords'''

    w2v_model = None
    def __init__(self,model_path):
        self.w2v_model = KeyedVectors.load_word2vec_format(model_path, binary=True)  # C binary format

    def make_extended_vocabulary(self, user_vocab, topnwords):

        extended_vocabulary = []

        for word in user_vocab:

            try:
                most_similar_words = self.w2v_model.most_similar(word, topn=topnwords)

                for similar_word in most_similar_words:
                    (w,similarity)  = similar_word
                    extended_vocabulary.append(w)

            except:
                print("Exception occurs")

        return extended_vocabulary

    def extended_vocabulary_vectors(self, user_vocab, topnwords):
        extended_vocabulary = self.make_extended_vocabulary(user_vocab, topnwords)
        extended_vocabulary_vectors_list = []
        for word in extended_vocabulary:
            extended_vocabulary_vectors_list.append(self.w2v_model[word])
        return extended_vocabulary_vectors_list
