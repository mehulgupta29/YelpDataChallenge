"""
	map changepoints and events with other information like business, user, ...

	changepoints per city {mean, median, min, max, count, values, most-recent changepoint, oldest changepoint recorded}
	changepoints per state {mean, median, min, max, count, values, most-recent changepoint, oldest changepoint recorded}
	changepoints per category {mean, median, min, max, count, values, most-recent changepoint, oldest changepoint recorded}
"""
import Util as util
import Constants as const
import Metrics as met
import Predictions as p

TAG = 'Code/scripts/Mappings :'

def paramsScore(b):
	"""
		calculate the param score for each business based on the aminities provided by them. maximum possible value of ps is 36
	"""
	ps=0

	if 'attributes' in b:
		a=b['attributes']

		if ('Take-out' in a) and a["Take-out"]:
			ps+=1
		if ('Drive-Thru' in a) and a["Drive-Thru"]:
			ps+=1
		if ('TCaters' in a) and a["Caters"]:
			ps+=1
		if ('Noise Level' in a) and a["Noise Level"] != "average":
			ps+=1
		if ('Takes Reservations' in a) and a["Takes Reservations"]:
			ps+=1
		if ('Delivery' in a) and a["Delivery"]:
			ps+=1
		if ('Has TV' in a) and a["Has TV"]:
			ps+=1
		if ('Outdoor Seating' in a) and a["Outdoor Seating"]:
			ps+=1
		if ('Waiter Service' in a) and a["Waiter Service"]:
			ps+=1
		if ('Accepts Credit Cards' in a) and a["Accepts Credit Cards"]:
			ps+=1
		if ('Good for Kids' in a) and a["Good for Kids"]:
			ps+=1
		if ('Good For Groups' in a) and a["Good For Groups"]:
			ps+=1
		if ('Price Range' in a) and a["Price Range"] == 1:
			ps+=1
		elif ('Price Range' in a) and a["Price Range"] == 2:
			ps+=2
		elif ('Price Range' in a) and a["Price Range"] == 3:
			ps+=3
		elif ('Price Range' in a) and a["Price Range"] >= 4:
			ps+=4

		if 'Good For' in a:
			g=a['Good For']

			if ('dessert' in g) and g["dessert"]:
				ps+=1
			if ('latenight' in g) and g["latenight"]:
				ps+=1
			if ('lunch' in g) and g["lunch"]:
				ps+=1
			if ('dinner' in g) and g["dinner"]:
				ps+=1
			if ('brunch' in g) and g["brunch"]:
				ps+=1
			if ('breakfast' in g) and g["breakfast"]:
				ps+=1

		if 'Ambience' in a:
			am=a['Ambience']

			if ('romantic' in am) and am["romantic"]:
				ps+=1
			if ('intimate' in am) and am["intimate"]:
				ps+=1
			if ('classy' in am) and am["classy"]:
				ps+=1
			if ('hipster' in am) and am["hipster"]:
				ps+=1
			if ('divey' in am) and am["divey"]:
				ps+=1
			if ('touristy' in am) and am["touristy"]:
				ps+=1
			if ('trendy' in am) and am["trendy"]:
				ps+=1
			if ('upscale' in am) and am["upscale"]:
				ps+=1
			if ('casual' in am) and am["casual"]:
				ps+=1

		if 'Parking' in a:
			p=a['Parking']

			if ('garage' in p) and p["garage"]:
				ps+=1
			if ('street' in p) and p["street"]:
				ps+=1
			if ('validated' in p) and p["validated"]:
				ps+=1
			if ('lot' in p) and p["lot"]:
				ps+=1
			if ('valet' in p) and p["valet"]:
				ps+=1
	return ps

