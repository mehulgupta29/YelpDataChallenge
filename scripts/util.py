"""
 A simple python script that contains all the helper/util functions. This functions can be used by other scripts.
"""
import json
import os
import csv

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