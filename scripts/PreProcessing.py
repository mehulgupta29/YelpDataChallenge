"""
Pre-process the text
"""
import Constants as const
from nltk.corpus import stopwords
import re

TAG = 'Code/scripts/PreProcessing :'

def loadLexicon(fname):
	"""
		read from a file and return a set of lexicons
	"""
	newLex=set()
	lex_conn=open(fname)
	#add every word in the file to the set
	for line in lex_conn:
		newLex.add(line.strip())# remember to strip to remove the lin-change character
	lex_conn.close()
	return newLex

def loadWordFiles():
	"""
		loads multiple lexicons and returns a list of all lexicons in lowercase
	"""
	posLex=loadLexicon(const.FileNames['positive-words'])
	negLex=loadLexicon(const.FileNames['negative-words'])
	comLex=loadLexicon(const.FileNames['common-words'])
	stopLex=set(stopwords.words('english')+list(posLex)+list(negLex)+list(comLex))
	return stopLex

def formatText(text):
	"""
		pre-process the text. also remove stopwords, positive lex, negative lex and common words lexicon
	"""
	text=re.sub('[^a-zA-Z]', ' ', text)
	text=re.sub(' +', ' ', text)
	words=text.lower().strip().split(' ')
	words=[item for item in words if item not in stopLex]
	return ' '.join(words)

def formatReviews2(reviews):
	"""
		reads inputted reviews list and formats the text and returns a dict with only required information from the reviews
	"""
	print(TAG, "formatReviews()")
	stopLex=loadWordFiles()
	res=[]
	for review in reviews:
		res.append({'bid': review['business_id'], 'date': review['date'], 'text': formatText(review['text'], stopLex), 'stars': review['stars']})
	return res

def formatReviews(reviews):
	"""
		reads inputted reviews list and formats the text and returns a dict with only required information from the reviews
	"""
	print(TAG, "formatReviews()")
	res=[]
	for review in reviews:
		res.append({'bid': review['business_id'], 'date': review['date'], 'text': review['text'], 'stars': review['stars']})
	return res

stopLex=loadWordFiles()
