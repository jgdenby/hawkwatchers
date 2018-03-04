import math
import nltk
import math
import pandas as pd
import numpy as np 

import sklearn
import sklearn.neural_network

from sklearn.model_selection import train_test_split


def predict(new_text):
	'''
	Takes a new release text and, using a neural network model trained
	on the tf-idf scores for all press releases since February 1994,
	predicts whether the new text heralds an increase in the federal
	interest rate.

	Inputs:
		new_text (str): a string representation of the new release text

	Outputs:
		prediction (str): 
	'''
	# reads local csv with all releases from Feb 1994, the month & year
	# of release, the numerical change in interest rate associated
	# with that month, and a boolean expression indicating whether
	# the interest rate increased
	releaserates_df = pd.read_csv('allreleaserates.csv', index_col=0)


	# computes tf-idf for all release texts and creates a vector representation
	# of each document's scores
	TFVectorizer = sklearn.feature_extraction.text.TfidfVectorizer(max_df=15,
		stop_words='english', norm='l2')

	TFVects = TFVectorizer.fit_transform(releaserates_df['release_text'])
	releaserates_df['vect'] = [np.array(v).flatten() for v in TFVects.todense()]

	# instantiate and fit neural network model
	clf_nn = sklearn.neural_network.MLPClassifier()
	clf_nn.fit(np.stack(releaserates_df['vect'], axis=0), releaserates_df['increase'])

	# compute tf-idf for new_text
	TFVects_test = TFVectorizer.transform([new_text])
	test_vects = [np.array(v).flatten() for v in TFVects_test.todense()]

	# classify new_text 
	y_pred = clf_nn.predict(np.stack(test_vects, axis=0))

	return y_pred[0]




