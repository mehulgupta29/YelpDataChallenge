"""
This is the starting point of the project. It is equivalent to the main() in C / Java
"""

import util
import constants
#import numpy as np
#import pandas as pd

def checkinPerBusiness(checkins):
	"""
		get the count of checkins for each business
	"""
	noOfCheckingPerBusi={}
	for checkin in checkins:
		noOfCheckingPerBusi[checkin['business_id']]=noOfCheckingPerBusi.get(checkin['business_id'], 0)+1
	return noOfCheckingPerBusi

#checkins = util.loadAndConvertJSONData(constants.FileNames['checkin'])
#print(util.sortValuesDesc(checkinPerBusiness(checkins), 20))

def averageReviewPerBusiness(reviews):
	freq={}
	for review in reviews:
		business_id = review['business_id']
		date = review['date']
		stars = review['stars']

		if business_id in freq:
			if date in freq[business_id]:
				(T,C,F) = freq[business_id][date]
				freq[business_id][date] = (T+stars, C+1, util.calculateAverage(T+stars, C+1))
			else:
				freq[business_id][date] = (stars, 1, util.calculateAverage(stars, 1))
		else:
			freq[business_id]={date: (stars, 1, util.calculateAverage(stars, 1))}
	return freq


def getFormatedData(avgReviews):
	result=[]
	for k,v in avgReviews.items():
		business_id = k
		for d,a in v.items():
			date = d
			avg = a[2] 
			result.append((business_id, date, avg))
	return result



reviews = util.loadAndConvertJSONData(constants.FileNames['review'])
freq = averageReviewPerBusiness(reviews)
#print(freq)
util.writeDataToJSON('average-reviews-per-busi-per-date', ['business_id', 'date', 'average_stars'], getFormatedData(freq))
