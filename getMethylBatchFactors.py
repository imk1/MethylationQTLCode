def makePairListDict(pairListDictFileName):
	# Make a dictionary that maps (column 1, column 2) to column 3
	pairListDict = {}
	pairListDictFile = open(pairListDictFileName)

	for line in pairListDictFile:
		# Iterate through the lines of the file and make an entry for each in the dictionary
		lineElements = line.strip().split("\t")
		pairList = []
		for le in lineElements[2:]:
			# Iterate through the ints in the line and add each to the list
			pairList.append(int(le))
		pairListDict[(lineElements[0], lineElements[1])] = pairList

	pairListDictFile.close()
	return pairListDict


def makeStringList(stringFileName):
	# Make a list of Strings from a file
	stringFile = open(stringFileName)
	stringList = []

	for line in stringFile:
		# Iterate through the Strings and add each to the list
		stringList.append(line.strip())

	stringFile.close()
	return stringList


def getMethylBatchFactors(methylationFileName, poolInfoFileName, barCodesFileName, methylLetter, outputFileName):
	# For each C on each read, record:
	# 1.  Read name (without base pair)
	# 2.  Chromosome
	# 3.  Position on chromosome
	# 4.  1 if it is methylated, 0 otherwise
	# 5.  Pool
	# 6.  Flowcell
	# 7.  Lane
	# 8.  Library
	# 9.  Strand
	poolInfoListDict = makePairListDict(poolInfoFileName)
	barCodesList = makeStringList(barCodesFileName)
	methylationFileNameElements = methylationFileName.split("/")
	methylationFileNameInfo = methylationFileNameElements[-1].split("_")
	barCode = methylationFileNameInfo[7]
	strand = methylationFileNameInfo[1]
	strandNum = 0
	if strand == "OT":
		# The strand is OT and not OB
		strandNum = 1
	(flowcell, lane) = (methylationFileNameInfo[5], methylationFileNameInfo[6])
	[poolNum, flowcellNum, laneNum] = poolInfoListDict[(flowcell, lane)]
	barCodeNum = barCodesList.index(barCode)
	batchFactorsStr = str(poolNum) + "\t" + str(flowcellNum) + "\t" + str(laneNum) + "\t" + str(barCodeNum) + "\t" + str(strandNum)

	methylationFile = gzip.open(methylationFileName)
	outputFile = gzip.open(outputFileName, 'w+')
	methylationFile.readline() # Remove the header
	for line in methylationFile:
		# Iterate through the C's and record each C's location, methylation status, and batch factors
		lineElements = line.strip().split("\t")
		location = (lineElements[2], int(lineElements[3]))
		isMethyl = 1
		if lineElements[4] != methylLetter:
			# The current C is not methylated
			isMethyl = 0
		outputFile.write(lineElements[0][:-2] + "\t" + location[0] + "\t" + str(location[1]) + "\t" + str(isMethyl) + "\t" + batchFactorsStr + "\n")
	methylationFile.close()
	outputFile.close()


if __name__=="__main__":
	import sys
	import gzip
	methylationFileName = sys.argv[1] # Should end with .gz
	poolInfoFileName = sys.argv[2]
	barCodesFileName = sys.argv[3]
	methylLetter = sys.argv[4]
	outputFileName = sys.argv[5] # Should end with .gz

	getMethylBatchFactors(methylationFileName, poolInfoFileName, barCodesFileName, methylLetter, outputFileName)
