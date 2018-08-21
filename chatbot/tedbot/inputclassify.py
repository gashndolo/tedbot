import nltk, re, pprint
import sklearn
from nltk import word_tokenize, WordNetLemmatizer
from random import shuffle
from sklearn.svm import LinearSVC
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.metrics import classification_report


posts = nltk.corpus.nps_chat.xml_posts()[:10000]

def dialogue_act_features(post):

	"""
		features = {}
		for word in nltk.word_tokenize(post):
			features['contains({})'.format(word.lower())] = True
		
		
		return features"""
	text = nltk.word_tokenize(post)
	tagged = nltk.pos_tag(text)
	x = tagged[0]
	y = tagged[len(text) - 1]
	features = {}
	features['first_word'] = x[0]

	return features

def classifier(): 

	cls_set = ['Emotion', 'ynQuestion', 'yAnswer', 'Continuer',
	'whQuestion', 'System', 'Accept', 'Clarify', 'Emphasis', 
	'nAnswer', 'Greet', 'Statement', 'Reject', 'Bye', 'Other']

	featuresets = [] # list of tuples of the form (post, featuresets)

	for post in posts:

 		# applying the feature extractor to each post
		# post.get('class') is the label of the current post
 		featuresets.append((dialogue_act_features(post.text),cls_set.index(post.get('class'))))

	shuffle(featuresets)
	size = int(len(featuresets) * .1) # 10% is used for the test set
	train = featuresets[size:]
	test = featuresets[:size]

	classif = SklearnClassifier(LinearSVC())
	classif.train(train)

	test_skl = []
	t_test_skl = []
	for d in test:
 		test_skl.append(d[0])
 		t_test_skl.append(d[1])

	return classif

classifier()
"""
while True:
	question = raw_input()
	x = classif.classify_many(dialogue_act_features(question))
	print x
"""