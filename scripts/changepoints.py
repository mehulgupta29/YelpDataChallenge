"""
	This is the starting point for finding changepoints
"""

import Util as util
import Constants as const
import PreProcessing as pp
import ComputeAverageStars as cas
import SentimentAnalysis as sa
import Output as out
import time

TAG = 'Code/scripts/ChangePoints :'

def detectChangePoints(freq, countThreshold, threshold):
	"""
		For each business, detect the change points based on the average stars per bucket date and the averagestars threshold
		inputs: 
			freq = {bid: {bucket1: (S, C, A, [T]), bucket2: ( , , , ), ...}, bid2: {...}, ...}
			countThreshold = int 
			threshold = float - difference between average stars should be atleast equat to threshold
		output:
			changepoint = {bid: [{startBucket:, endBucket:, slope:, text: [Tsb+Teb]}, {...}, ...], ...}
	"""
	print(TAG, "detectChangePoints()")
	
	changepoint={}
	for bid, v in freq.items():
		sortDateList=sorted(v)
		for i in range(len(sortDateList)-1):
			slope = findSlope(v[sortDateList[i]][2], v[sortDateList[i+1]][2], threshold)
			if (slope != 0) and (v[sortDateList[i]][1] >= countThreshold):
				T=v[sortDateList[i]][3] + v[sortDateList[i+1]][3]
				if bid in changepoint:
					changepoint[bid].append({'startBucket': sortDateList[i], 'endBucket': sortDateList[i+1], 'slope': slope, 'text': T})
				else:
					changepoint[bid] = [{'startBucket': sortDateList[i], 'endBucket': sortDateList[i+1], 'slope': slope, 'text': T}]
	return changepoint

def findSlope(one, two, threshold):
	"""
		Calculate the difference between two averagestars values and return the slope if it is greater than eqaul to threshold, otherwise return 0
	"""
	diff = two - one
	if abs(diff) >= threshold:
		return diff
	return 0

def run(params):
	"""
		it executes the program in an sequential way to determine the changepoints
		input:
			params: a dictonary that has all the user inputed params
		output:
			reviews: {bid: [{startBucket:, endBucket:, slope:, sentimentAnalysisScore:, accuracyScore:, confidenceScore:}, {...}, ...], ...}
	"""

	startTime=time.time()
	print(TAG, " -- STARTING --", time.ctime(startTime))

	#Load and Convert JSON to Py
	print(TAG, "Load Reviews and Convert JSON to Python")
	lapTime=time.time()
	reviews = util.loadConvertJSONPy(const.FileNames['review'])
	endTime=time.time()
	timeElapsed=time.localtime(endTime-lapTime)
	print(TAG, "Successful: Reviews Loaded", timeElapsed.tm_min, 'mins', timeElapsed.tm_sec, "secs")

	#Pre-Process the Text and re-format the Dict{}
	print(TAG, "Pre-Processing")
	lapTime=time.time()
	reviews = pp.formatReviews(reviews)
	endTime=time.time()
	timeElapsed=time.localtime(endTime-lapTime)
	print(TAG, "Successful: pre-processing completed", timeElapsed.tm_min, 'mins', timeElapsed.tm_sec, "secs")

	#Compute Average stars
	print(TAG, "Compute Average stars")
	lapTime=time.time()
	reviews = cas.averageStarsPerBucketPerBusiness(reviews, params['bucket']) #bucket={'day','month','year','quarter','semester'}
	endTime=time.time()
	timeElapsed=time.localtime(endTime-lapTime)
	print(TAG, "Successful: average stars computed", timeElapsed.tm_min, 'mins', timeElapsed.tm_sec, "secs")

	#Detect Change Points
	lapTime=time.time()
	reviews = detectChangePoints(reviews, params['reviewcount'], params['averagestars'])
	endTime=time.time()
	timeElapsed=time.localtime(endTime-lapTime)
	print(TAG, "Successful: change points detected", timeElapsed.tm_min, 'mins', timeElapsed.tm_sec, "secs")

	#Perform Sentiment Analysis and Compute Confidence scores
	print(TAG, "Perform Sentiment Analysis")
	lapTime=time.time()
	reviews = sa.performSentimentAnalysis(reviews, params['traindataset'], params['confidencescore'])
	endTime=time.time()
	timeElapsed=time.localtime(endTime-lapTime)
	print(TAG, "Successful: performed sentiment analysis", timeElapsed.tm_min, 'mins', timeElapsed.tm_sec, "secs")	

	endTime=time.time()
	timeElapsed=time.localtime(endTime-startTime)
	print(TAG, " -- DONE -- Total time elapsed:", timeElapsed.tm_min, 'mins', timeElapsed.tm_sec, "secs")

	#export reviews as csv
	datalist=[]
	ctr=0
	fname='output-changepoints.csv'

	headerlist=['Sr No', 'businessId', 'startBucket', 'endBucket', 'slope', 'sentimentAnalysisScore', 'accuracyScore', 'confidenceScore']

	for bid, values in reviews.items():
		for v in values:
			ctr+=1
			datalist.append([ctr, bid, v['startBucket'], v['endBucket'], v['slope'], v['sentimentAnalysisScore'], v['accuracyScore'], v['confidenceScore']])

	util.exportAsCSV(headerlist, datalist, fname)

	return reviews

