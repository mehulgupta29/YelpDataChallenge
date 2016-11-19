"""
	computes the various statistical and analytical metrics of the output - changepoints and events
"""
import statistics

TAG = 'Code/scripts/Metrics :'

def stats(scores):
	return {'mean': statistics.mean(scores), 'median': statistics.median(scores), 'min': min(scores), 'max': max(scores), 'count': len(scores)}

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