def mapCPBusi(changepoints, businesses):
	"""
		map each changepoints with respective business data
		inputs:
			changepoints: {bid: [{startBucket:, endBucket:, slope:, sentimentAnalysisScore:, accuracyScore:, confidenceScore:}, {...}, ...], ...}
		
			businesses: [{"business_id": , "full_address": "4734 Lebanon Church Rd\nDravosburg, PA 15034", "hours": {"Friday": {"close": "21:00", "open": "11:00"}, "Tuesday": {"close": "21:00", "open": "11:00"}, "Thursday": {"close": "21:00", "open": "11:00"}, "Wednesday": {"close": "21:00", "open": "11:00"}, "Monday": {"close": "21:00", "open": "11:00"}}, "open": true, "categories": ["Fast Food", "Restaurants"], "city": "Dravosburg", "review_count": 7, "name": "Mr Hoagie", "neighborhoods": [], "longitude": -79.9007057, "state": "PA", "stars": 3.5, "latitude": 40.3543266, "attributes": {"Take-out": true, "Drive-Thru": false, "Good For": {"dessert": false, "latenight": false, "lunch": false, "dinner": false, "brunch": false, "breakfast": false}, "Caters": false, "Noise Level": "average", "Takes Reservations": false, "Delivery": false, "Ambience": {"romantic": false, "intimate": false, "classy": false, "hipster": false, "divey": false, "touristy": false, "trendy": false, "upscale": false, "casual": false}, "Parking": {"garage": false, "street": false, "validated": false, "lot": false, "valet": false}, "Has TV": false, "Outdoor Seating": false, "Attire": "casual", "Alcohol": "none", "Waiter Service": false, "Accepts Credit Cards": true, "Good for Kids": true, "Good For Groups": true, "Price Range": 1}, "type": "business"}]
		
		outputs:
			mapcpbusi: {bid: {...,  changepoints:[{startBucket:, endBucket:, slope:, sentimentAnalysisScore:, accuracyScore:, confidenceScore:}, {...}, ...]}, ...}
			
			perCity,perState,perCategory: { city/state/category:{'slopelist':[], 'starlist':[], 'reviewcountlist':[], 'cpvalues':[{startBucket:, endBucket:, slope:, sentimentAnalysisScore:, accuracyScore:, confidenceScore:}, {...}, ...], 'bucketlist':[], 'bidlist':[]}, ...}
			
			matrics: {bid: {'rc':,'st':, 'cp':[{startBucket:, endBucket:, slope:, sentimentAnalysisScore:, accuracyScore:, confidenceScore:}, {...}, ...], 'ps':paramsScore(business)}, ...}
	"""
	mapcpbusi={}	#1
	perCity={}	#2
	perState={}	#3
	perCategory={}	#4
	train_matrics={}	#5
	test_matrics={}	#6

	for business in businesses:
		slopelist=[]
		bucketlist=[]
		bidlist=[]
		starlist=[]
		reviewcountlist=[]

		for cpBid, cp in changepoints.items():			
			if cpBid == business['business_id']:

				#1
				business['changepoints']=cp
				mapcpbusi[cpBid]=business

				for metric in cp:
					slopelist.append(metric['slope'])
					bucketlist.append(metric['startBucket'])
				bidlist.append(cpBid)
				starlist.append(business['stars'])
				reviewcountlist.append(business['review_count'])

				#2
				if ('city' in business) and business['city'] in perCity:
					v=perCity[business['city']]
					perCity[business['city']]={'slopelist':slopelist+v['slopelist'], 'starlist':starlist+v['starlist'], 'reviewcountlist':reviewcountlist+v['reviewcountlist'], 'cpvalues':cp, 'bucketlist':bucketlist+v['bucketlist'], 'bidlist':bidlist+v['bidlist']}
				else:
					perCity[business['city']]={'slopelist':slopelist, 'starlist':starlist, 'reviewcountlist':reviewcountlist, 'cpvalues':cp, 'bucketlist':bucketlist, 'bidlist':bidlist}

				#3
				if ('state' in business) and business['state'] in perState:
					w=perState[business['state']]
					perState[business['state']]={'slopelist':slopelist+w['slopelist'], 'starlist':starlist+w['starlist'], 'reviewcountlist':reviewcountlist+w['reviewcountlist'], 'cpvalues':cp, 'bucketlist':bucketlist+w['bucketlist'], 'bidlist':bidlist+w['bidlist']}
				else:
					perState[business['state']]={'slopelist':slopelist, 'starlist':starlist, 'reviewcountlist':reviewcountlist, 'cpvalues':cp, 'bucketlist':bucketlist, 'bidlist':bidlist}

				#4
				if ('categories' in business): 
					for cat in business['categories']:
						if cat in perCategory:
							x=perCategory[cat]
							perCategory[cat]={'slopelist':slopelist+x['slopelist'], 'starlist':starlist+x['starlist'], 'reviewcountlist':reviewcountlist+x['reviewcountlist'], 'cpvalues':cp, 'bucketlist':bucketlist+x['bucketlist'], 'bidlist':bidlist+x['bidlist']}
						else:
							perCategory[cat]={'slopelist':slopelist, 'starlist':starlist, 'reviewcountlist':reviewcountlist, 'cpvalues':cp, 'bucketlist':bucketlist, 'bidlist':bidlist}
				
				#5
				test_matrics[business['business_id']]={'rc':business['review_count'],'st':business['stars'], 'cp':cp, 'ps':paramsScore(business)}
			else:
				#6
				train_matrics[business['business_id']]={'rc':business['review_count'],'st':business['stars'], 'cp':[], 'ps':paramsScore(business)}

	return mapcpbusi,perCity,perState,perCategory,train_matrics,test_matrics

