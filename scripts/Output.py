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

def outputEvents(events, bucketdate, granularity):
	"""
		For each business, print the events for a given bucket
		input: 
			bucket= if None then display all the buckets
			events= {bucket:{word:%, word2: %, ...}, bucket2:{word:%,...}, ...}
			granularity : 'detailed', 'general'
	"""
	print(TAG, "Printing EVENTS at granularity level: ", granularity)

	ctr=0
	#Header
	headerstr='Sr No.'+'\t'+'Bucket'+'\t'+'Word'+'\t'+'% change'
	print('\n', headerstr)

	headerlist=['Sr No.', 'Bucket', 'Word', '% change']

	#Data
	datastr=''
	datalist=[]
	if len(bucketdate) < 1:
		for bucket, values in events.items():
			for word, percent in values.items():
				ctr+=1
				datastr= str(ctr) +'\t'+ bucket +'\t'+ word +'\t'+ str(round(percent, 0)) +'\n'
				print(datastr)
				datalist.append([ctr, bucket, word, round(percent, 0)])
	else:
		for word, percent in events[bucketdate].items():
			ctr+=1
			datastr= str(ctr) +'\t'+ bucketdate +'\t'+ word +'\t'+ str(round(percent, 0)) +'\n'
			print(datastr)
			datalist.append([ctr, bucketdate, word, round(percent, 0)])

	return headerlist,datalist




