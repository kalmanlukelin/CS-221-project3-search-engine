from __future__ import division
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from bs4 import BeautifulSoup, Comment
import time, re
import numpy as np
import json
import webbrowser
import Tkinter as tk

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
    get_stem(terms)
    return terms

def get_stem(content):
    stemmer = SnowballStemmer('english')
    for k in range(len(content)):
        content[k] = stemmer.stem(content[k]).encode('utf-8')



#indexPathBase = "/Users/GJzh/Desktop/JunGuo/results/"
#filePathBase = "/Users/GJzh/Downloads/WEBPAGES_RAW/"
def search(query):
	indexPathBase = "C:/Github/CS-221-project3-search-engine/index"
	MapFile = "C:/Users/USER/Downloads/WEBPAGES_RAW/bookkeeping.json"
	hash = get_json(MapFile)
	query_tokens = termProcessing([query])

	Documents = {}
	len_tokens=len(query_tokens)
	res=[]
	index = {}

	for item in query_tokens:
		idx=get_json(indexPathBase + '/' + item[0] + '/' + item[1] + '/' + item[2] + '.json')
		for k in range(len(idx)):
			if idx[k][0] == item:
				search_pool = idx[k][1]
				for (key, value) in search_pool.items():
					documentName = key.encode('utf-8')
					#Documents[documentName] = value['tf'.decode('utf-8')]
					Documents[documentName] = value['tf-idf'.decode('utf-8')]

	results_raw = sorted(Documents.iteritems(), key=lambda d: -d[1])
	
	length=len(results_raw)
	length=min(length, 20)
	for i in range(length):
		res.append(hash[results_raw[i][0]])
	return res

items=["Informatics", "Mondego", "Irvine", "artificial intelligence", "computer science"]
#items=["Informatics", "Mondego", "Irvine"]
for item in items:
	print item
	res=search(item)
	for r in res: print r