from __future__ import division
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from bs4 import BeautifulSoup, Comment
import time, re
import numpy as np
import json
import webbrowser
import Tkinter as tk
import sys

def calculate_Tfidf(tf,df):
	N=13645
	return (1+np.log10(tf))*(np.log10(N/df))

def get_json(indexFile):
	with open(indexFile) as handle:
		return json.load(handle)
def getCapitals(content):
	terms = []
	word = ""
	for i in range(len(content)):
		if len(word) >= 2 and len(word) <= 15 and not isstopwords(word.lower()) and word.isupper():
			terms.append(word)
		word = ""
		for j in range(len(content[i])):
			# if content[i][j].isalpha() or content[i][j].isdigit() or (content[i][j]=='-' and len(word)>0):
			if content[i][j].isalpha():
				word += content[i][j]
			else:
				if len(word) >= 3 and len(word) <= 15 and not isstopwords(word.lower()) and word.isupper():
					terms.append(word)
				word = ""
	if len(word) >= 2 and len(word) <= 15 and not isstopwords(word.lower()) and word.isupper():
		terms.append(word)
	#get_stem(terms)
	return terms
def isstopwords(word):
	sw = set(stopwords.words('english'))
	if word in sw:
		return True
	else:
		return False
def termProcessing(content):
	terms = []
	#content = query.split(' ')
	
	word=""
	for i in range(len(content)):
		if len(word)>=3 and len(word)<=15 and not isstopwords(word):
			terms.append(word.lower())
		word = ""
		for j in range(len(content[i])):
			if content[i][j].isalpha() or content[i][j].isdigit():
				word += content[i][j]
			else:
				if len(word)>=3 and len(word)<=15 and not isstopwords(word):
					terms.append(word.lower())
				word=""
	
	
	if len(word)>=3 and len(word)<=15 and not isstopwords(word):
		terms.append(word.lower())
	print terms
	get_stem(terms)
	print terms
	return terms
def get_stem(content):
	stemmer = SnowballStemmer('english')
	for k in range(len(content)):
		content[k] = stemmer.stem(content[k]).encode('utf-8')

	#indexPathBase = "/Users/GJzh/Desktop/JunGuo/results/"
#filePathBase = "/Users/GJzh/Downloads/WEBPAGES_RAW/"
#D:\18W\information_CS221\CS-221-project3-search-engine-master\database\index
def search(query,top_num):
	indexPathBase = "database"
	MapFile = "database/WEBPAGES_RAW/bookkeeping.json"
	hash = get_json(MapFile)
	query_tokens = termProcessing([query])
	print query_tokens[0]
	Documents = {}
	len_tokens=len(query_tokens)
	res=[]
	index = {}
	for item in query_tokens:
		idx=get_json(indexPathBase + '/index/' + item[0] + '/' + item[1] + '/' + item[2] + '.json')
		for k in range(len(idx)):
			if idx[k][0] == item:
				search_pool = idx[k][1]
				for (key, value) in search_pool.items():
					documentName = key.encode('utf-8')
					#Documents[documentName] = value['tf'.decode('utf-8')]
					Documents[documentName] = value['tf-idf'.decode('utf-8')]
		results_raw = sorted(Documents.iteritems(), key=lambda d: -d[1])
	
	length=len(results_raw)
	length=min(length, int(top_num))
	for i in range(length):
		res.append(hash[results_raw[i][0]])
	return res
#items=["Informatics", "Mondego", "Irvine", "artificial intelligence", "computer science"]
#items=["Informatics", "Mondego", "Irvine"]

#res=search(sys.argv[1],sys.argv[2])


#for r in res: print (r)