from nltk.corpus import stopwords
from nltk import word_tokenize
import nltk, string, os, re
sno = nltk.stem.SnowballStemmer('english')
from spell import *

def get_jaccard_sim(str1, str2):
	a = set(str1.split())
	b = set(str2.split())
	c = a.intersection(b)
	return float(len(c)) / (len(a) + len(b) - len(c))

def stematize(sentence):

	stemmed = []
	filtered = word_tokenize(sentence)
	for w in filtered:
		stemmed.append(sno.stem(w))

	sent = "".join([" " + i if not i.startswith("'") and i not in string.punctuation else i for i in stemmed]).strip()

	return sent

def remove_stop_words(sentence):
	stop_words = set(stopwords.words('english'))
	stop_words.update(["want", "I", "know", "What", "When", "how", "?", "!", ",", ".", "for"])
	word_tokens = word_tokenize(sentence)
	filtered = [w for w in word_tokens if not w in stop_words]

	sent = ""
	sent = "".join([" " + i if not i.startswith("'") and i not in string.punctuation else i for i in filtered]).strip()
	return sent

def symmetric_sentence_similarity(sent, sent2): 
	sents = correct(sent)
	sents2 = correct(sent2)
	return get_jaccard_sim(stematize(remove_stop_words(sents)), stematize(remove_stop_words(sents2)))