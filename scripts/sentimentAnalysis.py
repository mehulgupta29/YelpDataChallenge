"""
	SentimentAnalysis script is used to find the sentiment of a changepoint.
"""

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
import re
from nltk.corpus import stopwords
import Constants as const
import PreProcessing as pp

TAG = 'Code/scripts/SentimentAnalysis :'

def loadData(fname):
	"""
		read the reviews and their polarities from a given file
	"""
	print(TAG,"loadData(): ", fname)
	reviews=[]
	labels=[]
	f=open(fname)
	for line in f:
		review,rating=line.strip().split('\t')
		review = re.sub('<[a-zA-Z]+>', '', review)
		review = re.sub('n\'t', ' not', review)
		review = re.sub('\.+', ' ', review)
		review = re.sub('[^a-zA-Z]', ' ', review)
		review = re.sub(' +', ' ', review)
		reviews.append(review.lower())    
		labels.append(int(rating))
	f.close()
	return reviews,labels
	
def trainClassifier(trainingFname):
	"""
		reads training file, trains classifier and returns counter and classifier
	"""
	print(TAG, "trainClassifier()")
	rev_train,labels_train=loadData(trainingFname)
	counter = CountVectorizer(ngram_range=(1,2), max_df=0.41, min_df=0, strip_accents='unicode')
	counter.fit(rev_train)
	counts_train = counter.transform(rev_train)#transform the training data
	clf = LogisticRegression(solver="lbfgs", max_iter= 10000, multi_class='multinomial', tol=0.00000001, class_weight='balanced')
	clf.fit(counts_train,labels_train)

	return counter,clf

def findAccurayScore(testFname, counter, clf):
	"""
		compute the accuracy score based on the training and test dataset and a classifier
	"""
	print(TAG, "findAccurayScore()")
	rev_test,labels_test=loadData(const.FileNames[testFname])
	counts_test = counter.transform(rev_test)	#transform the testing data
	pred=clf.predict(counts_test)

	return accuracy_score(pred,labels_test)

def findSentimentScore(pred):
	"""
		reads the predictions of the classifier and returns the sentiment score. In the prediction, Negative is 0 and Positive is 1
	"""
	posCount=0
	negCount=0
	for record in pred:
		if record == 0:
			negCount+=1
		else:
			posCount+=1
	posScore=((posCount/len(pred))*100)
	negScore=((negCount/len(pred))*100)

	if posScore >= negScore:
		return posScore
	else:
		return -negScore

def computeSentiment(rev_test, counter, clf):
	"""
		compute the sentiment score based on the training and test dataset and a classifier
	"""
	counts_test = counter.transform(rev_test)	#transform the testing data
	pred=clf.predict(counts_test)

	return findSentimentScore(pred)

def computeConfidenceScore(sentiScore, accuScore):
	"""
		confidence score is the product of sentiment analysis score and accuray score of the classifier
	"""
	return abs(sentiScore)*accuScore

def performSentimentAnalysis(reviews, trainingFname, threshold):
	"""
		For each business, detect the sentiment analysis and confidence score based on reviews
		inputs: 
			reviews = {bid: [{startBucket:, endBucket:, slope:, text: [Tsb+Teb]}, {...}, ...], ...}
			trainingFname = File name of training dataset
			threshold = float - confidence score should be greater than equal to threshold
		output:
			sentianalysis = {bid: [{startBucket:, endBucket:, slope:, text: [Tsb+Teb], sentimentAnalysisScore:, accuracyScore:, confidenceScore:}, {...}, ...], ...}
	"""
	print(TAG, "performSentimentAnalysis()")
	sentianalysis={}
	counter,clf=trainClassifier(trainingFname)
	accuracyScore=findAccurayScore('reviews-test', counter, clf)
	
	for bid, values in reviews.items():
		for cp in values:
			
			texts=[]
			for text in cp['text']:
				texts.append(pp.formatText(text))

			sentiScore=computeSentiment(texts, counter, clf)
			confidenceScore=computeConfidenceScore(sentiScore, accuracyScore)

			if confidenceScore >= threshold:
				if bid in sentianalysis:
					sentianalysis[bid].append({'startBucket': cp['startBucket'], 'endBucket': cp['endBucket'], 'slope': cp['slope'], 'sentimentAnalysisScore': sentiScore, 'accuracyScore': accuracyScore, 'confidenceScore':confidenceScore})
				else:
					sentianalysis[bid]=[{'startBucket': cp['startBucket'], 'endBucket': cp['endBucket'], 'slope': cp['slope'], 'sentimentAnalysisScore': sentiScore, 'accuracyScore': accuracyScore, 'confidenceScore':confidenceScore}]
	return sentianalysis


