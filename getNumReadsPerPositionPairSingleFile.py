def processBismarkSamLineShort(bismarkSamLine):
	# Get the chromosome, position on chromosome, direction in which to iterate, and sequence from a line of a sam file
	# Direction = True means iterate through the sequence in the fowards direction (position is the first base)
	# Direction = False means iterate through the sequence in the backwards direction (position is the last base)
	bismarkSamLineElements = bismarkSamLine.split("\t")
	if ("_" in bismarkSamLineElements[2]) or ("chrM" in bismarkSamLineElements[2]):
		# The read maps to an unknown chromosome or mitochondrial DNA
		return ["", int(bismarkSamLineElements[3]), len(bismarkSamLineElements[9])]

	bismarkChrom = int(bismarkSamLineElements[2][3:])
	return [bismarkSamLineElements[0][0:-2], bismarkChrom, int(bismarkSamLineElements[3]), len(bismarkSamLineElements[9])]


def makePositionPairsList(pairsFileName):
	# Make a dictionary for each pair of locations with a 0 for each pair
	# The format of the position file is chromosome (with no chr), start, end
	positionPairsList = []
	pairsFile = open(pairsFileName)
	
	for line in pairsFile:
		# Iterate through the chromosomes and make an entry in the dictionary for each
		lineElements = line.strip().split("\t")
		if int(lineElements[1]) <= int(lineElements[2]):
			# The first element in the pair is smaller
			positionPairsList.append([int(lineElements[0]), int(lineElements[1]), int(lineElements[2]), 0])
		else:
			positionPairsList.append([int(lineElements[0]), int(lineElements[2]), int(lineElements[1]), 0])
	
	pairsFile.close()
	return positionPairsList


def getNumReadsPerPositionPairSingleFile(readsFileNameListFileName, pairsFileName):
	# Get the number of reads at each pair of positions in a single file
	# ASSUMES THAT READS HAVE NO INDELS
	# ASSUMES THAT THE FILE WITH READS AND THE FILE WITH POSITIONS ARE SORTED IN KARYOTYPIC ORDER [chr1, chr2, ...]
	positionPairsList = makePositionPairsList(pairsFileName)
	readsFileNameListFile = open(readsFileNameListFileName)
	readsFile = open(readsFileName.strip())
	lastStartIndex = 0
	SNPIndexesOnReadDict = {}
		
	for line in readsFile:
		# Iterate through the reads and increment every position for every read
		if line[0] == "@":
			# The line is a header, so continue
			continue
			
		[bismarkRead, bismarkChrom, bismarkPosition, bismarkSequenceLength] = processBismarkSamLineShort(line.strip())
		if (bismarkChrom == "") or (bismarkChrom < positionPairsList[lastStartIndex][0]):
			# The current read maps to mitochondrial DNA or an unknown region
			continue

		if (bismarkChrom == positionPairsList[lastStartIndex][0]):
			# The current read and the current position are on the same chromosome
			if bismarkPosition + bismarkSequenceLength < positionPairsList[lastStartIndex][1]:
				# The current read is before the current position
				continue
			while (lastStartIndex < len(positionPairsList)) and ((positionPairsList[lastStartIndex][1] < bismarkPosition) and (bismarkChrom == positionPairsList[lastStartIndex][0])):
				# The current position is before the current read, so go to the next position
				lastStartIndex = lastStartIndex + 1
			if lastStartIndex >= len(positionPairsList):
				# All pairs have been incremented appropriately, so stop
				break
			if bismarkRead not in SNPIndexesOnReadDict.keys():
				# At a new read
				SNPIndexesOnReadDict[bismarkRead] = []
			currentIndex = lastStartIndex
			while ((currentIndex < len(positionPairsList)) and (bismarkChrom == positionPairsList[currentIndex][0])) and (positionPairsList[currentIndex][1] < bismarkPosition + bismarkSequenceLength):
				# Iterate through the positions that overlap the current read
				if (positionPairsList[currentIndex][1] >= bismarkPosition) and (positionPairsList[currentIndex][2] < bismarkPosition + bismarkSequenceLength):
					# The position at the current index overlaps this read
					if currentIndex not in SNPIndexesOnReadDict[bismarkRead]:
						# The position at the current index has not already been incremented for this read
						SNPIndexesOnReadDict[bismarkRead].append(currentIndex)
						positionPairsList[currentIndex][3] = positionPairsList[currentIndex][3] + 1
				currentIndex = currentIndex + 1
	readsFile.close()
	return positionPairsList

	
def outputpositionPairsList(positionPairsList, outputFileName):
	# Output the number of reads at each position
	outputFile = open(outputFileName, 'w+')
	
	for pp in positionPairsList:
		# Iterate through the pairs of positions and output the number of reads that overlap each pair
		outputFile.write("chr" + str(pp[0]) + "\t" + str(pp[1]) + "\t" + str(pp[2]) + "\t" + str(pp[3]) + "\t" + str(abs(pp[2] - pp[1])) + "\n")
	outputFile.close()


if __name__=="__main__":
	import sys
	readsFileName = sys.argv[1]
	# Each Sam in readsFileNameListFile file has the following important columns:
	# 3.  Chromosome
	# 4.  Start of current read
	# 10.  Sequence
	pairsFileName = sys.argv[2]
	outputFileName = sys.argv[3]

	positionPairsList = getNumReadsPerPositionPairSingleFile(readsFileName, pairsFileName)
	outputpositionPairsList(positionPairsList, outputFileName)