"""
 A simple python script that contains all the helper/util functions. This functions can be used by other scripts.
"""
import json
import os

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