def performSentimentAnalysis2(reviews, trainingFname, threshold):
	"""
		For each business, detect the sentiment analysis and confidence score based on reviews
		inputs: 
			reviews = {bid: [{startBucket:, endBucket:, slope:, text: [Tsb+Teb]}, {...}, ...], ...}
			trainingFname = File name of training dataset
			threshold = float - confidence score should be greater than equal to threshold
		output:
			sentianalysis = {bid: [{startBucket:, endBucket:, slope:, text: [Tsb+Teb], sentimentAnalysisScore:, accuracyScore:, confidenceScore:}, {...}, ...], ...}
	"""
	print(TAG, "performSentimentAnalysis()")
	sentianalysis={}
	counter,clf=trainClassifier(trainingFname)
	accuracyScore=findAccurayScore('reviews-test', counter, clf)
	print(accuracyScore)
	
	for bid, values in reviews.items():
		for cp in values:
			#text=pp.formatText(cp['text'])
			sentiScore=computeSentiment(cp['text'], counter, clf)
			confidenceScore=computeConfidenceScore(sentiScore, accuracyScore)
			if confidenceScore >= threshold:
				if bid in sentianalysis:
					sentianalysis[bid].append({'startBucket': cp['startBucket'], 'endBucket': cp['endBucket'], 'slope': cp['slope'], 'text': cp['text'], 'sentimentAnalysisScore': sentiScore, 'accuracyScore': accuracyScore, 'confidenceScore':confidenceScore})
				else:
					sentianalysis[bid]=[{'startBucket': cp['startBucket'], 'endBucket': cp['endBucket'], 'slope': cp['slope'], 'text': cp['text'], 'sentimentAnalysisScore': sentiScore, 'accuracyScore': accuracyScore, 'confidenceScore':confidenceScore}]
	return sentianalysis

def loadDataTestFile(fname):
	"""
	read only the reviews from a given file
	"""
	reviews=[]
	f=open(fname)
	for line in f:
		review=line.strip()
		review = re.sub('<[a-zA-Z]+>', '', review)
		review = re.sub('n\'t', ' not', review)
		review = re.sub('\.+', ' ', review)
		review = re.sub('[^a-zA-Z\d\.]', ' ', review)
		review = re.sub(' +', ' ', review)
		reviews.append(review.lower())
	f.close()
	return reviews


def runSentimentAnalysis(trainingFname, rev_test):

	print(TAG, "runSentimentAnalysis()")
	#load data
	rev_train,labels_train=loadData(train)
	print(TAG,'Files loaded Successfully!')

	#build a counter based on the training dataset
	counter = CountVectorizer(ngram_range=(1,2), max_df=0.41, min_df=0, strip_accents='unicode')
	counter.fit(rev_train)
	print(TAG,'Counter Build')

	#count the number of times each term appears in a document and transform each doc into a count vector
	counts_train = counter.transform(rev_train)#transform the training data
	counts_test = counter.transform(rev_test)#transform the testing data
	print(TAG, 'Transform complete')

	#train classifier
	clf = LogisticRegression(solver="lbfgs", max_iter= 10000, multi_class='multinomial', tol=0.00000001, class_weight='balanced')
	print(TAG, 'Train Classifier complete')

	#train all classifier on the same datasets
	clf.fit(counts_train,labels_train)

	#use hard voting to predict (majority voting)
	pred=clf.predict(counts_test)
	print(TAG, 'Pedict Complete', pred)

	#print accuracy
	#printAccuracy(pred,labels_test)

	#print sentiment score
	printSentimentScore(pred)

	print(TAG, "COMPLETED - run ")