def run(params, changepoints):
	"""
	vars: 
		results= {bid: {'predictionclass': , 'rc':,' st':, 'cp':[{startBucket:, endBucket:, slope:, sentimentAnalysisScore:, accuracyScore:, confidenceScore:}, {...}, ...], 'ps':paramsScore(business)}, ...}
	"""

	print(TAG, "-- STARTING --")

	#Load and Convert JSON to Py
	print(TAG, "Load Businesses and Convert JSON to Python")
	businesses = util.loadConvertJSONPy(const.FileNames['business'])
	print(TAG, "Successful: Reviews Loaded")

	#Map reviews-changepoints and business
	print(TAG, "Mapping changepoints to businesses")
	rbs,perCity,perState,perCategory,train_matrics,test_matrics = mapCPBusi(changepoints, businesses)
	print(TAG, "Successful: Mapping completed")
		
	#Compute stats
	print(TAG, "Calculating Stats - City")
	for k,v in perCity.items():
		perCity[k]['metrics']={'slopestats':met.stats(v['slopelist']), 'overallslopestat':met.slopestats(v['slopelist']), 'starstats':met.stats(v['starlist']), 'rcstats':met.stats(v['reviewcountlist']), 'bucketstats':met.startChangepointStats(v['bucketlist'])}

	print(TAG, "Calculating Stats - State")
	for k,v in perState.items():
		perState[k]['metrics']={'slopestats':met.stats(v['slopelist']), 'overallslopestat':met.slopestats(v['slopelist']), 'starstats':met.stats(v['starlist']), 'rcstats':met.stats(v['reviewcountlist']), 'bucketstats':met.startChangepointStats(v['bucketlist'])}

	print(TAG, "Calculating Stats - Category")
	for k,v in perCategory.items():
		perCategory[k]['metrics']={'slopestats':met.stats(v['slopelist']), 'overallslopestat':met.slopestats(v['slopelist']), 'starstats':met.stats(v['starlist']), 'rcstats':met.stats(v['reviewcountlist']), 'bucketstats':met.startChangepointStats(v['bucketlist'])}

	#Predict
	print(TAG, "STARTING - Prediction")
	results=p.runPrediction(train_matrics, test_matrics, params['kneighbours'])
	print(TAG, "Successful: Prediction completed")

	for bid, v in results.items():
		print("Bid:",bid,"\tStats(stars, paramscore):",(v['st'],v['ps']),"\tReason:", v['predictionclass'])

