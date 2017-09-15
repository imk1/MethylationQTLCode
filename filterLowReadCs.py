def filterLowReadCs(methylBatchFactorsFileName, minReads, methylBatchFactorsFiltFileName):
	# Remove Cs with fewer than minReads
	# ASSUMES THAT THE FILE IS SORTED BY CHROMOSOME, THEN POSITION ON CHROMOSOME
	methylBatchFactorsFile = gzip.open(methylBatchFactorsFileName)
	methylBatchFactorsFiltFile = gzip.open(methylBatchFactorsFiltFileName, 'w+')
	lineList = []
	line = methylBatchFactorsFile.readline()
	lineElements = line.split("\t")
	lastLocation = (lineElements[1], int(lineElements[2]))
	lineList.append(line)

	for line in methylBatchFactorsFile:
		# Iterate through the reads and, when reaching a new C, record the previous C if it has enough reads
		lineElements = line.split("\t")
		location = (lineElements[1], int(lineElements[2]))
		if location == lastLocation:
			# The C has not changed
			lineList.append(line)
		else:
			if len(lineList) >= minReads:
				# There are enough reads for the current C, so keep it
				for l in lineList:
					# Iterate through the lines for the current C and record each
					methylBatchFactorsFiltFile.write(l)
			lineList = []
			lastLocation = location
			lineList.append(line)

	methylBatchFactorsFile.close()
	methylBatchFactorsFiltFile.close()


if __name__=="__main__":
	import sys
	import gzip
	import numpy as np
	from sklearn.preprocessing import OneHotEncoder
	from sklearn import linear_model
	methylBatchFactorsFileName = sys.argv[1] # Should end with .gz
	minReads = int(sys.argv[2])
	methylBatchFactorsFiltFileName = sys.argv[3] # Should end with .gz

	filterLowReadCs(methylBatchFactorsFileName, minReads, methylBatchFactorsFiltFileName)