def buildCounter():
	"""
	Build a counter based on the training dataset
	"""
	counter = CountVectorizer(ngram_range=(1,2), max_df=0.41, min_df=0, strip_accents='unicode', stop_words=stopwords.words('english'))
	return counter


def printAccuracy(pred, labels_test):
	"""
	print accuracy of the sentiment analysis prediction model
	"""
	print(TAG, "Accuracy Score:", accuracy_score(pred,labels_test))

def printSentimentScore(pred):
	posCount=0
	negCount=0
	for record in pred:
		if record == 0:
			negCount+=1
		else:
			posCount+=1
	posScore=((posCount/len(pred))*100)
	negScore=((negCount/len(pred))*100)

	print(TAG, "Sentiment Score: Positive:", posScore, "Negative:", negScore)
	return posScore, negScore

def run2(fname_train, fname_test): 
	#i dont know why but I am getting 0.86 accuracy instead of 0.90

	#load Data
	rev_train,labels_train=loadData(fname_train)
	rev_test,labels_test=loadData(fname_test)
	print(TAG,'Files loaded Successfully!')

	#Build Counter
	counter = buildCounter()
	counter.fit(rev_train)
	print(TAG,'Counter Build')

	#count the number of times each term appears in a document and transform each doc into a count vector
	counts_train = counter.transform(rev_train)#transform the training data
	counts_test = counter.transform(rev_test)#transform the testing data
	print(TAG, 'Transform complete')

	#Train Classifier
	#clf = trainClassifier()
	print(TAG, 'Train Classifier complete')

	#train all classifier on the same datasets
	clf.fit(counts_train,labels_train)

	#use hard voting to predict (majority voting)
	pred=clf.predict(counts_test)
	print(TAG, 'Pedict Complete')

	#Print Accuracy
	printAccuracy(pred,labels_test)
	
	#Print Sentiment Score
	printSentimentScore(pred)


def getReviewsPerDate(reviews, businessid, startdate):
	"""
	Return a list of reivews for a particular duration and of a particular business
	"""
	print(TAG, "STARTING - getReviewsPerDate ----------")
	result=[]
	for review in reviews:
		if businessid in review['business_id']:
			if startdate in review['date']:
				text = review['text']
				text = re.sub('[^a-zA-Z\d\.]', ' ', text)
				#text = re.sub('so+', 'so', text)
				result.append(text)
	print(TAG, "COMPLETED - getReviewsPerDate ")
	return result

def getReviewsPerBucket(reviews, businessid, startdate):
	"""
	Return a list of reivews for a particular duration and of a particular business
	"""
	print(TAG, "STARTING - getReviewsPerDate ----------")
	result=[]
	for review in reviews:
		if businessid in review['business_id']:
			if startdate in review['date']:
				text = review['text']
				text = re.sub('[^a-zA-Z\d\.]', ' ', text)
				#text = re.sub('so+', 'so', text)
				result.append(text)
	print(TAG, "COMPLETED - getReviewsPerDate ")
	return result

def saveReviewsToTXT(reviews, fname):
	"""
	Create a new file to save the review text as one review per line
	"""
	print(TAG, "STARTING - saveReviewsToTXT ----------")
	f=open(fname, 'w')
	for text in reviews:
		f.write(text+"\n")
	f.close()
	print(TAG, "SUCCESSFUL - file", fname, "created.")
	print(TAG, "COMPLETED - saveReviewsToTXT ")


def reviewCountPerDatePerBusiness(reviews):
	freq={}
	for review in reviews:
		business_id = review['business_id']
		date = review['date']

		if business_id in freq:
			freq[business_id][date]=freq[business_id].get(date, 0)+1
		else:
			freq[business_id]={date: 1}
	print(freq)
	return freq

def getKReviewCountsResults(reviewCountFreq, k):
	result=()
	for key,value in reviewCountFreq.items():
		for date, count in value.items():
			if count >= k:
				result=(key, date, count)
	print(result)
	return result
