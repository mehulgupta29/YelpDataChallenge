from nltk.corpus import stopwords
import Util as util
import re
import Constants as constants
import nltk
from nltk.tokenize import word_tokenize


TAG = 'Code/scripts/QReviews :'

def load():
	
	posLex=loadLexicon(constants.FileNames['positive-words'])
	negLex=loadLexicon(constants.FileNames['negative-words'])
	comLex=loadLexicon(constants.FileNames['common-words'])
	stopLex=set(stopwords.words('english')+list(posLex)+list(negLex))
	return stopLex

def loadLexicon(fname):
	newLex=set()
	lex_conn=open(fname)
	#add every word in the file to the set
	for line in lex_conn:
		newLex.add(line.strip())# remember to strip to remove the lin-change character
	lex_conn.close()
	return newLex

def perprocessedText(text):
	"""
	pre-process the text and return a list of unique words. also remove stopwords, positive lex and negative lex
	"""
	text=re.sub('[^a-zA-Z]', ' ', text)
	text = re.sub(' +', ' ', text)
	#words=text.lower().strip().split(' ')
	#words = [item for item in words if item not in stopLex]
	#ftext=' '.join(words)
	return text 

if __name__ == "__main__":

	print(TAG, "Load Reviews and Convert JSON to Python")
	reviews = util.loadConvertJSONPy(constants.FileNames['review'])
	print(TAG, "Successful: Reviews Loaded")

	#print(TAG, "loading Stop-Lex ")
	#stopLex=load()
	#print(TAG, "Successful: Stop Lex loaded -> bucketing ....")

	bucketedReviews={}	#{bucket: 'Text', bucket2:'', ...}

	#2,685,066 reviews total
	for review in reviews:
		reviewDate=review['date']
		bucket=util.bucketedDate(reviewDate, 'quarter')
		texts=perprocessedText(review['text'])

		if bucket in bucketedReviews:
			bucketedReviews[bucket]=bucketedReviews[bucket]+" "+texts
			print(bucket)
		else:
			bucketedReviews[bucket]=texts

	print(TAG, "Converting Python to JSON")
	js=util.convertPyJson(bucketedReviews)

	print(TAG, "Writing to file - reviews-quarter.json")
	fw=open('reviews-quarter.json', 'w+')
	fw.write(js)
	print(TAG, "Wrtiting completed --x--x--x--x--")

	fw.close()
