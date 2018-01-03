import driver_class as dr
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

'''
visualize (w2vec) word vectors in 2D 
'''
#1. Get sample data  of 2 classes

def get_text_from_file(file_path):
	with open(file_path, 'r') as content_file:
	    content = content_file.read()
	return (content)


def get_vectors(category,model_path, text,n_words):
	driver = dr.Driver(model_path)
	vectors = driver.get_extended_vocab_vectors(text,n_words)
	return vectors

def populate_category_vectors():
	cat_dict = {
		'legal': 'legal/sample_merged_file_legal.txt',
		'health':'health/sample_merged_file_health.txt',
	}
	root_path = '../../sampledata'
	model_path = '../../pretrained_models/GoogleNews-vectors-negative300-SLIM.bin'
	vectors_dict={}
	vocab_n_words = 10
	for category in cat_dict:

		text = get_text_from_file('/'.join([root_path,cat_dict[category]]))
		vectors_dict[category] = get_vectors(category, model_path, text, vocab_n_words)
		vectors = vectors_dict[category]
		print 'cat={} , size = {},{}'.format(category,len(vectors),len(vectors[0]))


# main
populate_category_vectors()

