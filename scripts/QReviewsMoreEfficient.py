import Util as util
import Constants as constants
import json
import nltk
from nltk.corpus import stopwords
import re
from nltk.tokenize import word_tokenize

TAG = 'Code/scripts/QReviewsMoreEfficient :'

def loadLexicon(fname):
	newLex=set()
	lex_conn=open(fname)
	#add every word in the file to the set
	for line in lex_conn:
		newLex.add(line.strip())# remember to strip to remove the lin-change character
	lex_conn.close()
	return newLex

def load():
	
	posLex=loadLexicon(constants.FileNames['positive-words'])
	negLex=loadLexicon(constants.FileNames['negative-words'])
	comLex=loadLexicon(constants.FileNames['common-words'])
	stopLex=set(stopwords.words('english')+stopwords.words('spanish')+stopwords.words('portuguese')+stopwords.words('french')+stopwords.words('german')+list(posLex)+list(negLex))
	return stopLex

def percentchange(wd1, wd2, threshold):
	"""
	inputs:
		wd1/wd2:{word:count, word2:count, ..}
		threshold: Float
	output:
		diff={word: %change, word2: %change,...}
	"""
	diff={}
	commonwords=set(wd1) & set(wd2)
	for cword in commonwords:
		v1=wd1[cword]
		v2=wd2[cword]

		change=((v2-v1)/v1)*100
		if abs(change) >= threshold:
			diff[cword]=diff.get(cword, 0)+change
	return diff

def detectEvents(freq, threshold):
	"""
	inputs:
		freq={bucket:{word:count, word2:count, ..}, bucket2:{...}, ...}
	vars:
		percentchange()={word: %, word2:%,...}
	output:
		event={bucket:{word:%, word2: %, ...}, bucket2:{word:%,...}, ...}
	"""
	print(TAG, "STARTING - detectEvents ")

	event={}
	sortedBucketList=sorted(freq.keys())
	for i in range(len(sortedBucketList)-1):
		#print(i, sortedBucketList[i], sortedBucketList[i+1], threshold)
		event[sortedBucketList[i]]=percentchange(freq[sortedBucketList[i]], freq[sortedBucketList[i+1]], threshold)
	print(TAG, "COMPLETED - detectEvents ")
	return event

def run(params):
	print(TAG, 'Running EVENTS')

	print(TAG, 'Loading PreProcessed JSON Reviews file - review-bucket-quarter-freqdist')
	#{bucket: nltk.FreqDist, bucket2:nltk.FreqDist, ...}
	bucketedReviews=util.loadConvertJSONPy(constants.FileNames['review-bucket-quarter-freqdist'])
	bucketedReviews=bucketedReviews[0]
	print(TAG, 'JSON to PY converted')
	
	print(TAG, 'Detecting Events: Analysing word freq distribution and finding patterns')
	events=detectEvents(bucketedReviews, params['eventthreshold'])
	print(TAG, 'Events Detected')

	return events

	#print(TAG, 'Printing events for bucket : 2016-Quarter2 till 2016-Quarter3\n',events['2016-Q2']) 
	#output: events['2016-Q2']:{'wahlburgers': 2300.0, 'underpriced': 300.0, 'macdonald': 300.0, 'kanoa': 350.0, 'barbocoa': 400.0, 'chomped': 500.0, 'merts': 300.0, 'pokemon': 1100.0, 'kleinfeld': 500.0, 'mylene': 350.0, 'stoppage': 300.0, 'linea': 300.0, 'afc': 300.0, 'squeegee': 400.0, 'bharta': 400.0, 'naseem': 300.0, 'tuner': 600.0, 'mvah': 300.0, 'awrs': 500.0, 'tatami': 300.0, 'wahlburger': 300.0, 'nama': 500.0, 'jul': 700.0, 'asbestos': 300.0, 'honneur': 300.0, 'hasbrown': 300.0, 'bebop': 300.0, 'obstructions': 300.0, 'appie': 400.0, 'kerosene': 300.0, 'telefono': 400.0, 'urology': 300.0, 'rhett': 300.0, 'july': 336.318407960199, 'cks': 300.0, 'caliper': 800.0, 'fufu': 300.0, 'athena': 500.0, 'oxford': 300.0, 'ivc': 300.0, 'takamatsu': 300.0, 'pizio': 300.0, 'estava': 500.0, 'mortimer': 300.0, 'burma': 500.0, 'bodyflo': 500.0, 'firenze': 300.0, 'kavsar': 300.0, 'huger': 400.0, 'ary': 300.0, 'jaenica': 700.0, 'luxxi': 300.0, 'complexe': 300.0, 'skywater': 600.0, 'bbh': 400.0, 'weidner': 500.0, 'lockmaster': 300.0, 'collier': 400.0, 'brinks': 300.0, 'presotea': 500.0, 'tract': 300.0, 'unpleased': 300.0, 'freshbox': 300.0, 'jatoba': 300.0, 'ppm': 600.0, 'greedily': 300.0, 'fucker': 300.0, 'uzbek': 300.0, 'rewired': 300.0, 'madeleine': 400.0, 'compadres': 300.0, 'peanutbutter': 400.0, 'pandamonium': 300.0, 'andarra': 600.0, 'choripan': 300.0, 'mutt': 800.0, 'eddies': 300.0, 'lc': 300.0}

