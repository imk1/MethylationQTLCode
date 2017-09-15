def processBismarkSamLineShort(bismarkSamLine):
	# Get the chromosome, position on chromosome, direction in which to iterate, and sequence from a line of a sam file
	# Direction = True means iterate through the sequence in the fowards direction (position is the first base)
	# Direction = False means iterate through the sequence in the backwards direction (position is the last base)
	bismarkSamLineElements = bismarkSamLine.split("\t")
	if ("_" in bismarkSamLineElements[2]) or ("chrM" in bismarkSamLineElements[2]):
		# The read maps to an unknown chromosome or mitochondrial DNA
		return ["", int(bismarkSamLineElements[3]), len(bismarkSamLineElements[9])]

	bismarkChrom = bismarkSamLineElements[2]
	return [bismarkChrom, int(bismarkSamLineElements[3]), len(bismarkSamLineElements[9])]


def makePositionPairsDict(pairsFileName):
	# Make a dictionary for each pair of locations with a 0 for each pair
	positionPairsDict = {}
	pairsFile = open(pairsFileName)
	chromList = []
	positionStartMax = 0
	positionEndMin = float("inf")
	
	for line in pairsFile:
		# Iterate through the chromosomes and make an entry in the dictionary for each
		lineElements = line.strip().split("\t")
		if lineElements[0] not in chromList:
			# Add the current chromosome to the list
			chromList.append(lineElements[0])
		pairChromPositions = (lineElements[0], int(lineElements[1]), int(lineElements[2]));
		if int(lineElements[2]) < int(lineElements[1]):
			# The second element in the pair is smaller
			pairChromPositions = (lineElements[0], int(lineElements[2]), int(lineElements[1]));
		if pairChromPositions[1] > positionStartMax:
			# The current start is greater than the largest start so far
			positionStartMax = pairChromPositions[1]
		if pairChromPositions[2] < positionEndMin:
			# The current end is less than the largest end so far
			positionEndMin = pairChromPositions[2]
		positionPairsDict[pairChromPositions] = 0
	
	pairsFile.close()
	return [positionPairsDict, chromList, positionStartMax, positionEndMin]


def getNumReadsPerPositionPair(readsFileNameListFileName, pairsFileName):
	# Get the number of reads at each pair of positions
	# ASSUMES THAT READS HAVE NO INDELS
	[positionPairsDict, chromList, positionStartMax, positionEndMin] = makePositionPairsDict(pairsFileName)
	positionPairs = positionPairsDict.keys()
	readsFileNameListFile = open(readsFileNameListFileName)
	
	for readsFileName in readsFileNameListFile:
		# Iterate through the files with the reads and increment the positions for each read in each file
		print readsFileName.strip()
		readsFile = open(readsFileName.strip())
		
		for line in readsFile:
			# Iterate through the reads and increment every position for every read
			if line[0] == "@":
				# The line is a header, so continue
				continue
			
			[bismarkChrom, bismarkPosition, bismarkSequenceLength] = processBismarkSamLineShort(line.strip())
			if ((bismarkChrom == "") or (bismarkChrom not in chromList)) or ((bismarkPosition > positionStartMax) or (bismarkPosition + bismarkSequenceLength < positionEndMin)):
				# The current read maps to mitochondrial DNA or an unknown region or a chromosome that is not in any of the pairs
				continue
			
			for pp in positionPairs:
				# Iterate through the pairs of positions and add one for each position in each read
				if pp[0] == bismarkChrom:
					# The read is on the same chromosome as the current position pair
					if (pp[1] >= bismarkPosition) and (pp[2] < bismarkPosition + bismarkSequenceLength):
						# The position pair is in the current read, so increment its counts
						positionPairsDict[pp] = positionPairsDict[pp] + 1
		readsFile.close()
	readsFileNameListFile.close()
	return positionPairsDict

	
def outputPositionPairsDict(positionPairsDict, outputFileName):
	# Output the number of reads at each position, making a separate file for each chromosome
	positionPairs = positionPairsDict.keys()
	outputFile = open(outputFileName, 'w+')
	
	for pp in positionPairs:
		# Iterate through the pairs of positions and output the number of reads that overlap each pair
		outputFile.write(pp[0] + "\t" + str(pp[1]) + "\t" + str(pp[2]) + "\t" + str(positionPairsDict[pp]) + "\n")
	outputFile.close()


if __name__=="__main__":
	import sys
	readsFileNameListFileName = sys.argv[1]
	# Each Sam in readsFileNameListFile file has the following important columns:
	# 3.  Chromosome
	# 4.  Start of current read
	# 10.  Sequence
	pairsFileName = sys.argv[2]
	outputFileName = sys.argv[3]

	positionPairsDict = getNumReadsPerPositionPair(readsFileNameListFileName, pairsFileName)
	outputPositionPairsDict(positionPairsDict, outputFileName)