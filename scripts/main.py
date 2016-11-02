"""
This is the starting point of the project. It is equivalent to the main() in C / Java
"""

import util
import constants

#pyData = util.loadAndConvertJSONData(util.FileConstant['test'])
#print(pyData)
#print(pyData[0]['votes'])

print(constants.FileNames['business'])
print(constants.FileNames['test'])

f=open(constants.FileNames['test'])
for f1 in f:
	print(f1)

