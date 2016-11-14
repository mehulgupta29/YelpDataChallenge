"""
This is the starting point of the project. It is equivalent to the main() in C / Java
"""
import sys
import ChangePoints as cp
import Constants as const

TAG = 'Code/scripts/Main :'

def runChangePoints(params):
	"""
	Find change points
	"""
	cp.run(params)

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

	return params

if __name__ == "__main__":
	print(TAG, "STARTING")

	params=inputParams(sys.argv)
	#print(params)
	
	runChangePoints(params)

	print(TAG, "ENDING")