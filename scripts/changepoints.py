"""
	This script is to detect changepoint
"""

TAG = 'Code/scripts/changepoints : '

# freq = {businessId: {date: (Total, Count, Function - average), date2: (T, C, F), ...}, businessId2: {...}, ...}
def detectChangepoint(freq, threshold):
	"""
	"""
	print(TAG, "STARTING - detectChangepoint ----------")
	globalctr=0
	businessctr=0
	maxgobalctr=0
	changepoint={} #{businessId: [(startDate, endDate, slope), (,,), ...], ...}
	for businessId, dateDict in freq.items():
		localctr=0
		sortDateList=sorted(dateDict)
		for i in range(len(sortDateList)-1):
			slope = find(dateDict[sortDateList[i]], dateDict[sortDateList[i+1]], threshold)
			if slope != 0:
				localctr+=1
				globalctr+=1
				if businessId in changepoint:
					changepoint[businessId].append((sortDateList[i], sortDateList[i+1], slope, localctr, globalctr, businessctr))
					maxgobalctr=globalctr
				else:
					businessctr+=1
					changepoint[businessId] = [(sortDateList[i], sortDateList[i+1], slope, localctr, globalctr, businessctr)]
	print(TAG, "COMPLETED - detectChangepoint ------ max-globalctr:", maxgobalctr, "--businessctr:", businessctr)
	return changepoint

def find(dateOne, dateTwo, threshold):
	"""
	"""
	#print(TAG, "find() ----------dateOne:", dateOne[2], " dateTwo[2]:", dateTwo[2])
	diff = dateOne[2] - dateTwo[2]
	if abs(diff) >= threshold:
		return diff
	return 0