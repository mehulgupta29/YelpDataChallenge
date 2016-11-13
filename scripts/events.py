"""
	This script detects events
"""
from nltk.corpus import stopwords
import util
import re
import constants

TAG = 'Code/scripts/events :'
stopLex=''

def load():
	posLex=loadLexicon(constants.FileNames['positive-words'])
	negLex=loadLexicon(constants.FileNames['negative-words'])
	stopLex=set(stopwords.words('english')+list(posLex)+list(negLex))

def loadLexicon(fname):
	newLex=set()
	lex_conn=open(fname)
	#add every word in the file to the set
	for line in lex_conn:
		newLex.add(line.strip())# remember to strip to remove the lin-change character
	lex_conn.close()
	return newLex

def perprocessedText(text, stopLex):
	"""
	pre-process the text and return a list of unique words. also remove stopwords, positive lex and negative lex
	"""
	text=re.sub('[^a-zA-Z]', ' ', text)
	text = re.sub(' +', ' ', text)
	words=text.lower().strip().split(' ')
	return [item for item in words if item not in stopLex]
	
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

def run(reviews, bucket):
	print(TAG, "STARTING - wordcount ")
	posLex=loadLexicon(constants.FileNames['positive-words'])
	negLex=loadLexicon(constants.FileNames['negative-words'])
	comLex=loadLexicon(constants.FileNames['common-words'])
	stopLex=set(stopwords.words('english')+list(posLex)+list(negLex)+list(comLex))

	freq={} #{word: {date:count, date2:count2, ..., metrics:{sum:, count:, mean:, median:, max:, valuelist:[]}}, ...}
	for review in reviews:
		words=perprocessedText(review['text'], stopLex)
		date=util.bucketedDate(review['date'], bucket)
		for word in words:			
			if word in freq:
				if date in freq[word]:
					freq[word][date]+=1
				else:
					freq[word][date]=1
			else:
				freq[word]={date:1}
			#freq[word][metrics]=metrics(word)
	print(TAG, "COMPLETED - wordcount")
	#print(freq)
	detectEvents(freq, 100)
