def makeMethylationDict(methylationSitesFileName):
	# Make a dictionary of methylation sites (ASSUMES NOT MANY SITES)
	# Each key is a tuple with (chromosome, location), and each value is an array with [methylated reads, total reads]
	methylationSitesFile = open(methylationSitesFileName)
	methylationSitesDict = {}
	for line in methylationSitesFile:
		# Iterate through the methylated sites and initialize an entry in the dictionary for each
		lineElements = line.split("\t")
		location = (lineElements[0], int(lineElements[1]))
		methylationSitesDict[location] = [0, 0]
	methylationSitesFile.close()
	return methylationSitesDict

def getMethylationCounts(methylationFileNameListFileName, methylationSitesFileName, methylMark):
	# Find the fraction of reads for each site that are methylated
	methylationSitesDict = makeMethylationDict(methylationSitesFileName)
	methylationFileNameListFile = open(methylationFileNameListFileName)
	for methylationFileName in methylationFileNameListFile:
		# Iterate through files and count the methylated sites in each
		print methylationFileName
		methylationFile = open(methylationFileName.strip())
		methylationFile.readline() # Remove the header
		for line in methylationFile:
			# Iterate through the lines with the methylation information and increment the appropriate counts
			lineElements = line.split("\t")
			location = (lineElements[2], int(lineElements[3]))
			if location not in methylationSitesDict:
				# The location is not a location of interest, so skip it
				continue
			if lineElements[4].strip() == methylMark:
				# The current CpG is methylated
				methylStatus = True
				methylationSitesDict[location][0] = methylationSitesDict[location][0] + 1
			methylationSitesDict[location][1] = methylationSitesDict[location][1] + 1
		methylationFile.close()
	methylationFileNameListFile.close()
	return methylationSitesDict

def outputMethylationCounts(methylationSitesFileName, methylationSitesDict, outputFileName):
	# Output the number of methylated sites for each location
	outputFile = open(outputFileName, 'w+')
	methylationSitesFile = open(methylationSitesFileName)
	for line in methylationSitesFile:
		# Iterate through the methylated sites and initialize an entry in the dictionary for each
		lineElements = line.split("\t")
		location = (lineElements[0], int(lineElements[1]))
		numMethylatedReads = methylationSitesDict[location][0]
		numReads = methylationSitesDict[location][1]
		fracMethylatedReads = 0
		if numReads > 0:
			# Compute the fraction of methylated reads
			fracMethylatedReads = float(numMethylatedReads)/float(numReads)
		outputFile.write(location[0] + "\t" + str(location[1]) + "\t" + str(fracMethylatedReads) + "\t" + str(numMethylatedReads) + "\t" + str(numReads) + "\n")
	outputFile.close()
	methylationSitesFile.close()

if __name__=="__main__":
	import sys
	methylationFileNameListFileName = sys.argv[1]
	methylationSitesFileName = sys.argv[2]
	methylMark = sys.argv[3] # Z for CpGs
	outputFileName = sys.argv[4]
	methylationSitesDict = getMethylationCounts(methylationFileNameListFileName, methylationSitesFileName, methylMark)
	outputMethylationCounts(methylationSitesFileName, methylationSitesDict, outputFileName)
