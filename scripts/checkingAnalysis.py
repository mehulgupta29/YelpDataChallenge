
import util
import constants
import computeAverageStars
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
