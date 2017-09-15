def processBismarkSamLineShortPlus(bismarkSamLine):
	# Get the chromosome, position on chromosome, direction in which to iterate, and sequence from a line of a sam file
	# Direction = True means iterate through the sequence in the fowards direction (position is the first base)
	# Direction = False means iterate through the sequence in the backwards direction (position is the last base)
	bismarkSamLineElements = bismarkSamLine.strip().split("\t")
	bismarkChrom = bismarkSamLineElements[2]
	return [bismarkChrom, int(bismarkSamLineElements[3]), len(bismarkSamLineElements[9])]

	
def getNumPatternsPerRegion(humanGenomeFileName, pattern):
	# Gets the number of patterns (for example, CpG) in each region of the genome
	# ASSUMES THAT THE NUMBER OF BASES IN EACH LINE (except for headers) IN humanGenomeFile IS regionLength
	# ASSUMES THAT THE FIRST LINE OF humanGenomeFile STARTS WITH >
	patternDict = {}
	regionDict = {}
	humanGenomeFile = open(humanGenomeFileName)
	chrom = ""
	
	for line in humanGenomeFile:
		# Iterate through the human genome and find the number of CpGs in each region
		if line[0] == ">":
			# At the beginning of a new chromosome
			chrom = line.strip()[1:]
			patternDict[chrom] = []
			regionDict[chrom] = []
	
		else:
			sequence = line.strip()
			numPatterns = 0
			for i in range(0, len(sequence) - len(pattern) + 1):
				# Iterate through the bases and find the number of occurrences of the pattern
				if sequence[i:i+len(pattern)] == pattern:
					# An instance of the pattern has been found
					numPatterns = numPatterns + 1
			patternDict[chrom].append(numPatterns)
			regionDict[chrom].append(0)
		
	humanGenomeFile.close()
	return [patternDict, regionDict]


def getNumReadsPerRegion(readsFileNameListFileName, regionDict, regionLength):
	# Get the number of reads at each position in each region
	# ASSUMES THAT READS HAVE NO INDELS
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
			
			[bismarkChrom, bismarkPosition, bismarkSequenceLength] = processBismarkSamLineShortPlus(line.strip())
			if bismarkChrom not in patternDict:
				# The current read maps to an unknown region
				continue
			
			i = bismarkPosition
			while i < bismarkPosition + bismarkSequenceLength:
				# Increment the counts for each position
				currentFloor = int(math.floor(float(i)/float(regionLength))) - 1
				regionDict[bismarkChrom][currentFloor] = regionDict[bismarkChrom][currentFloor] + 1
				i = regionLength * math.floor(float(i + regionLength)/float(regionLength))
		readsFile.close()
	readsFileNameListFile.close()
	return regionDict

	
def outputDictPair(patternDict, regionDict, outputFileNamePath, outputFileNameSuffix):
	# Output the number of patterns and reads in each region, making a separate file for each chromosome
	chromList = patternDict.keys()
	
	for chrom in chromList:
		# Iterate through the chromosomes and output the number of reads at each location for each
		outputFileName = outputFileNamePath + "/" + chrom + "_" + outputFileNameSuffix
		outputFile = open(outputFileName, 'w+')
		
		for i in range(len(patternDict[chrom])):
			# Record the number of reads at each position
			outputFile.write(str(patternDict[chrom][i]) + "\t" + str(regionDict[chrom][i]) + "\n")
		outputFile.close()


if __name__=="__main__":
	import sys
	import math
	readsFileNameListFileName = sys.argv[1]
	# Each Sam in readsFileNameListFile file has the following important columns:
	# 3.  Chromosome
	# 4.  Start of current read
	# 10.  Sequence
	humanGenomeFileName = sys.argv[2]
	pattern = sys.argv[3]
	regionLength = int(sys.argv[4]) # SHOULD BE THE LENGTH OF A LINE IN THE FASTA FILE (80 for HumanGenomeMaskedYRI/hg19MaskedYRIchrAll.fasta)
	outputFileNamePath = sys.argv[5] # Should not end with /
	outputFileNameSuffix = sys.argv[6] # Should not start with _

	[patternDict, regionDict] = getNumPatternsPerRegion(humanGenomeFileName, pattern)
	regionDict = getNumReadsPerRegion(readsFileNameListFileName, regionDict, regionLength)
	outputDictPair(patternDict, regionDict, outputFileNamePath, outputFileNameSuffix)