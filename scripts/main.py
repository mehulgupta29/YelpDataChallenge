"""
This is the starting point of the project. It is equivalent to the main() in C / Java
"""
import sys
import ChangePoints as cp
import Constants as const
import Metrics as me
import Mappings as ma
import Output as out
#import Events as ev
import QReviewsMoreEfficient as ev

TAG = 'Code/scripts/Main :'

def inputParams(argv):
	params={}
	
	if ('--bucket' or '-b') in argv:
		params['bucket']=argv[argv.index('--bucket')+1]
	else:
		params['bucket']='quarter'

	if ('--averagestars' or '-a') in argv:
		params['averagestars']=float(argv[argv.index('--averagestars')+1])
	else:
		params['averagestars']=float(2)

	if ('--confidencescore' or '-c') in argv:
		params['confidencescore']=float(argv[argv.index('--confidencescore')+1])
	else:
		params['confidencescore']=float(75)

	if ('--traindataset' or '-t') in argv:
		params['traindataset']=const.FileNames[argv[argv.index('--traindataset')+1]]
	else:
		params['traindataset']=const.FileNames['reviews-train']

	if ('--reviewcount' or '-rc') in argv:
		params['reviewcount']=float(argv[argv.index('--reviewcount')+1])
	else:
		params['reviewcount']=float(10)

	if ('--granularity' or '-g') in argv:
		params['granularity']=argv[argv.index('--granularity')+1]
	else:
		params['granularity']='general'

	if ('--kneighbours' or '-k') in argv:
		params['kneighbours']=int(argv[argv.index('--kneighbours')+1])
	else:
		params['kneighbours']=int(5)

	if ('--eventthreshold' or '-e') in argv:
		params['eventthreshold']=float(argv[argv.index('--eventthreshold')+1])
	else:
		params['eventthreshold']=float(300)

	if ('--eventstartbucket' or '-esb') in argv:
		params['eventstartbucket']=argv[argv.index('--eventstartbucket')+1]
	else:
		params['eventstartbucket']='2015-07-01'

	if ('--eventendbucket' or '-eeb') in argv:
		params['eventendbucket']=argv[argv.index('--eventendbucket')+1]
	else:
		params['eventendbucket']='2015-12-31'

	if ('--dispalyeventforbucket' or '-deb') in argv:
		params['dispalyeventforbucket']=argv[argv.index('--dispalyeventforbucket')+1]
	else:
		params['dispalyeventforbucket']=''

	return params

def runChangePoints(params):
	"""
	Find change points
	"""
	changepoints=cp.run(params)
	#print(changepoints)

	#Output the change points
	out.outputChangePoints(changepoints, params['granularity'])

	#Compute Statistics of output
	print(TAG, "Change Point Stats\n\n")
	stats=me.computeCPStatistics(changepoints)
	print(stats)

	#Map and predict
	print(TAG, "Map and predict")
	mappings=ma.run(params, changepoints)
	
	print(TAG, " -- Done -- exiting...")


def runEvents(params):
	"""
	Find Events
	"""
	events=ev.run(params)

	#Output the events
	headerlist,datalist=out.outputEvents(events, params['dispalyeventforbucket'], params['granularity'])
	#headerlist,datalist=out.outputEvents(events, None, params['granularity'])

	#Export as CSV
	ev.exportAsCSV(headerlist, datalist, 'output-events.csv')

if __name__ == "__main__":
	"""
	run command: 
		python Main.py --bucket quarter --averagestars 2.0 --confidencescore 74.9 --granularity general --kneighbours 5 --eventthreshold 300 --dispalyeventforbucket 2016-Q2
	"""
	print(TAG, "STARTING")

	params=inputParams(sys.argv)
	#print(params)
	
	runChangePoints(params)
	runEvents(params)

	print(TAG, "ENDING")