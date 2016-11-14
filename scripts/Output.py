"""
	this script is used to display the output
"""

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