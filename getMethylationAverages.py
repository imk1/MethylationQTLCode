def getIndivdiualsIndexes(individualsList, individualsFileName):
	# Gets the indexes of the individuals in the list that are in the file with the list of individuals of interest
	individualsIndexes = []
	individualsFile = open(individualsFileName)
	for line in individualsFile:
		# Iterate through the individuals and add each individual's index to the list
		if line.strip() in individualsList:
			# The current individual is in the list of individuals with methylation data
			individualsIndexes.append(individualsList.index(line.strip()))
	individualsFile.close()
	print len(individualsIndexes)
	return individualsIndexes

def makeStringList(StringFileName):
	# Make a list of Strings from a file
	StringFile = open(StringFileName)
	StringList = []
	for line in StringFile:
		# Iterate through the Strings in the file and add each to the list
		StringList.append(line.strip())
	return StringList

def getMethylationAverages(methylationFileName, methylationIDsFileName, individualsFileName):
	# Gets the average methylation for each of the desired locations across the desired inviduals
	methylationFile = open(methylationFileName) # ASSUMES THAT THIS IS A GSE*_matrix_processed.txt FILE
	individualsLine = methylationFile.readline()
	individualsInfo = individualsLine.split("\t") # ASSUMES TAB BETWEEN INDIVIDUAL IDENTIFIERS
	print len(individualsInfo)
	individualsList = []
	for i in range(1, len(individualsInfo)):
		# Iterate through the individuals and add each of their IDs to the list
		# ASSUMES THAT FIRST ENTRY DOES NOT CONTAIN AN INDIVIDUAL ID
		# ASSUMES THAT EACH ID IS REPEATED CONSECUTIVELY
		if i % 2 == 0:
			# At a repeated ID, so skip it
			continue
		individualID = individualsInfo[i]
		individualsList.append(individualID)
	individualsIndexes = getIndivdiualsIndexes(individualsList, individualsFileName)
	methylationIDsList = makeStringList(methylationIDsFileName)
	methylationAveragesList = []
	for methylationID in methylationIDsList:
		# Initialize methylation averages to be -1
		methylationAveragesList.append(-1)
	for line in methylationFile:
		# Iterates through lines with methylation data and finds the average for each site of interest
		lineElements = line.split("\t") # ASSUMES THAT THERE IS A TAB BETWEEN EACH ELEMENT
		if lineElements[0] not in methylationIDsList:
			# The current ID is not of interest, so skip it
			continue
		methylationIDsIndex = methylationIDsList.index(lineElements[0])
		betasList = []
		for index in individualsIndexes:
			# Iterate through the individuals and put each of their methylations in the array
			# ASSUMES THAT THE FIRST ELEMENT IS THE ID AND THAT ALL OTHER ODD ELEMENTS ARE NOT BETAS
			betaString = lineElements[(2*index) + 1]
			if betaString != "":
				# Beta was measured for the current methylation ID, individual ID
				betasList.append(float(betaString))
		methylationAverage = numpy.average(betasList)
		methylationAveragesList[methylationIDsIndex] = methylationAverage
	return methylationAveragesList

def outputNums(numsList, outputFileName):
	# Writes numbers to a file
	outputFile = open(outputFileName, 'w+')
	for num in numsList:
		# Iterate through the numbers and write each to the output file
		outputFile.write(str(num) + "\n")
	outputFile.close()

if __name__=="__main__":
	import sys
	import numpy
	methylationFileName = sys.argv[1]
	methylationIDsFileName = sys.argv[2]
	individualsFileName = sys.argv[3]
	outputFileName = sys.argv[4]
	methylationAveragesList = getMethylationAverages(methylationFileName, methylationIDsFileName, individualsFileName)
	outputNums(methylationAveragesList, outputFileName)

