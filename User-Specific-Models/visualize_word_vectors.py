import driver_class as dr
import sys  
import pdb

import matplotlib.pyplot as plt
import pandas as pd

import numpy as np
from sklearn.decomposition import PCA as sklearnPCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.datasets.samples_generator import make_blobs
from pandas.tools.plotting import parallel_coordinates
from pandas import DataFrame
from sklearn.manifold import TSNE


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


def get_vectors(category,model_path, text,n_words,is_bin_file):
	driver = dr.Driver(model_path,is_bin_file)
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

	
	model_dict = {
		'custom' : 'legal.health.model',
		'goog':  'GoogleNews-vectors-negative300-SLIM.bin'
	}
	root_path = '../../sampledata'
	
	model_path = '../../pretrained_models/'+model_dict['goog']
	is_bin_file = True

	vectors_dict={}
	vocab_n_words = 10

	data_matrix = []
	labels = []
	for category in cat_dict:

		text = get_text_from_file('/'.join([root_path,cat_dict[category]]))
		vectors_dict[category] = get_vectors(category, model_path, text, vocab_n_words,is_bin_file)
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
	print(pca.explained_variance_ratio_)
	return transformed

def plot_data(X,y):
	'''
	Unused method, consider fixing / removing
	'''

	print 'plotting data'
	print type(X.shape)
	print type(y.shape)

	# c = y
	print (X.iloc[:,0].shape)
	print (X.iloc[:,1].shape)
	# figure out the colours
	# Try 2 separate plots
	# try 1 plot over the other

	# TODO: convert to where clause on df
	class_idx_dict = {}
	colour_dict ={}
	index = 0

	y_list = list(y.values.flatten())
	for y_val in y_list:

		if y_val not in class_idx_dict:
			class_idx_dict[y_val]= [] 
		
		class_idx_dict[y_val].append(index)
		index +=1

	fig1 = plt.figure()
	for label in [0,1]:
		rows_idx = class_idx_dict[label]
		if label==0:
			colour = 'red'
		else:
			colour = 'blue'
		plt.scatter(X.iloc[rows_idx,0],X.iloc[rows_idx,1],color =colour)
		
	plt.show()


	fig1 = plt.figure()
	for label in [1,0]:
		rows_idx = class_idx_dict[label]
		if label==0:
			colour = 'red'
		else:
			colour = 'blue'
		plt.scatter(X.iloc[rows_idx,0],X.iloc[rows_idx,1],color =colour)
		
	plt.show()

def plot_transformed(Z,y):
	
	# TODO: clean up/refactor to make a dictionary for multiple class
	
	idx_list_0=[]
	idx_list_1=[]
	for row_id in range(len(y)):

		if y[row_id] == 0:
			idx_list_0.append(row_id)
		else:
			idx_list_1.append(row_id)

	# TODO: different classes should have different colors
	plt.scatter(Z[idx_list_0, 0], Z[idx_list_0, 1],color = 'red')
	plt.scatter(Z[idx_list_1, 0], Z[idx_list_1, 1],color = 'blue')
	'''
	label_list = []
	for row in rows:
		label_list.append(labels[row])

	for label, x, y in zip(label_list, Z[:, 0], Z[:, 1]):
		plt.annotate(label, xy=(x, y), xytext=(0, 0), textcoords='offset points')
		'''
	plt.show()

def plot_data_tsne(X,labels):

	tsne = TSNE(n_components=2, random_state=0)
	np.set_printoptions(suppress=True)
	nr,_ = X.shape
	rows = [int(w) for w in np.linspace(0,nr-200,1000)]

	Z = tsne.fit_transform(X[rows,:])
	y = []
	for row in rows:
		y.append(labels[row])

	plot_transformed(Z,y)


# main
(data_matrix, labels) = populate_category_vectors()

X_rot = make_2d_proj(data_matrix,20)
y = DataFrame(labels)
#plot_data(X_rot,y)



plot_data_tsne(np.matrix(data_matrix), list(y.values.flatten()))

