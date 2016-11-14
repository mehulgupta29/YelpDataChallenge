import util
import constants

pyData = util.loadAndConvertJSONData(constants.FileNames['business'])
#print(pyData)
util.convertToCSV(pyData, 'business')

pyData = util.loadAndConvertJSONData(constants.FileNames['checkin'])
#print(pyData)
util.convertToCSV(pyData, 'checkin')

pyData = util.loadAndConvertJSONData(constants.FileNames['review'])
#print(pyData)
util.convertToCSV(pyData, 'review')

pyData = util.loadAndConvertJSONData(constants.FileNames['tip'])
#print(pyData)
util.convertToCSV(pyData, 'tip')

pyData = util.loadAndConvertJSONData(constants.FileNames['user'])
#print(pyData)
util.convertToCSV(pyData, 'user')