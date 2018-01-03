from text_parser import text_parser
from vocabulary_extender import vocabulary_extender

class Driver:

	def get_extended_vocab_vectors(self,text,n_words):
			user_dict = self.parser.get_para_feature_words(text)
			extended_dict = self.extender.extended_vocabulary_vectors(user_dict,n_words)
			return (extended_dict)

	def __init__(self,model_path):
		self.parser = text_parser()
		self.extender = vocabulary_extender(model_path)
		
# parameters of the model		
n_words = 10
model_path = '../../pretrained_models/GoogleNews-vectors-negative300-SLIM.bin'
text = "Deciding whether to sell items on an as-is basis or with a warranty depends on the type of item being sold and whether or not offering a warranty makes financial sense for the seller. Once the decision has been made, it's important to clearly outline the terms in the bill of sale contract."
driver = Driver(model_path)
extended_vocab_vectors = driver.get_extended_vocab_vectors(text,n_words)

print (len(extended_vocab_vectors))
print (len(extended_vocab_vectors[0]))
