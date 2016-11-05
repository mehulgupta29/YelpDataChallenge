"""
This is the starting point of the project. It is equivalent to the main() in C / Java
"""

import util
import constants
import computeAverageStars
import sentimentAnalysis as sa
#import numpy as np
#import pandas as pd

TAG = 'Code/scripts/main :'
print(TAG, "STARTING MAIN ----------")

"""
#checkings per business
#checkins = util.loadAndConvertJSONData(constants.FileNames['checkin'])
#print(util.sortValuesDesc(checkinPerBusiness(checkins), 20))
"""

"""
#calculate average review per date per business
"""
"""
print(TAG, "STARTING COMPUTATION - AVERAGE STARS PER DATE PER BUSINESS ----------")

reviews = util.loadAndConvertJSONData(constants.FileNames['review'])
freq = computeAverageStars.averageReviewPerBusiness(reviews)
#print(freq)
util.writeDataToJSON('average-reviews-per-busi-per-date', ['business_id', 'date', 'average_stars'], computeAverageStars.getFormatedData(freq))

print(TAG, "ENDED COMPUTATION - AVERAGE STARS PER DATE PER BUSINESS ----------")
"""

print(TAG, "LOADING REVIEWS ----------")
reviews = util.loadAndConvertJSONData(constants.FileNames['test'])
print(TAG, "REVIEWS LOADED SUCCESSFULLY")

#reviewFreq = sa.reviewCountPerDatePerBusiness(reviews)
#sa.getKReviewCountsResults(reviewFreq, 5)

"""
#Sentiment Analysis
"""
print(TAG, "STARTING SENTIMENT ANALYSIS ----------")

businessid= 'ZPjWVaRwvtB8J5evDeUXMQ'
startdate = '2016-06-10'
testFname = constants.FileNames['reviews-test-perbusiness-perdate']

reviewList = sa.getReviewsPerDate(reviews, businessid, startdate)

sa.saveReviewsToTXT(reviewList, testFname)

sa.run(constants.FileNames['reviews-train'], testFname)

print(TAG, "ENDED SENTIMENT ANALYSIS")



