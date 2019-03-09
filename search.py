from bs4 import BeautifulSoup, Comment
import time, re
import json
import webbrowser
import Tkinter as tk
import sys
import os
import numpy as np
import math

from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords

def cal_tf_idf(tf, df):
    doc_num=37485
    if tf == 0 or df == 0: return 0
    return (1+math.log10(tf))*(math.log10(doc_num/df))

def load_json(file):
    with open(file) as f:
        return json.load(f)

def process_term(term_list):
    res=[]
    stopwds=set(stopwords.words('english'))
    stem = SnowballStemmer('english')
    for term in term_list:
        # Replace the non alphabaetical and numeric characters with space.
        # Change all the characters to lower case
        # Split characters based on space
        filter_term=re.compile('[^a-zA-Z0-9]').sub(' ', term).lower().split()

        for ft in filter_term:
            if len(ft) >= 3 and len(ft) <= 12 and not ft in  stopwds: # Get appropriate length of characters.
                ft_stemmed=stem.stem(ft)
                res.append(ft_stemmed)

    # return list of tokens
    return res 

# Sort it by normailzied cosine similarity first. If it's the same, then sort it without normalization.
def compare_func(ele1, ele2):
    if ele1[1]['ncos_sim'] != ele2[1]['ncos_sim']:
        return 1 if ele1[1]['ncos_sim'] < ele2[1]['ncos_sim'] else -1
    return 1 if ele1[1]['cos_sim'] < ele2[1]['cos_sim'] else -1

def cosin_similariy(arr1, arr2):
    return sum(np.multiply(arr1, arr2))

def search(path, query, top_num, optimize=True):
    print "Searching %s" % query

    # load index and database.
    bookkeeping = load_json(path+"/WEBPAGES_RAW/bookkeeping.json")
    index=None
    if not optimize: index = load_json(path+"/dict/index.json") # load database withou optimization

    # load doc info.
    doc_info = load_json(path+"/doc/doc.json")
    
    query_terms=process_term([query])
    len_query=len(query_terms)
    query_tf_idf=np.zeros(len_query)
    
    measure_docs={}
    
    for i in range(len(query_terms)):
        # check if the file exists.
        if not os.path.isfile(path + '/dict_tree/' + query_terms[i][0] + '/' + query_terms[i][1] + '/' + query_terms[i][2] + '.json'): continue
        # load database with opitmization
        if optimize: index=load_json(path + '/dict_tree/' + query_terms[i][0] + '/' + query_terms[i][1] + '/' + query_terms[i][2] + '.json')

        for term_idx in index:
            # term found.
            if term_idx[0] == query_terms[i]:
                docs=term_idx[1]
                df=len(docs)
                query_tf_idf[i]=cal_tf_idf(1,df)

                for (key, val) in docs.items():
                    doc_name=key
                    tf=val['tf']
                    tf_idf=val['tf-idf']
                    if not doc_name in measure_docs:
                        measure_docs[doc_name]={}
                        measure_docs[doc_name]['tf-idf']=np.zeros(len_query)
                    measure_docs[doc_name]['tf-idf'][i]=tf_idf
                break
   
    # calculate scores
    scores={}
    for doc in measure_docs:
    	norm_doc=np.sqrt(sum(measure_docs[doc_name]['tf-idf'] ** 2))
    	norm_q=np.sqrt(sum(query_tf_idf ** 2))
    	vector_doc=measure_docs[doc]['tf-idf']
    	vector_q=query_tf_idf
    	n_vector_doc=vector_doc
    	n_vector_q=vector_q
    	if norm_doc != 0: n_vector_doc/=norm_doc
        if norm_q != 0: n_vector_q/=norm_q

        scores[doc]={}
        scores[doc]['ncos_sim']=cosin_similariy(n_vector_doc, n_vector_q) # Normalized cosine similarity
        scores[doc]['cos_sim']=cosin_similariy(vector_doc, vector_q) # Non-normailzed cosine similarity
        #scores[doc]['jacc']=len_query/doc_info[doc] # Calculate Jaccard coefficient
        scores[doc]['jacc']=len_query/doc_info[doc]["words"]

    # sorted by cosine sinilarity. 
    result=sorted(scores.iteritems(), cmp=compare_func)

    # get the best results.
    result=result[:int(top_num)]

    # sort the best results based on Jaccard coefficient.
    result=sorted(result, key=lambda f : -f[1]['jacc'])
    
    urls=[]
    
    
    for doc in result:
        urls.append((doc_info[doc[0]]["title"], bookkeeping[doc[0]]))
    return urls

'''
res=search("C:/Github/CS-221-project3-search-engine/database", "artifical intelligence", 10)
for r in res: 
    print r
'''

'''
global path
#path=sys.argv[1]
path="C:/Github/CS-221-project3-search-engine/database"
'''

'''
res=search("computer science", 10)
for r in res:
	print r
'''

'''
with open('query_result', 'w') as r:
    query=["Informatics", "Mondego", "Irvine", "artificial intelligence", "computer science"]

    for q in query:
        start=time.time()
        res= search(q, 10, optimize=True)
        end=time.time()
        print>> r, "optimized search time: %d" %(end-start)
        
        start=time.time()
        res= search(q, 10, optimize=False)
        end=time.time()
        print>> r, "non-optimized search time: %d" %(end-start)

        print>> r, "\n"
'''
