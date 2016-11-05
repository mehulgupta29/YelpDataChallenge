"""
	computeAverageStars script is used to define the functions that are used to find the average stars per date for a particular business
"""

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