#run({'kneighbours': 5}, {'xfSw-RbQ-4ackmmOJmlg6Q': [{'confidenceScore': 81.818181818181813, 'startBucket': '2016-Q2', 'slope': -3.5999999999999996, 'sentimentAnalysisScore': -90.9090909090909, 'accuracyScore': 0.90000000000000002, 'endBucket': '2016-Q3'}], 'g2VN-L5UPk5haGVeSe1LEg': [{'confidenceScore': 82.5, 'startBucket': '2012-Q3', 'slope': 2.0, 'sentimentAnalysisScore': -91.66666666666666, 'accuracyScore': 0.90000000000000002, 'endBucket': '2012-Q4'}], 'CNxkXXv7NVkoLWjU7t4gwA': [{'confidenceScore': 78.75, 'startBucket': '2016-Q2', 'slope': 2.2666666666666666, 'sentimentAnalysisScore': -87.5, 'accuracyScore': 0.90000000000000002, 'endBucket': '2016-Q3'}], 'C_Tu6eMyzSJhDwg2XXtnUw': [{'confidenceScore': 75.000000000000014, 'startBucket': '2015-Q1', 'slope': -2.0, 'sentimentAnalysisScore': -83.33333333333334, 'accuracyScore': 0.90000000000000002, 'endBucket': '2015-Q2'}], '1oFvqm7eSpJbVpxpPxueaA': [{'confidenceScore': 77.142857142857139, 'startBucket': '2016-Q2', 'slope': 2.5384615384615383, 'sentimentAnalysisScore': -85.71428571428571, 'accuracyScore': 0.90000000000000002, 'endBucket': '2016-Q3'}], 'sSoqftejBK-j3PWefePqYA': [{'confidenceScore': 77.142857142857139, 'startBucket': '2016-Q2', 'slope': -3.45, 'sentimentAnalysisScore': -85.71428571428571, 'accuracyScore': 0.90000000000000002, 'endBucket': '2016-Q3'}], 'kexliej8P8VdxXfMQmyfyQ': [{'confidenceScore': 78.75, 'startBucket': '2016-Q2', 'slope': -2.0999999999999996, 'sentimentAnalysisScore': -87.5, 'accuracyScore': 0.90000000000000002, 'endBucket': '2016-Q3'}], 'leewd6-3ZCVAPr-RVtcVKA': [{'confidenceScore': 77.142857142857139, 'startBucket': '2016-Q1', 'slope': -2.45, 'sentimentAnalysisScore': -85.71428571428571, 'accuracyScore': 0.90000000000000002, 'endBucket': '2016-Q2'}], 'DfNoB509sMpMbu-qvsgvrA': [{'confidenceScore': 76.15384615384616, 'startBucket': '2016-Q2', 'slope': 2.0, 'sentimentAnalysisScore': -84.61538461538461, 'accuracyScore': 0.90000000000000002, 'endBucket': '2016-Q3'}], 'X5QTGpPfqXFtmtizsGAksw': [{'confidenceScore': 75.000000000000014, 'startBucket': '2011-Q3', 'slope': -2.3, 'sentimentAnalysisScore': -83.33333333333334, 'accuracyScore': 0.90000000000000002, 'endBucket': '2011-Q4'}], 'FSoc19hv_VnUisJ856QZ5w': [{'confidenceScore': 78.0, 'startBucket': '2016-Q2', 'slope': 2.642857142857143, 'sentimentAnalysisScore': -86.66666666666667, 'accuracyScore': 0.90000000000000002, 'endBucket': '2016-Q3'}], 'zDGhPMIxPcjKWVyXROjUzw': [{'confidenceScore': 84.705882352941174, 'startBucket': '2015-Q2', 'slope': 2.242424242424242, 'sentimentAnalysisScore': -94.11764705882352, 'accuracyScore': 0.90000000000000002, 'endBucket': '2015-Q3'}], 'Iet7RbjzuVoXX907QfHIOw': [{'confidenceScore': 90.0, 'startBucket': '2016-Q2', 'slope': -2.230769230769231, 'sentimentAnalysisScore': -100.0, 'accuracyScore': 0.90000000000000002, 'endBucket': '2016-Q3'}], 'i0rx72IqWuGOyWadGjRLVg': [{'confidenceScore': 82.5, 'startBucket': '2016-Q2', 'slope': 2.5, 'sentimentAnalysisScore': -91.66666666666666, 'accuracyScore': 0.90000000000000002, 'endBucket': '2016-Q3'}], 'V9i9LnTg9H2XvzqCVBSOXg': [{'confidenceScore': 77.142857142857139, 'startBucket': '2011-Q3', 'slope': -2.0606060606060606, 'sentimentAnalysisScore': -85.71428571428571, 'accuracyScore': 0.90000000000000002, 'endBucket': '2011-Q4'}], '9ENO2XnX3rbddsXtjVAUqw': [{'confidenceScore': 83.571428571428584, 'startBucket': '2016-Q2', 'slope': 2.0833333333333335, 'sentimentAnalysisScore': -92.85714285714286, 'accuracyScore': 0.90000000000000002, 'endBucket': '2016-Q3'}], 'kQzJki9E0ducGKz-CAn_XA': [{'confidenceScore': 80.0, 'startBucket': '2015-Q4', 'slope': -2.066666666666667, 'sentimentAnalysisScore': -88.88888888888889, 'accuracyScore': 0.90000000000000002, 'endBucket': '2016-Q1'}], 'XuJwbaXrRZfnFtPxXCeJ2w': [{'confidenceScore': 86.08695652173914, 'startBucket': '2016-Q2', 'slope': 2.3289473684210527, 'sentimentAnalysisScore': -95.65217391304348, 'accuracyScore': 0.90000000000000002, 'endBucket': '2016-Q3'}], '-wvryBujtHabx4jCW98eqQ': [{'confidenceScore': 84.705882352941174, 'startBucket': '2015-Q2', 'slope': -2.883333333333333, 'sentimentAnalysisScore': -94.11764705882352, 'accuracyScore': 0.90000000000000002, 'endBucket': '2015-Q3'}], 'RrIUqPDMxD23bCgFHGh6sQ': [{'confidenceScore': 80.0, 'startBucket': '2016-Q2', 'slope': -2.2499999999999996, 'sentimentAnalysisScore': -88.88888888888889, 'accuracyScore': 0.90000000000000002, 'endBucket': '2016-Q3'}], 'EtijSxqheu_LHohSvKQfLA': [{'confidenceScore': 81.818181818181813, 'startBucket': '2016-Q2', 'slope': -2.6, 'sentimentAnalysisScore': -90.9090909090909, 'accuracyScore': 0.90000000000000002, 'endBucket': '2016-Q3'}], '24OmQWFTnbfGv-e8GyEMAw': [{'confidenceScore': 75.000000000000014, 'startBucket': '2016-Q2', 'slope': -2.090909090909091, 'sentimentAnalysisScore': -83.33333333333334, 'accuracyScore': 0.90000000000000002, 'endBucket': '2016-Q3'}], 'znmvCpcwxYk_kYCqtUFt5Q': [{'confidenceScore': 75.000000000000014, 'startBucket': '2013-Q1', 'slope': -2.8181818181818183, 'sentimentAnalysisScore': -83.33333333333334, 'accuracyScore': 0.90000000000000002, 'endBucket': '2013-Q2'}], '0BpMvu5B9fY-KEbOuxLtFQ': [{'confidenceScore': 78.75, 'startBucket': '2013-Q3', 'slope': 2.6153846153846154, 'sentimentAnalysisScore': -87.5, 'accuracyScore': 0.90000000000000002, 'endBucket': '2013-Q4'}], 'YTIVvEP8QWV3iJUV8JI24w': [{'confidenceScore': 78.75, 'startBucket': '2016-Q2', 'slope': -2.7857142857142856, 'sentimentAnalysisScore': -87.5, 'accuracyScore': 0.90000000000000002, 'endBucket': '2016-Q3'}], 'qY9IzXAY_NM5nf697T02RQ': [{'confidenceScore': 76.15384615384616, 'startBucket': '2016-Q2', 'slope': -2.4, 'sentimentAnalysisScore': -84.61538461538461, 'accuracyScore': 0.90000000000000002, 'endBucket': '2016-Q3'}], 'e0HQNVQcfsTavbOsIlCd6w': [{'confidenceScore': 83.07692307692308, 'startBucket': '2014-Q4', 'slope': -2.590909090909091, 'sentimentAnalysisScore': -92.3076923076923, 'accuracyScore': 0.90000000000000002, 'endBucket': '2015-Q1'}], 'vcB9sr7s4WrcAw8yNbBm7g': [{'confidenceScore': 76.666666666666671, 'startBucket': '2015-Q2', 'slope': -2.3076923076923075, 'sentimentAnalysisScore': -85.18518518518519, 'accuracyScore': 0.90000000000000002, 'endBucket': '2015-Q3'}], 'mMTlibtg6lZ0FomMqiNcWA': [{'confidenceScore': 77.586206896551715, 'startBucket': '2015-Q4', 'slope': -2.0714285714285716, 'sentimentAnalysisScore': -86.20689655172413, 'accuracyScore': 0.90000000000000002, 'endBucket': '2016-Q1'}], '0CeEgarUoVP2Nq9s1Mn0Aw': [{'confidenceScore': 76.15384615384616, 'startBucket': '2016-Q2', 'slope': -3.416666666666667, 'sentimentAnalysisScore': -84.61538461538461, 'accuracyScore': 0.90000000000000002, 'endBucket': '2016-Q3'}], '9e42a9MVYBqJOfArmQoOIA': [{'confidenceScore': 77.72727272727272, 'startBucket': '2013-Q3', 'slope': -2.545454545454545, 'sentimentAnalysisScore': -86.36363636363636, 'accuracyScore': 0.90000000000000002, 'endBucket': '2013-Q4'}], 'KHtaNwoAG76qK6BIYGYJvQ': [{'confidenceScore': 82.5, 'startBucket': '2016-Q2', 'slope': -2.1818181818181817, 'sentimentAnalysisScore': -91.66666666666666, 'accuracyScore': 0.90000000000000002, 'endBucket': '2016-Q3'}], 'mSbFLlDB5Qu-6al1e2DSBw': [{'confidenceScore': 83.571428571428584, 'startBucket': '2016-Q2', 'slope': -3.5384615384615383, 'sentimentAnalysisScore': -92.85714285714286, 'accuracyScore': 0.90000000000000002, 'endBucket': '2016-Q3'}], 'bdsKG7MQIMmZ73lgOaTZ0A': [{'confidenceScore': 81.818181818181813, 'startBucket': '2015-Q1', 'slope': 2.6, 'sentimentAnalysisScore': -90.9090909090909, 'accuracyScore': 0.90000000000000002, 'endBucket': '2015-Q3'}], 'cTFq_1sAnQUb9eMZO6FlvQ': [{'confidenceScore': 81.818181818181813, 'startBucket': '2016-Q2', 'slope': -3.2, 'sentimentAnalysisScore': -90.9090909090909, 'accuracyScore': 0.90000000000000002, 'endBucket': '2016-Q3'}], 'vteLW_uV_3ycbgKYXRMevA': [{'confidenceScore': 82.5, 'startBucket': '2016-Q2', 'slope': 2.090909090909091, 'sentimentAnalysisScore': -91.66666666666666, 'accuracyScore': 0.90000000000000002, 'endBucket': '2016-Q3'}], 'txjgzrWMeuBJfG8eAv3mow': [{'confidenceScore': 90.0, 'startBucket': '2015-Q2', 'slope': 2.0, 'sentimentAnalysisScore': -100.0, 'accuracyScore': 0.90000000000000002, 'endBucket': '2015-Q3'}], '16VWORTVIsJ6QZt3HTxj3w': [{'confidenceScore': 75.000000000000014, 'startBucket': '2015-Q2', 'slope': -2.6363636363636362, 'sentimentAnalysisScore': -83.33333333333334, 'accuracyScore': 0.90000000000000002, 'endBucket': '2015-Q3'}], 'UCid2Tas6K4SB9sHO9gQ8w': [{'confidenceScore': 76.15384615384616, 'startBucket': '2015-Q3', 'slope': 2.090909090909091, 'sentimentAnalysisScore': -84.61538461538461, 'accuracyScore': 0.90000000000000002, 'endBucket': '2015-Q4'}], 'vnla3T2fUaskp5L4xKtqsw': [{'confidenceScore': 79.411764705882348, 'startBucket': '2016-Q1', 'slope': -2.0, 'sentimentAnalysisScore': -88.23529411764706, 'accuracyScore': 0.90000000000000002, 'endBucket': '2016-Q2'}], 'vbIgxwyyTq03158xRvnfuQ': [{'confidenceScore': 83.571428571428584, 'startBucket': '2014-Q2', 'slope': -2.25, 'sentimentAnalysisScore': -92.85714285714286, 'accuracyScore': 0.90000000000000002, 'endBucket': '2014-Q3'}], '17FKJgS11HppOf00qXKEqA': [{'confidenceScore': 76.15384615384616, 'startBucket': '2016-Q2', 'slope': 2.3333333333333335, 'sentimentAnalysisScore': -84.61538461538461, 'accuracyScore': 0.90000000000000002, 'endBucket': '2016-Q3'}], '75ryy2cW4JUQ4ZgD4XGSIw': [{'confidenceScore': 85.263157894736835, 'startBucket': '2013-Q3', 'slope': -2.0357142857142856, 'sentimentAnalysisScore': -94.73684210526315, 'accuracyScore': 0.90000000000000002, 'endBucket': '2013-Q4'}], 'n_QAA70NrnGIsGjog3HF_Q': [{'confidenceScore': 77.142857142857139, 'startBucket': '2016-Q2', 'slope': -2.888888888888889, 'sentimentAnalysisScore': -85.71428571428571, 'accuracyScore': 0.90000000000000002, 'endBucket': '2016-Q3'}], 'vrkhs3YxUPa21YgkfsveOg': [{'confidenceScore': 75.78947368421052, 'startBucket': '2016-Q2', 'slope': -2.3333333333333335, 'sentimentAnalysisScore': -84.21052631578947, 'accuracyScore': 0.90000000000000002, 'endBucket': '2016-Q3'}], '4_yqGLhfQJ-mRyH7i2-KNQ': [{'confidenceScore': 75.000000000000014, 'startBucket': '2016-Q2', 'slope': 2.35, 'sentimentAnalysisScore': -83.33333333333334, 'accuracyScore': 0.90000000000000002, 'endBucket': '2016-Q3'}], 'Yet-ozuhwfG5NLeLqeKcWg': [{'confidenceScore': 77.142857142857139, 'startBucket': '2015-Q3', 'slope': -2.5, 'sentimentAnalysisScore': -85.71428571428571, 'accuracyScore': 0.90000000000000002, 'endBucket': '2015-Q4'}], '00xD3o61AjrGOpEHiGPEwg': [{'confidenceScore': 75.000000000000014, 'startBucket': '2016-Q2', 'slope': -2.125, 'sentimentAnalysisScore': -83.33333333333334, 'accuracyScore': 0.90000000000000002, 'endBucket': '2016-Q3'}], 'Y1sSdaeuicOzR87DIREinw': [{'confidenceScore': 81.818181818181813, 'startBucket': '2014-Q3', 'slope': 2.2, 'sentimentAnalysisScore': -90.9090909090909, 'accuracyScore': 0.90000000000000002, 'endBucket': '2014-Q4'}], 'LRpoyZt-3PbCEEbU7nkvwQ': [{'confidenceScore': 81.0, 'startBucket': '2016-Q2', 'slope': 2.2666666666666666, 'sentimentAnalysisScore': -90.0, 'accuracyScore': 0.90000000000000002, 'endBucket': '2016-Q3'}], 'QqPaQhUZQL-9zzxNJDcriA': [{'confidenceScore': 81.818181818181813, 'startBucket': '2016-Q2', 'slope': 2.3, 'sentimentAnalysisScore': -90.9090909090909, 'accuracyScore': 0.90000000000000002, 'endBucket': '2016-Q3'}], '9zUNzGdT-AfVOWrcbD2Vog': [{'confidenceScore': 82.5, 'startBucket': '2016-Q1', 'slope': -2.0, 'sentimentAnalysisScore': -91.66666666666666, 'accuracyScore': 0.90000000000000002, 'endBucket': '2016-Q2'}], 'bVsh5Z6-BrVkhSo9STyk0w': [{'confidenceScore': 78.0, 'startBucket': '2014-Q4', 'slope': -4.0, 'sentimentAnalysisScore': -86.66666666666667, 'accuracyScore': 0.90000000000000002, 'endBucket': '2015-Q1'}], 'XHTUbyhQnwzP1FDXPBk84A': [{'confidenceScore': 75.000000000000014, 'startBucket': '2015-Q3', 'slope': -3.6363636363636367, 'sentimentAnalysisScore': -83.33333333333334, 'accuracyScore': 0.90000000000000002, 'endBucket': '2015-Q4'}], 'eHD1iu4B5yd_wj_uiSapzQ': [{'confidenceScore': 81.818181818181813, 'startBucket': '2014-Q1', 'slope': 2.0, 'sentimentAnalysisScore': -90.9090909090909, 'accuracyScore': 0.90000000000000002, 'endBucket': '2015-Q3'}], 'qXQ3ZBdwI3GlbR5-eYWqNA': [{'confidenceScore': 77.142857142857139, 'startBucket': '2016-Q2', 'slope': -2.0, 'sentimentAnalysisScore': -85.71428571428571, 'accuracyScore': 0.90000000000000002, 'endBucket': '2016-Q3'}], 'YqcPBiZMeCjZFlJlA28zwQ': [{'confidenceScore': 75.000000000000014, 'startBucket': '2016-Q2', 'slope': -2.454545454545454, 'sentimentAnalysisScore': -83.33333333333334, 'accuracyScore': 0.90000000000000002, 'endBucket': '2016-Q3'}], '_4J7fu3t-3yc4BaNCPN9HA': [{'confidenceScore': 78.0, 'startBucket': '2016-Q2', 'slope': -2.7857142857142856, 'sentimentAnalysisScore': -86.66666666666667, 'accuracyScore': 0.90000000000000002, 'endBucket': '2016-Q3'}], 'DKY2be7dDX2CT_WB_Dk4pQ': [{'confidenceScore': 78.75, 'startBucket': '2015-Q3', 'slope': 2.1333333333333333, 'sentimentAnalysisScore': -87.5, 'accuracyScore': 0.90000000000000002, 'endBucket': '2015-Q4'}], 'CvufqyRBbS2Ed2wQlAXCMw': [{'confidenceScore': 78.75, 'startBucket': '2013-Q2', 'slope': -2.153846153846154, 'sentimentAnalysisScore': -87.5, 'accuracyScore': 0.90000000000000002, 'endBucket': '2013-Q3'}], 'gUz5Gdf7biNIhTQwg2V6Gw': [{'confidenceScore': 81.428571428571431, 'startBucket': '2016-Q2', 'slope': -2.473684210526316, 'sentimentAnalysisScore': -90.47619047619048, 'accuracyScore': 0.90000000000000002, 'endBucket': '2016-Q3'}], 'JCyuOGUzMrXxJOj0pkoRMg': [{'confidenceScore': 83.07692307692308, 'startBucket': '2016-Q2', 'slope': 2.75, 'sentimentAnalysisScore': -92.3076923076923, 'accuracyScore': 0.90000000000000002, 'endBucket': '2016-Q3'}], 'q4r4-CLho_L_paKcObKo4g': [{'confidenceScore': 80.526315789473685, 'startBucket': '2016-Q2', 'slope': -3.666666666666667, 'sentimentAnalysisScore': -89.47368421052632, 'accuracyScore': 0.90000000000000002, 'endBucket': '2016-Q3'}], 'I6fg87AEulZezPpBLQadYw': [{'confidenceScore': 83.07692307692308, 'startBucket': '2016-Q2', 'slope': -2.9166666666666665, 'sentimentAnalysisScore': -92.3076923076923, 'accuracyScore': 0.90000000000000002, 'endBucket': '2016-Q3'}], 'Zc2IwSzGY63zkyhfNrr7HA': [{'confidenceScore': 78.0, 'startBucket': '2016-Q2', 'slope': -2.0, 'sentimentAnalysisScore': -86.66666666666667, 'accuracyScore': 0.90000000000000002, 'endBucket': '2016-Q3'}], 'FcBcmHppCJiaMPE-7AQcRQ': [{'confidenceScore': 78.75, 'startBucket': '2016-Q2', 'slope': -3.1739130434782608, 'sentimentAnalysisScore': -87.5, 'accuracyScore': 0.90000000000000002, 'endBucket': '2016-Q3'}], 'rz5rKbTQpKVHcjGeCbL10A': [{'confidenceScore': 75.78947368421052, 'startBucket': '2015-Q3', 'slope': -2.2976190476190474, 'sentimentAnalysisScore': -84.21052631578947, 'accuracyScore': 0.90000000000000002, 'endBucket': '2015-Q4'}], 'KVOqzp3ie3yhXxBnjqNWbQ': [{'confidenceScore': 75.000000000000014, 'startBucket': '2016-Q2', 'slope': -3.090909090909091, 'sentimentAnalysisScore': -83.33333333333334, 'accuracyScore': 0.90000000000000002, 'endBucket': '2016-Q3'}]})