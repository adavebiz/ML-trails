from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import nltk
import re

class text_parser:
    
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
            for item in items:
                sv_list.append(item)
        return (sv_list)
