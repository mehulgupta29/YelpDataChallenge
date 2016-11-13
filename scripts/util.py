"""
 A simple python script that contains all the helper/util functions. This functions can be used by other scripts.
"""
import json
import os
import csv
from operator import itemgetter
from datetime import datetime

def loadAndConvertJSONData(fname):
	"""
	 This function reads a json file as input and convert it to a python object. It returns a list of dictionaries
	"""
	pyDataList=[]
	file=open(fname)
	for jsonText in file:
		jsonToPy=json.loads(jsonText)
		pyDataList.append(jsonToPy)
	file.close()
	return pyDataList

def convertPyToJson(pyData):
	"""
	 This function takes a python object (List, Dict, Set, Boolean, String, Integer) and returns an equivalent json object 
	"""
	return json.dumps(pyData)

def getAbsFileName(fname):
	fileAbsPath=os.path.abspath(fname)
	return fileAbsPath

def convertToCSV(dataList, fname):
	key=[]
	f = csv.writer(open(fname+".csv", "w"))
	
	#Write CSV Header, If you dont need that, remove this line
	for k in dataList[0].keys():
		key.append(k)
	f.writerow(key)

	#Write the data to csv
	for dataDict in dataList:
		value=[]
		for v in dataDict.values():
			value.append(v)
		f.writerow(value)
	print(fname+".csv", "successfully created")
 

def sortValuesDesc(dataDict, k):
	"""
		sort the dictionary by value, in descending order and return the k top records
	"""
	sortedByValue=sorted(dataDict.items(),key=itemgetter(1),reverse=True)
	return sortedByValue[:k] # return the top k terms and their frequencies

def calculateAverage(T,C):
	return T/C

def writeDataToJSON(fname, headers, data):
	
	f = csv.writer(open(fname+".csv", "w"))
	
	#Write CSV Header, If you dont need that, remove this line
	f.writerow(headers)

	#Write the data to csv
	for rec in data:
		f.writerow(rec)

	print(fname+".csv", "successfully created")
	
def bucketedDate(dateStr, bucket):
	formate="%Y-%m-%d"
	dateObj=datetime.strptime(dateStr, formate)
	bucketType={'day': dateObj.day, 'month': dateObj.month, 'year': dateObj.year, 'quarter': quarter(dateObj), 'semester': semester(dateObj)}
	return bucketType[bucket]

def quarter(dateObj):
	""" 
		Wrong Implementation
	"""
	year=dateObj.year
	month=dateObj.month
	if 1<= month <= 3:
		return str(year)+'-Q1'
	elif 4<= month <=6:
		return str(year)+'-Q2'
	elif 7<= month <=9:
		return str(year)+'-Q3'
	elif 10<= month <=12:
		return str(year)+'-Q4'
	else:
		return "ERROR - Invalid quarter"

def semester(dateObj):
	"""
		Wrong Implementation
	"""
	year=dateObj.year
	month=dateObj.month
	if 1<= month <= 4:
		return str(year)+'-S1'
	elif 5<= month <=8:
		return str(year)+'-S2'
	elif 9<= month <=12:
		return str(year)+'-S3'
	else:
		return "ERROR - Invalid semester"

