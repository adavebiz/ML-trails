from text_parser import text_parser
from vocabulary_extender import vocabulary_extender

text = "Deciding whether to sell items on an as-is basis or with a warranty depends on the type of item being sold and whether or not offering a warranty makes financial sense for the seller. Once the decision has been made, it's important to clearly outline the terms in the bill of sale contract."

parser = text_parser()
extender = vocabulary_extender()
user_dict = parser.get_para_feature_words(text)
#extended_dict = extender.make_extended_vocabulary(user_dict,10)
extended_dict = extender.extended_vocabulary_vectors(user_dict,10)
print(extended_dict)