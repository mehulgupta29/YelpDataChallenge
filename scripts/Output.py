"""
	this script is used to display the output and its statistics
"""
import statistics

TAG = 'Code/scripts/Output :'

def outputChangePoints(reviews, granularity):
	"""
		For each business, print the change points based on confidence score
		input: 
			reviews = {bid: [{startBucket:, endBucket:, slope:, text: [Tsb+Teb], sentimentAnalysisScore:, accuracyScore:, confidenceScore:}, {...}, ...], ...}
			granularity : 'detailed', 'general'
	"""
	print(TAG, "Printing Change Points at granularity level: ", granularity)

	ctr=0
	if granularity == 'detailed':
		#Header
		print('Sr No.', '\tbid', '\tstartBucket', '\tendBucket', '\tslope', '\tsentimentAnalysisScore', '\taccuracyScore', '\tconfidenceScore')

		#Data
		for bid, values in reviews.items():
			for v in values:
				ctr+=1
				print(ctr,'\t', bid,'\t', v['startBucket'],'\t', v['endBucket'],'\t', v['slope'],'\t', v['sentimentAnalysisScore'],'\t', v['accuracyScore'],'\t', v['confidenceScore'])
	else:
		#Header
		print('Sr No.', '\tBusiness Id           ', '\tChange Point', '\tSlope', '\tConfidence Score')

		#Data
		for bid, values in reviews.items():
			for v in values:
				ctr+=1
				print(ctr,'\t', bid,'\t', v['startBucket'],'\t', '{0:.2f}'.format(v['slope']),'\t', '{0:.2f}'.format(v['confidenceScore']))

def stats(scores):
	return {'mean': statistics.mean(scores), 'median': statistics.median(scores), 'min': min(scores), 'max': max(scores)}

def slopestats(scores):
	outcome=''
	pcount=0
	ncount=0

	for score in scores:
		if score >= 0:
			pcount+=1
		else:
			ncount+=1

	if pcount > ncount:
		percent=(pcount / len(scores))*100
	elif ncount > pcount:
		percent=(pcount / len(scores))*100
	else:
		percent=50

	if percent > 80:
		outcome='Strongly Positive'
	elif percent > 60:
		outcome='Mostly Positive'
	elif percent > 40:
		outcome='Neutral'
	elif percent > 20:
		outcome='Mostly Negative'
	else:
		outcome='Strongly Negative'

	return outcome

def startChangepointStats(scores):
	return {'oldest': min(scores), 'most recent': max(scores)}

def computeCPStatistics(reviews):
	"""
		Change Points detected : 13
		Confidence Score : {mean: , median: , min: , max:}
		Change in stars : {mean: , median: , min: , max:} 
		Overall change Outcome: +, mostly +, neutral, mostly -, -
		Change points : {oldest: , most recent: }
	"""
	print(TAG, "Printing Output Statistics")

	counter=0
	confidenceScoreList=[]
	slopeList=[]
	startChangepointList=[]
	endChangepointList=[]
	sentimentScoreList=[]

	for bid, values in reviews.items():
		counter+=1
		for v in values:
			startChangepointList.append(v['startBucket'])
			endChangepointList.append(v['endBucket'])
			slopeList.append(v['slope'])
			sentimentScoreList.append(v['sentimentAnalysisScore'])
			confidenceScoreList.append(v['confidenceScore'])
	
	cpstats={'changepointDetected': counter, 'confidenceScore': stats(confidenceScoreList), 'changeInStars': stats(slopeList), 'overallOutcome': slopestats(slopeList), 'changepoints': startChangepointStats(startChangepointList)}
	
	return cpstats
