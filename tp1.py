try :
	import cpickle as pickle
except :
	import pickle
import string
from collections import defaultdict
import timeit
import re
from math import log10

def open_file(number):
	file = open(r'C:\Users\ASUS X541U\Documents\TP RI\collections\d'+str(number)+'.txt','r',encoding='latin-1')
	for f in file.readlines():
		print(f)
	file.close()

def create_stop():
	stop = {}
	file = open(r'C:\Users\ASUS X541U\Documents\TP RI\stopwords_fr.txt','r',encoding='utf-8')
	for f in file.readlines():
			stop[f.replace('\n','')]=1
	file.close()
	file = open('stop.pkl', 'wb')
	pickle.dump(stop,file)
	file.close()

def preprocess(i):
	file = open(r'..\collections\d'+str(i)+'.txt','r',encoding='latin-1')
	sentence = file.read().lower().replace(r"\n", " ")
	sentence = re.sub(r"[\/()&~£{}%_:+*\"\]\[,.;@#?!&$«»]|[1-9]+\ *", " ", sentence)
	return re.split(r'\s+', sentence) # split if encounters 1 space or more

def create_index(number):
	create_stop()
	file = open('stop.pkl', 'rb')
	stop = pickle.load(file)
	file.close()
	#inverse=defaultdict(lambda : defaultdict(int))
	inverse={}
	col={}
	for i in range(0,3):
		doc = 'd'+str(i)
		col[doc]=defaultdict(int)
		for word in preprocess(i): 
			if word not in stop : #  it uses the dictionary's hashing contrarly to using .key()
				col[doc][word]+=1
				if word in inverse.keys():
					if doc not in inverse[word].keys():
						inverse[word][doc]+=1
				else:
					inverse[word]=defaultdict(int)
					inverse[word][doc]+=1


	file = open('structure.pkl', 'wb')
	pickle.dump(col,file)
	file.close()
	return col

def get_index():
	file = open('structure.pkl', 'rb')
	st = pickle.load(file)
	file.close()
	return st



def inverse_index():
	start = timeit.timeit()
	inversed = {}
	index=create_index(370)
	for doc in index.keys():
		for word in index[doc].keys():
			inversed[word]=defaultdict(int)
			for d in index.keys():
				if d != doc:
					inversed[word][d]+=0
			inversed[word][doc]+=1

	file = open('inverse.pkl', 'wb')
	pickle.dump(inversed,file)
	file.close()
	return inversed
			
	end = timeit.timeit()
	print(end - start)

def get_inverse():
	file = open('inverse.pkl', 'rb')
	st = pickle.load(file)
	file.close()
	return st

def requetebydocument(document):
	index = get_index()
	document=document-1
	print("Liste des termes du document d"+str(document))
	for word in index['d'+str(document)].keys():
		print(word,'frequence :'+str(index['d'+str(document)][word]))


def requetebyterme(terme):
	terme=terme.lower()
	number=0
	index_inverse=inverse_index()
	#print(index_inverse[terme].keys())
	#print('Terme : '+terme)
	for wdoc in index_inverse[terme].keys():
		print('Document:'+wdoc+' Frequence du terme '+terme+':'+str(index_inverse[terme][wdoc]))
		if index_inverse[terme][wdoc] == 1:
			number+=1
	return number

def weighted_index(number):
	index = get_index()
	inverse = get_inverse()
	weighted_index = {}
	for word in inverse.keys():
		for doc in inverse[word].keys():
			weighted_index[word]=defaultdict(int)
			freq = inverse[word][doc]
			if freq == 0:
				weighted_index[word][doc]+=0
			else :
				max_doc = max(list(index[doc].keys()), key=(lambda key: index[doc][word])) # retourne la clé selon le critere(key) le max (s[key])
				doc_number = requetebyterme(word)
				weighted_index[word][doc]+=(freq/(float(index[doc][max_doc])*log10((number/doc_number)+1))) #poids(ti, dj)=(freq(ti,dj)/Max(freq(t, dj))*Log((N/ni) +1)
				print(weighted_index[word][doc])

create_index(370)
#inverse_index()
#requetebydocument(2)
#requetebyterme('logiciel')
#weighted_index(370)

