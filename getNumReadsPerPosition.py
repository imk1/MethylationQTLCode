def processBismarkSamLineShort(bismarkSamLine):
	# Get the chromosome, position on chromosome, direction in which to iterate, and sequence from a line of a sam file
	# Direction = True means iterate through the sequence in the fowards direction (position is the first base)
	# Direction = False means iterate through the sequence in the backwards direction (position is the last base)
	bismarkSamLineElements = bismarkSamLine.split("\t")
	if ("_" in bismarkSamLineElements[2]) or ("chrM" in bismarkSamLineElements[2]):
		# The read maps to an unknown chromosome or mitochondrial DNA
		return ["", int(bismarkSamLineElements[3]), len(bismarkSamLineElements[9])]

	bismarkChrom = bismarkSamLineElements[2][3:]
	return [bismarkChrom, int(bismarkSamLineElements[3]), len(bismarkSamLineElements[9])]


def makePositionDict(chromLengthsFileName):
	# Make an array for each chromosome that has a 0 for each position
	positionDict = {}
	chromLengthsFile = open(chromLengthsFileName)
	
	for line in chromLengthsFile:
		# Iterate through the chromosomes and make an entry in the dictionary for each
		lineElements = line.strip().split("\t")
		positionDict[lineElements[0]] = []
		for i in range(int(lineElements[1])):
			# Add a 0 to the chromosomes entry for each position
			positionDict[lineElements[0]].append(0)
	
	chromLengthsFile.close()
	return positionDict


def getNumReadsPerPosition(readsFileNameListFileName, chromLengthsFileName):
	# Get the number of reads at each position
	# ASSUMES THAT READS HAVE NO INDELS
	positionDict = makePositionDict(chromLengthsFileName)
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
			if bismarkChrom == "":
				# The current read maps to mitochondrial DNA or an unknown region
				continue
			
			for i in range(bismarkPosition, bismarkPosition + bismarkSequenceLength):
				# Increment the counts for each position
				positionDict[bismarkChrom][i] = positionDict[bismarkChrom][i] + 1
		readsFile.close()
	readsFileNameListFile.close()
	return positionDict

	
def outputPositionDict(positionDict, outputFileNamePath, outputFileNameSuffix):
	# Output the number of reads at each position, making a separate file for each chromosome
	chromList = positionDict.keys()
	
	for chrom in chromList:
		# Iterate through the chromosomes and output the number of reads at each location for each
		outputFileName = outputFileNamePath + "/" + "chr" + chrom + "_" + outputFileNameSuffix
		outputFile = open(outputFileName, 'w+')
		
		for numReads in positionDict[chrom]:
			# Record the number of reads at each position
			outputFile.write(str(numReads) + "\n")
		outputFile.close()


if __name__=="__main__":
	import sys
	readsFileNameListFileName = sys.argv[1]
	# Each Sam in readsFileNameListFile file has the following important columns:
	# 3.  Chromosome
	# 4.  Start of current read
	# 10.  Sequence
	chromLengthsFileName = sys.argv[2]
	outputFileNamePath = sys.argv[3] # Should not end with /
	outputFileNameSuffix = sys.argv[4] # Should not start with _

	positionDict = getNumReadsPerPosition(readsFileNameListFileName, chromLengthsFileName)
	outputPositionDict(positionDict, outputFileNamePath, outputFileNameSuffix)