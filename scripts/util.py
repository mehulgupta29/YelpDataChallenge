"""
 A simple python script that contains all the helper/util functions. This functions can be used by other scripts.
"""
import json
import os
import csv
from operator import itemgetter

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
	
