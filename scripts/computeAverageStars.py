"""
	computeAverageStars script is used to define the functions that are used to find the average stars per date for a particular business
"""
from datetime import datetime
import Util as util

def averageStarsPerBucketPerBusiness(reviews, bucket):
	"""
		compute the average stars per bucket date for each business
		inputs: 
			reviews = [{bid:, date:, text:, stars:}, {...}, ...]
			bucket = string
		output:
			freq = {bid: {bucket1: (S, C, A, [T]), bucket2: ( , , , ), ...}, bid2: {...}, ...}
	"""
	freq={}
	for review in reviews:
		bid = review['bid']
		bucketdate = util.bucketedDate(review['date'], bucket)
		stars = review['stars']
		text = review['text']
		if bid in freq:
			if bucketdate in freq[bid]:
				(S,C,A,Tlist) = freq[bid][bucketdate]
				Tlist.append(text)
				freq[bid][bucketdate] = (S+stars, C+1, util.calculateAverage(S+stars, C+1), Tlist)
			else:
				freq[bid][bucketdate] = (stars, 1, util.calculateAverage(stars, 1), [text])
		else:
			freq[bid]={bucketdate: (stars, 1, util.calculateAverage(stars, 1), [text])}
	return freq

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

