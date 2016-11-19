"""
	This script detects events
"""
from nltk.corpus import stopwords
import Util as util
import re
import Constants as constants
import nltk
#from nltk.probability import ConditionalFreqDist
from nltk.tokenize import word_tokenize


TAG = 'Code/scripts/events :'
stopLex=''

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
	#return [item for item in words if item not in stopLex]
	return text
	
def detectEvents(freq, threshold):
	print(TAG, "STARTING - detectEvents ")
	#{word: [(date1, count1, date2, count2, %change), (date1, count1, date2, count2, %change), ...], ...}
	event={} 
	for word, dateDict in freq.items():
		sortDateList=sorted(dateDict)
		for i in range(len(sortDateList)-1):
			change = percentchange(dateDict[sortDateList[i]], dateDict[sortDateList[i+1]], threshold)
			if change != 0:
				if word in event:
					event[word].append((sortDateList[i], dateDict[sortDateList[i]], sortDateList[i+1], dateDict[sortDateList[i+1]], change))
				else:
					event[word] = [(sortDateList[i], dateDict[sortDateList[i]], sortDateList[i+1], dateDict[sortDateList[i+1]], change)]
	print(TAG, "COMPLETED - detectEvents ", event)
	return event

def percentchange(value1, value2, threshold):
	change=((value2-value1)/value1)*100
	if abs(change) >= threshold:
		return change
	else:
		return 0


def mean(values):
	return sum(values) / max(len(values), 1)
def metrics(newvalue):
	valuelist=[]
	valuelist.append(newvalue)
	obj={'valuelist': valuelist, 
	'sum': sum(valuelist), 
	'count': len(valuelist), 
	'mean': mean(valuelist), 
	'median': median(valuelist), 
	'max': max(valuelist)}
	return obj

def run2(params):
	print(TAG, "STARTING - wordcount ")

	stopLex=load()
	print(TAG, "Successful: Stop Lex loaded ")
	
	#Load and Convert JSON to Py
	fdist = FreqDist(word for word in word_tokenize("hello world's. how r u doing today? is everything u do great? nah!! my name is mehul, i am mehul gupta") if word not in stopLex)
	print(fdist.most_common(50))

	"""
	print(TAG, "Load Reviews and Convert JSON to Python")
	reviews = util.loadConvertJSONPy(constants.FileNames['review'])
	print(TAG, "Successful: Reviews Loaded")
	

	#stopLex=load()
	print(TAG, "Successful: Stop Lex loaded ")

	print(TAG, "Computing Word Count")
	freq={} #{word: {date:count, date2:count2, ..., metrics:{sum:, count:, mean:, median:, max:, valuelist:[]}}, ...}

	
	print(reviews[0]['text'])
	fdist = FreqDist(word for word in word_tokenize(reviews[0]['text']))
	print(fdist.most_common(50))
	

	for review in reviews:
		words=perprocessedText(review['text'], stopLex)
		date=util.bucketedDate(review['date'], params['bucket'])
		for word in words:
			if word not in stopLex:		
				if word in freq:
					if date in freq[word]:
						freq[word][date]+=1
					else:
						freq[word][date]=1
				else:
					freq[word]={date:1}
				#freq[word][metrics]=metrics(word)
	"""
	print(TAG, "COMPLETED - wordcount")
	#print(freq)
	#detectEvents(freq, params['eventthreshold'])


def run(params):
	print(TAG, "STARTING - wordcount ")

	print(TAG, "Load Reviews and Convert JSON to Python")
	reviews = util.loadConvertJSONPy(constants.FileNames['review'])
	print(TAG, "Successful: Reviews Loaded")

	print(TAG, "loading Stop-Lex ")
	stopLex=load()
	print(TAG, "Successful: Stop Lex loaded ")

	bucketedReviews={}	#{bucket: 'Text', bucket2:'', ...}
	wordcountFreq={}	#{bucket: nltk.FreqDist, bucket2: nltk.FreqDist, ...}

	print(TAG, "Bucketing Reviews ...")
	i=0
	for review in reviews:
		reviewDate=review['date']
		if params['eventstartbucket']<=reviewDate<=params['eventendbucket']:
			bucket=util.bucketedDate(reviewDate, params['bucket'])
			i+=1
			print(i, bucket)
			texts=perprocessedText(review['text'])
			if bucket in bucketedReviews:
				bucketedReviews[bucket]=bucketedReviews[bucket]+" "+texts
			else:
				bucketedReviews[bucket]=texts
	print(TAG, "Successful: Reviews Buckted")

	print(TAG, "Computing FreqDist using nltk")
	for B,T in bucketedReviews.items():
		fdist = nltk.FreqDist(word for word in word_tokenize(T) if word not in stopLex)
		wordcountFreq[B]=fdist

	print(TAG, "Successful: FreqDist completed")
	print(wordcountFreq)
	"""
	print(TAG, "Load Reviews and Convert JSON to Python")
	reviews = util.loadConvertJSONPy(constants.FileNames['review'])
	print(TAG, "Successful: Reviews Loaded")
	

	#stopLex=load()
	print(TAG, "Successful: Stop Lex loaded ")

	print(TAG, "Computing Word Count")
	freq={} #{word: {date:count, date2:count2, ..., metrics:{sum:, count:, mean:, median:, max:, valuelist:[]}}, ...}

	
	print(reviews[0]['text'])
	fdist = FreqDist(word for word in word_tokenize(reviews[0]['text']))
	print(fdist.most_common(50))
	

	for review in reviews:
		words=perprocessedText(review['text'], stopLex)
		date=util.bucketedDate(review['date'], params['bucket'])
		for word in words:
			if word not in stopLex:		
				if word in freq:
					if date in freq[word]:
						freq[word][date]+=1
					else:
						freq[word][date]=1
				else:
					freq[word]={date:1}
				#freq[word][metrics]=metrics(word)
	"""
	print(TAG, "COMPLETED - wordcount")
	#print(freq)
	#detectEvents(freq, params['eventthreshold'])


