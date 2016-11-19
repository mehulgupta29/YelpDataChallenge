"""
	predict the cause of a changepoint
"""
from operator import itemgetter
import nltk

TAG = 'Code/scripts/Predictions :'

def normalize(N, D):
	"""
	returns normalized values, Normalize = N/D , where D is the max possible value for N
	"""
	if (D != 0):
		return N/D
	else:
		return None

def getCoordinate(matrix):
	"""
	inputs:
		matrix: {'rc':,'st':,'cp':[{startBucket:, endBucket:, slope:, sentimentAnalysisScore:, accuracyScore:, confidenceScore:}, {...}, ...], 'ps':paramsScore(business)}

	vars:
		matrix_class: {-1: Inconclusive(default), 0: Normal, 1: Positive Human Factor, 2: Negative Human Factor}
		xcord: Normalized Stars = Stars/5
		ycord: Normalized ParamsScore = ParamsScore/36

	output:
		(xcord, ycord, matrix_class): (stars, paramscore, class)
	"""
	xcord=normalize(matrix['st'], 5)
	ycord=normalize(matrix['ps'], 36)
	ratio=ycord/xcord

	matrix_class=-1
	
	#if 0.9 <= ratio < 1.1:
	if (ratio <= 1 and ycord>0.5) or (ratio>=1 and xcord<0.5):
		matrix_class=0
	elif (xcord>=0.5 and ycord<=0.5):
		matrix_class=1
	elif (xcord<=0.5 and ycord>=0.5):
		matrix_class=2

	return (xcord, ycord, matrix_class)

def calculateDistance(p1, p2):
	x2=p2[0]
	x1=p1[0]
	y2=p2[1]
	y1=p1[1]
	return (((x2-x1)*(x2-x1))+((y2-y1)*(y2-y1))) ** 0.5

def getNeighbourDistance(test_coordinate, train_coordinates):
	"""
	output:
		result = {(xcord, ycord, matrix_class): distance, (,,):, ...}
	"""
	result={}
	for train_cord in train_coordinates:
			#print(test_coordinate, train_cord)
			distance=calculateDistance(test_coordinate, train_cord)
			result[train_cord]=distance
	return result

def findNeighbours(neighbourDict, k):
	"""
	inputs:
		neighbourDict = {(xcord, ycord, matrix_class): distance, (,,):, ...}
		k : find K nearest neighbours
	output:
		[((xcord, ycord, matrix_class), distance), ((x,y,c), d), ...]
	"""
	freq=neighbourDict
	sortedByValue=sorted(freq.items(),key=itemgetter(1))
	return sortedByValue[:k]

def voteLabels(topKNeighbours):
	"""
	return the vote with the max vote count
	input:
		topKNeighbours = [((xcord, ycord, matrix_class), distance), ((x,y,c), d), ...]
	var:
		vote = {-1: vote count, 0: vote count, 1: vote count}
	output:
		vote = [(class, vote count)]
	"""
	vote={}
	for kn in topKNeighbours:
		rev_class = kn[0][2]
		vote[rev_class]=vote.get(rev_class, 0)+1

	sorting=sorted(vote.items(), key=itemgetter(1), reverse=True)
	return sorting[:1]

def getAccuracy(testList, predictions):
	correct = 0
	for x in range(len(testList)):
		if testList[x] is predictions[x]:
			correct += 1
	return (correct/float(len(testList))) * 100.0

def predictClass(test_matrix, train_coordinates, KNeighbours):
	r_test_cord=getCoordinate(test_matrix)
	neighbourDict=getNeighbourDistance(r_test_cord, train_coordinates)
	topKNeighbours=findNeighbours(neighbourDict, KNeighbours)
	answer=voteLabels(topKNeighbours)
	return answer[0][0]

def runPrediction(train_matrics, test_matrics, KNeighbours):
	"""
	input:
		train_matrics: {bid: {'rc':,'st':, 'cp':[{startBucket:, endBucket:, slope:, sentimentAnalysisScore:, accuracyScore:, confidenceScore:}, {...}, ...], 'ps':paramsScore(business)}, ...}

		test_matrics: {bid: {'rc':,'st':, 'cp':[{startBucket:, endBucket:, slope:, sentimentAnalysisScore:, accuracyScore:, confidenceScore:}, {...}, ...], 'ps':paramsScore(business)}, ...}

	vars:
		coordinates= (xcord, ycord, matrix_class) "(stars, paramscore, class)"
		train_coordinates= [coordinates]
		topKNeighbours= [((xcord, ycord, matrix_class), distance), ((x,y,c), d), ...]
		answer= prediction class: -1,0,1
		predictions= {bid: {'predictionclass': , 'rc':,' st':, 'cp':[{startBucket:, endBucket:, slope:, sentimentAnalysisScore:, accuracyScore:, confidenceScore:}, {...}, ...], 'ps':paramsScore(business)}, ...}
	"""
	print(TAG, "Find Coordinates - Training dataset")
	train_coordinates=[]
	for bid,matrix in train_matrics.items():
		coordinates=getCoordinate(matrix)
		train_coordinates.append(coordinates)
	print(TAG, "Successful: Training dataset Coordinates found")

	print(TAG, "STARTING - Prediction, K=", KNeighbours)  
	predictions={}
	for test_bid, test_matrix in test_matrics.items():
		answer=predictClass(test_matrix, train_coordinates, KNeighbours)
		if answer == -1:
			test_matrix['predictionclass']='Inconclusive: due to insufficient data'
		elif answer == 0:
			test_matrix['predictionclass']='Due to lack of Services to the Customer'
		elif answer == 1:
			test_matrix['predictionclass']='Due to Positive Human Factors'
		else:
			test_matrix['predictionclass']='Due to Negative Human Factors'

		predictions[test_bid]=test_matrix
	print(TAG, "Successfull: Prediction completed")
	
	return predictions

