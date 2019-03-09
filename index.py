import sys
import os
import time
import re
import json
import math

from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords

from bs4 import BeautifulSoup, Comment
from urlparse import urljoin

def load_json(file):
    with open(file) as f:
        return json.load(f)

def process():
    print "Start processing !"
    global path
    global doc_num
    global max_tfidf
    global min_tfidf
    global doc_info

    doc_num=0 # Record the documents processed.
    max_tfidf=0
    min_tfidf=sys.maxsize

    term_idx={} # Record the term and it's property.
    doc_info={} # Record number of unique words and title for each document

    index_file = load_json(path+"/WEBPAGES_RAW/bookkeeping.json")

    #75 folders in total
    num_folders=75
    num_files=500
    for i in range(num_folders):
        for j in range(num_files):
            f_path=path+"/WEBPAGES_RAW/{}/{}".format(i,j)
            if not os.path.isfile(f_path): continue # File doesn't exist
            doc_id="{}/{}".format(i,j)
            #doc_info[doc_id]=0
            doc_info[doc_id]={"words":0, "title" : "N/A"}

            with open(f_path) as f:
                # Porcess the html web page.
                page=BeautifulSoup(f.read(),"lxml")

                # Skip the file that doesn't have head and body tag.
                if page.head is None and page.body is None:
                    print "Incomplete file:{}".format(doc_id)
                    continue

                print "process file: {}".format(f_path)
                doc_num+=1
                
                # record page title.
                if page.title and page.title.string:
                    #print page.title.string
                    doc_info[doc_id]["title"]=page.title.string.strip()

                # process head tag.
                if page.head is not None:
                    text = page.head.findAll(text=True)
                    relev = filter(relev_func, text)
                    terms = process_term(relev)
                    for term in terms:
                        if term not in term_idx:
                            term_idx[term]={}
                        if doc_id not in term_idx[term]:
                            term_idx[term][doc_id]={'tf': 0, 'tf-idf': 0, 'urls': 0}
                        term_idx[term][doc_id]['tf']+=1
                        #doc_info[doc_id]+=1
                        doc_info[doc_id]["words"]+=1

                
                # process body tag.
                if page.body is not None:
                    text = page.body.findAll(text=True)
                    relev = filter(relev_func, text)
                    terms = process_term(relev)
                    for term in terms:
                        if term not in term_idx:
                            term_idx[term]={}
                        if doc_id not in term_idx[term]:
                            term_idx[term][doc_id]={'tf': 0, 'tf-idf': 0, 'urls': 0}
                        term_idx[term][doc_id]['tf']+=1
                        #doc_info[doc_id]+=1
                        doc_info[doc_id]["words"]+=1

                # process urls in this page.
                '''
                in_url = index_file[doc_id]
                urls = []
                urls.append(in_url)

                out_urls=page.findAll('a')

                for out_url in out_urls:
                    url=out_url.get('href')
                    url = urljoin(in_url, url)
                    urls.append(url)

                url_terms=process_term(urls)
                for term in url_terms:
                    if term not in term_idx:
                        term_idx[term]={}
                    if doc_id not in term_idx[term]:
                        term_idx[term][doc_id]={'tf': 0, 'tf-idf': 0, 'urls': 0}
                    term_idx[term][doc_id]['urls']+=1 # Count the number of urls in this page.
                    #doc_info[doc_id]+=1
                    doc_info[doc_id]["words"]+=1
                '''
    
    # Calcuate tf-idf
    for term in term_idx:
        df = len(term_idx[term])
        for doc in term_idx[term]:
            tf = term_idx[term][doc]['tf']
            term_idx[term][doc]['tf-idf']=cal_tf_idf(tf, df)
            if term_idx[term][doc]['tf-idf'] > max_tfidf: max_tfidf=term_idx[term][doc]['tf-idf']
            if term_idx[term][doc]['tf-idf'] < min_tfidf: min_tfidf=term_idx[term][doc]['tf-idf']
    return term_idx


def cal_tf_idf(tf, df):
    global doc_num
    if tf == 0 or df == 0: return 0
    return (1+math.log10(tf))*(math.log10(doc_num/df))

def relev_func(data):
    irrev={'style', 'script', 'meta'} #[document]
    if data.parent.name in irrev: return False
    return True

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
    return res

# check whether the directory exists
def check_dir(path):
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except OSEroor as exc:
            if exc.errno != errno.EEXIST: raise

def save_result(term_dict, build_time, dict_time, dict_tr_time):
    global doc_num
    global max_tfidf
    global min_tfidf

    with open('result', 'w') as r:
        print>> r, "number of processed documents:", doc_num, "\n"
        print>> r, "number of unique words:", len(term_dict), "\n"
        print>> r, "max tf-idf:", max_tfidf, "\n"
        print>> r, "min tf-idf", min_tfidf, "\n"
        print>> r, "Time for building dictionary:", build_time, "\n"
        print>> r, "Time for saving dictionary:", dict_time, "\n"
        print>> r, "Time for saving dictionary tree:", dict_tr_time, "\n"

def save_dict(term_list):
    print "Save dictionary !"

    # Save all the terms into a json file
    cur=[]
    for term in term_list:
        cur.append(term)

    f_path=path+'/dict/index.json'
    check_dir(f_path)
    with open(f_path, 'w') as outfile:
        outfile.write(json.dumps(cur))
    

def save_dict_tree(term_list):
    global path

    print "Save dictionary tree !"

    idx="___"
    sub_res=[]
    for term in term_list:
        # Collect the items that are longer than 2
        if len(term[0]) > 2:
            #Encounter a different term
            if (term[0][0]+term[0][1]+term[0][2]) != idx:
                #Output sub_res
                if len(sub_res) > 0:
                    f_path=path+'/dict_tree/'+idx[0]+'/'+idx[1]+'/'+idx[2]+'.json'
                    check_dir(f_path)
                    with open(f_path, 'w') as outfile:
                        outfile.write(json.dumps(sub_res))
                idx=term[0][0]+term[0][1]+term[0][2]
                sub_res=[]
            sub_res.append(term)
    
    #add last term
    if len(sub_res) > 0:
        f_path=path+'/dict_tree/'+idx[0]+'/'+idx[1]+'/'+idx[2]+'.json'
        check_dir(f_path)
        with open(f_path, 'w') as outfile:
            outfile.write(json.dumps(sub_res))

def save_doc_info():
    print "Save doc info !"
    f_path=path+'/doc/doc.json'
    check_dir(f_path)
    with open(f_path, 'w') as outfile:
        outfile.write(json.dumps(doc_info))

global path
path=sys.argv[1]
#path="C:/Github/CS-221-project3-search-engine/database"

start=time.time()
term_dict=process()
end=time.time()
build_time=end-start
print "Time for building the dictionary: %2.f seconds." %(build_time)

term_list=sorted(term_dict.iteritems(), key=lambda f : f[0])

start=time.time()
save_dict(term_list)
end=time.time()
dict_time=end-start
print "Time for saving the dictionary: %2.f seconds." %(dict_time)

start=time.time()
save_dict_tree(term_list)
end=time.time()
dict_tr_time=end-start
print "Time for saving the dictionary tree: %2.f seconds." %(dict_tr_time)

save_result(term_dict, build_time, dict_time, dict_tr_time)
save_doc_info()