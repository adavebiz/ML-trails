import driver_class as dr
import sys  

import matplotlib.pyplot as plt
import pandas as pd

from sklearn.decomposition import PCA as sklearnPCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.datasets.samples_generator import make_blobs
from pandas.tools.plotting import parallel_coordinates
from pandas import DataFrame


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
	label_dict={
		'legal':0,
		'health':1
	}
	root_path = '../../sampledata'
	model_path = '../../pretrained_models/GoogleNews-vectors-negative300-SLIM.bin'
	vectors_dict={}
	vocab_n_words = 10

	data_matrix = []
	labels = []
	for category in cat_dict:

		text = get_text_from_file('/'.join([root_path,cat_dict[category]]))
		vectors_dict[category] = get_vectors(category, model_path, text, vocab_n_words)
		vectors = vectors_dict[category]
		print 'cat={} , size = {},{}'.format(category,len(vectors),len(vectors[0]))


		if len(data_matrix) == 0:
			data_matrix = vectors
			labels = [label_dict[category]]*len(vectors)
		else:
			for v in vectors:
				data_matrix.append(v)
				labels.append(label_dict[category])
	

	return (data_matrix, labels)

			
def make_2d_proj(data_mat,n_dim):
	X = DataFrame(data_mat)
	#X = X.transpose()
	X_norm = (X - X.min())/(X.max() - X.min())
	pca = sklearnPCA(n_components=n_dim) #2-dimensional PCA
	transformed = pd.DataFrame(pca.fit_transform(X_norm))
	return transformed

def plot_data(X,y):
	print 'testing complete'
	print type(X.shape)
	print type(y.shape)

	# c = y
	print (X.iloc[:,0].shape)
	print (X.iloc[:,1].shape)
	# figure out the colours
	# Try 2 separate plots
	# try 1 plot over the other
	plt.scatter(X.iloc[:,0], X.iloc[:,1],c = y.iloc[:,0])
	plt.show()


# main
(data_matrix, labels) = populate_category_vectors()

X_rot = make_2d_proj(data_matrix,2)
y = DataFrame(labels)
plot_data(X_rot,y)