def exportAsCSV(headerlist, datalist, fname):
	util.exportAsCSV(headerlist, datalist, fname)


if __name__ == "__main__":

	"""
	print(TAG, "STARTING PART-5...")


	#Part-5
	print('Loading JSON ..')
	#{bucket: nltk.FreqDist, bucket2:nltk.FreqDist, ...}
	bucketedReviews=util.loadConvertJSONPy(constants.FileNames['review-bucket-quarter-freqdist'])
	bucketedReviews=bucketedReviews[0]
	print('JSON to PY converted')
	#print(bucketedReviews['2015-Q4'])
	events=detectEvents(bucketedReviews, 300)
	print(events['2016-Q2']) 
	#output: events['2016-Q2']:{'wahlburgers': 2300.0, 'underpriced': 300.0, 'macdonald': 300.0, 'kanoa': 350.0, 'barbocoa': 400.0, 'chomped': 500.0, 'merts': 300.0, 'pokemon': 1100.0, 'kleinfeld': 500.0, 'mylene': 350.0, 'stoppage': 300.0, 'linea': 300.0, 'afc': 300.0, 'squeegee': 400.0, 'bharta': 400.0, 'naseem': 300.0, 'tuner': 600.0, 'mvah': 300.0, 'awrs': 500.0, 'tatami': 300.0, 'wahlburger': 300.0, 'nama': 500.0, 'jul': 700.0, 'asbestos': 300.0, 'honneur': 300.0, 'hasbrown': 300.0, 'bebop': 300.0, 'obstructions': 300.0, 'appie': 400.0, 'kerosene': 300.0, 'telefono': 400.0, 'urology': 300.0, 'rhett': 300.0, 'july': 336.318407960199, 'cks': 300.0, 'caliper': 800.0, 'fufu': 300.0, 'athena': 500.0, 'oxford': 300.0, 'ivc': 300.0, 'takamatsu': 300.0, 'pizio': 300.0, 'estava': 500.0, 'mortimer': 300.0, 'burma': 500.0, 'bodyflo': 500.0, 'firenze': 300.0, 'kavsar': 300.0, 'huger': 400.0, 'ary': 300.0, 'jaenica': 700.0, 'luxxi': 300.0, 'complexe': 300.0, 'skywater': 600.0, 'bbh': 400.0, 'weidner': 500.0, 'lockmaster': 300.0, 'collier': 400.0, 'brinks': 300.0, 'presotea': 500.0, 'tract': 300.0, 'unpleased': 300.0, 'freshbox': 300.0, 'jatoba': 300.0, 'ppm': 600.0, 'greedily': 300.0, 'fucker': 300.0, 'uzbek': 300.0, 'rewired': 300.0, 'madeleine': 400.0, 'compadres': 300.0, 'peanutbutter': 400.0, 'pandamonium': 300.0, 'andarra': 600.0, 'choripan': 300.0, 'mutt': 800.0, 'eddies': 300.0, 'lc': 300.0}

	
	#Part-4.1
	bucketedReviews={} #{bucket: nltk.FreqDist, bucket2:nltk.FreqDist, ...}
	file=open(constants.FileNames['review-bucket-quarter-wordlistformat'])
	for jsonText in file:
		print('Loading JSON ..')
		jsonToPy=json.loads(jsonText)
		print('JSON to PY converted')
		for bucket, words in jsonToPy.items():
			print(bucket)
			freq=nltk.FreqDist(words)
			if bucket in bucketedReviews:
				print('ERROR - There should not be multiple keys with same name')
			else:
				bucketedReviews[bucket]=freq
	file.close()

	print(bucketedReviews['2016-Q1'])
	f=bucketedReviews['2016-Q1']
	print(f.N(), f.most_common(5))
	
	
	#Part-4
	bucketedReviews={} #{bucket: nltk.FreqDist, bucket2:nltk.FreqDist, ...}
	i=0
	file=open(constants.FileNames['review-bucket-quarter-worldwordlistformat'])
	for jsonText in file:
		print('Loading JSON ..')
		jsonToPy=json.loads(jsonText)
		print('JSON to PY converted')
		for bucket, words in jsonToPy.items():
			i+=1
			print(i,bucket)
			freq=nltk.FreqDist(words)
			if bucket in bucketedReviews:
				print('ERROR - There should not be multiple keys with same name')
			else:
				bucketedReviews[bucket]=freq
	file.close()

	print(TAG, "Converting Python to JSON")
	js=util.convertPyJson(bucketedReviews)

	print(TAG, "Writing to file: reviews-bucket-quarter-freqdist.json")
	fw=open('reviews-bucket-quarter-freqdist.json', 'w+')
	fw.write(js)
	print(TAG, "Wrtiting completed --x--x--x--x--")

	fw.close()

	print(bucketedReviews['2016-Q2'])
	f=bucketedReviews['2016-Q2']
	print(f.most_common(50))
	
	
	#Part-3
	bucketedReviews={} #{bucket: [words], bucket2:[], ...}

	print('Loading StopLex .')
	stopLex=load()
	i=0
	file=open(constants.FileNames['review-bucket-quarter-stringformat'])
	for jsonText in file:
		print('Loading JSON ..')
		jsonToPy=json.loads(jsonText)
		print('JSON to PY converted')
		for bucket, text in jsonToPy.items():
			i+=1
			print(i,bucket)
			words=[word.lower() for word in word_tokenize(text) if word.lower() not in stopLex]
			if bucket in bucketedReviews:
				bucketedReviews[bucket]=bucketedReviews[bucket]+words
			else:
				bucketedReviews[bucket]=words
	file.close()

	print(TAG, "Converting Python to JSON")
	js=util.convertPyJson(bucketedReviews)

	print(TAG, "Writing to file: reviews-bucket-quarter-worldwordlistformat.json")
	fw=open('reviews-bucket-quarter-worldwordlistformat.json', 'w+')
	fw.write(js)
	print(TAG, "Wrtiting completed --x--x--x--x--")

	fw.close()
	

	#Part-2
	bucketedReviews={} #{bucket: 'Text', bucket2:'', ...}
	file=open(constants.FileNames['review-bucket-quarter'])
	for jsonText in file:
		print('Loading JSON ..')
		jsonToPy=json.loads(jsonText)
		print('JSON to PY converted')
		for bucket, textlist in jsonToPy.items():
			print(bucket)

			text=' '.join(textlist)
			text=re.sub('[^a-zA-Z]', ' ', text)
			text=re.sub(' +', ' ', text)

			if bucket in bucketedReviews:
				bucketedReviews[bucket]=bucketedReviews[bucket]+text
			else:
				bucketedReviews[bucket]=text
	file.close()

	print(TAG, "Converting Python to JSON")
	js=util.convertPyJson(bucketedReviews)

	print(TAG, "Writing to file - reviews-quarter.json")
	fw=open('reviews-bucket-quarter-stringformat.json', 'w+')
	fw.write(js)
	print(TAG, "Wrtiting completed --x--x--x--x--")

	fw.close()


	#Part-1
	bucketedReviews={} #{bucket: [Text], bucket2:[], ...}
	ctr=0

	file=open(constants.FileNames['review'])
	for jsonText in file:
		jsonToPy=json.loads(jsonText)
		date=jsonToPy['date']
		text=jsonToPy['text']
		bucket=util.bucketedDate(date, 'quarter')

		if bucket in bucketedReviews:
			bucketedReviews[bucket].append(text)
		else:
			bucketedReviews[bucket]=[text]
		if ctr/25000:
			print(ctr, bucket)

	file.close()

	print(TAG, "Converting Python to JSON")
	js=util.convertPyJson(bucketedReviews)

	print(TAG, "Writing to file - reviews-quarter.json")
	fw=open('reviews-bucket-quarter.json', 'w+')
	fw.write(js)
	print(TAG, "Wrtiting completed --x--x--x--x--")

	fw.close()
	"""
