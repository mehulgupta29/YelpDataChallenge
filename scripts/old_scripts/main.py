"""
This is the starting point of the project. It is equivalent to the main() in C / Java
"""

import util
import constants
import computeAverageStars
import sentimentAnalysis as sa
import changepoints as cp
import events
#import numpy as np
#import pandas as pd

TAG = 'Code/scripts/main :'
print(TAG, "STARTING MAIN ----------")

"""
#calculate average review per bucket per business
"""
print(TAG, "STARTING COMPUTATION - AVERAGE STARS PER BUCKET PER BUSINESS ----------")

print(TAG, "LOADING REVIEWS ----------")
reviews = util.loadAndConvertJSONData(constants.FileNames['test'])	#Read all the reviews from the file
print(TAG, "REVIEWS LOADED SUCCESSFULLY -> Computing Freq", type(reviews))

"""
bucket='quarter' #bucketType={'day','month','year','quarter','semester'}
freq = computeAverageStars.averageStarsPerBucketPerBusiness(reviews, bucket)	#Compute the freq of average stars per bucket per business
#print(freq)

print(TAG, "REVIEWS FREQ COMPUTED -> Detecting Change points")
#util.writeDataToJSON('average-reviews-per-busi-per-date', ['business_id', 'date', 'average_stars'], computeAverageStars.getFormatedData(freq))

threshold = 2 #the absolute difference between average stars to be considered as a changepoint
changepoints = cp.detectChangepoint(freq, threshold)
print(changepoints)

print(TAG, "ENDED COMPUTATION - AVERAGE STARS PER BUCKET PER BUSINESS ----------")
"""

"""
#Find events

print(TAG, "STARTING COMPUTATION - Events")

print(TAG, "LOADING REVIEWS ----------")
reviews = util.loadAndConvertJSONData(constants.FileNames['test'])	#Read all the reviews from the file
print(TAG, "REVIEWS LOADED SUCCESSFULLY -> Computing Freq")

bucket='quarter' #bucketType={'day','month','year','quarter','semester'}
freq = events.run(reviews, bucket)	

print(TAG, "ENDED COMPUTATION - EVENTS")
"""

"""
#Sentiment Analysis - Tips

print(TAG, "LOADING TIPS ----------")
tips = util.loadAndConvertJSONData(constants.FileNames['tip'])
print(TAG, "TIPS LOADED SUCCESSFULLY")

#tipFreq = sa.reviewCountPerDatePerBusiness(tips)
#sa.getKReviewCountsResults(tipFreq, 5)


print(TAG, "STARTING SENTIMENT ANALYSIS ----- TIPS -----")

businessid= 'uY1hOM4pySx07Yle9NGAiQ'
startdate = '2010-11-03'
tipTestFname = constants.FileNames['tips-test-perbusiness-perdate']

tipList = sa.getReviewsPerDate(tips, businessid, startdate)

sa.saveReviewsToTXT(tipList, tipTestFname)

sa.run(constants.FileNames['reviews-train'], tipTestFname)

print(TAG, "ENDED SENTIMENT ANALYSIS  ----- TIPS -----")
"""



"""
#checkings per business
#checkins = util.loadAndConvertJSONData(constants.FileNames['checkin'])
#print(util.sortValuesDesc(checkinPerBusiness(checkins), 20))
"""


"""
#calculate average review per date per business

print(TAG, "STARTING COMPUTATION - AVERAGE STARS PER DATE PER BUSINESS ----------")

reviews = util.loadAndConvertJSONData(constants.FileNames['review'])
freq = computeAverageStars.averageReviewPerBusiness(reviews)
#print(freq)
util.writeDataToJSON('average-reviews-per-busi-per-date', ['business_id', 'date', 'average_stars'], computeAverageStars.getFormatedData(freq))

print(TAG, "ENDED COMPUTATION - AVERAGE STARS PER DATE PER BUSINESS ----------")
"""


"""
#Sentiment Analysis - Reviews

print(TAG, "LOADING REVIEWS ----------")
reviews = util.loadAndConvertJSONData(constants.FileNames['test'])
print(TAG, "REVIEWS LOADED SUCCESSFULLY")

#reviewFreq = sa.reviewCountPerDatePerBusiness(reviews)
#sa.getKReviewCountsResults(reviewFreq, 5)

print(TAG, "STARTING SENTIMENT ANALYSIS ----- REVIEWS -----")

businessid= 'ZPjWVaRwvtB8J5evDeUXMQ'
startdate = '2016-06-10'
testFname = constants.FileNames['reviews-test-perbusiness-perdate']

reviewList = sa.getReviewsPerDate(reviews, businessid, startdate)

sa.saveReviewsToTXT(reviewList, testFname)

sa.run(constants.FileNames['reviews-train'], testFname)

print(TAG, "ENDED SENTIMENT ANALYSIS  ----- REVIEWS -----")

"""
