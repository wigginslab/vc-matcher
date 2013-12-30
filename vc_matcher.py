from nltk import *
import sys
import csv
import pickle
import datetime
import re
import json

def gen_features(startup_ngrams, label=None):
	"""
	Generates a feature set from ngrams

	args:
		startup_ngrams: ngrams in the startup 
		label: 1 if it has been invested in the VC being trained for,
				0 if not, None if the featureset is a test set

	returns:
		feature_list: returns a featureset NLTK can classify based on
	"""
	feature_list = []
	for ngrams in startup_ngrams:
		for ngram in ngrams:
			ngram = tuple([x.lower() for x in ngram])
			feature_dic= {}
			feature_dic['contains %s' %(ngram,)] = True
			if label == True:
				feature_list.append((feature_dic,1))
			elif label == False:
				feature_list.append((feature_dic, 0))
			else:
				feature_list.append((feature_dic))
	return feature_list

def gen_word_features(startup_ngrams, mode='train'):
	feature_list = []
	for ngrams in startup_ngrams:
		for ngram in ngrams:
			for word in ngram:
				feature_dic= {}
				feature_dic['contains (%s)' %(word.lower())] = True
				if mode == 'train':
					feature_list.append((feature_dic,1))
				else:
					feature_list.append((feature_dic))
	return feature_list

def build_model(yes_cograms, no_cograms):
	"""
	Builds a naive bayes model based on no_cograms

	args:
		yes_cograms: cograms corresponding to the VC
		no_cograms: cograms not corresponding to the VC

	returns:
		pickled_classifier: a pickled naive bayes classifier
	"""
	feature_set = gen_features(no_cograms, label=False)
	feature_set = feature_set + gen_features(yes_cograms, label=True)
	classifier = NaiveBayesClassifier.train(feature_set)
	pickled_classifier = pickle.dumps(classifier)
	return pickled_classifier

def test(model, text):
	"""
	Takes a VC model and the user given text and returns probability of the VC investing in that company

	args:
		model: NaiveBayesClassifier
		text: description of startup from user

	returns: 
		accuracy: percent accuracy of model
	"""
	new_ngrams = build_ngrams(text)
	new_features = gen_features(new_ngrams)
	return model.prob_classify(new_features[0]).prob(1)


def build_ngrams(text):
	"""
	Convert text to bigrams and trigrams

	args:
		text: text to convert

	returns:
		ngrams: a list of bigrams and trigrams
	"""
	# remove punctuation
	text = re.findall("\w+", text)
	text_bigrams = [x for x in bigrams(text)]
	text_trigrams = [x for x in trigrams(text)]
	ngrams = text_bigrams + text_trigrams
	return [ngrams]

def match_vc(text, page):
	"""
	Returns venture capitalist suggestions for a text description of a startup.

	args:
		text: text description of a startup
		page: what range of crunchbase VC entries to search

	returns:
		vc_holder: JSON holding the VC name, url, and percent match
	"""
	"""
	ngrams = build_ngrams(text)
	new_features = gen_features(ngrams)

	lower_query_bound = str((page-1) * 50)
	upper_query_bound = str(page * 50)
	if int(upper_query_bound) > 438:
		upper_query_bound = str(438)

	# query database for VCs
	vcs = db.session.query(VC).filter("id >="+ lower_query_bound +" AND id <="+upper_query_bound).all()

	vc_names = []
	vc_urls = []
	percent = []

	# get results
	for vc in vcs:
		vc_name = vc.name
		vc_url = vc.url
		vc_model = pickle.loads(vc.nb_model)
		result = vc_model.prob_classify(new_features[0]).prob(1)
		# how much of a match must it be to be returned
		threshold = .6
		if result >= threshold:
			percent.append(result)
			vc_names.append(vc_name)
			vc_urls.append(vc_url)

	vc_holder = {"listItems":[]}

	# format to json
	for i in range(0,len(vc_names)):
		json_dic = {
			'name': vc_names[i],
			'url': vc_urls[i],
			'result': percent[i]
		}
		vc_holder['listItems'].append(json_dic)

	return vc_holder
"""