def getNumReadsInfo(numReadsLine, numReadsCol):
	# Get the location and number of reads for the current line with a number of reads for a position
	if numReadsLine == "":
		# At the end of the file
		return [("", 0, 0), True]
	numReadsLineElements = numReadsLine.strip().split("\t")
	numReadsInfo = (numReadsLineElements[0], int(numReadsLineElements[1]), int(numReadsLineElements[numReadsCol]))
	return [numReadsInfo, False]

def filterNumReads(numReadsFileName, regionsFileName, outputFileName, numReadsCol):
	# Selects numbers of reads from numReadsFile for positions within the regions in regionsFile
	# ASSUMES THAT numReadsFile AND regionsFile ARE SORTED BY CHROM, START
	# INCLUDES ALL BASES IN regionsFile, INCLUDING THE START AND END
	numReadsFile = open(numReadsFileName)
	regionsFile = open(regionsFileName)
	outputFile = open(outputFileName, 'w+')
	[numReadsInfo, numReadsFileEnd] = getNumReadsInfo(numReadsFile.readline(), numReadsCol)
	for line in regionsFile:
		# Iterate through the regions in regionsFile and record the numbers of reads information for the positions in numReadsFile
		lineElements = line.strip().split("\t")
		while numReadsInfo[0] < lineElements[0]:
			# Iterate through the numbers of reads until the right chromosome is reached
			[numReadsInfo, numReadsFileEnd] = getNumReadsInfo(numReadsFile.readline(), numReadsCol)
			if numReadsFileEnd == True:
				# At the end of numReadsFile, so stop
				break
		if numReadsFileEnd == True:
			# At the end of numReadsFile, so stop
			break
		while (numReadsInfo[1] < int(lineElements[1])) and (numReadsInfo[0] == lineElements[0]):
			# Iterate through the numbers of reads until the right chromosome is reached
			[numReadsInfo, numReadsFileEnd] = getNumReadsInfo(numReadsFile.readline(), numReadsCol)
			if numReadsFileEnd == True:
				# At the end of numReadsFile, so stop
				break
		if numReadsFileEnd == True:
			# At the end of numReadsFile, so stop
			break
		while (numReadsInfo[0] == lineElements[0]) and ((numReadsInfo[1] >= int(lineElements[1])) and ((numReadsInfo[1] <= int(lineElements[2])))):
			outputFile.write(numReadsInfo[0] + "\t" + str(numReadsInfo[1]) + "\t" + str(numReadsInfo[2]) + "\n")
			[numReadsInfo, numReadsFileEnd] = getNumReadsInfo(numReadsFile.readline(), numReadsCol)
			if numReadsFileEnd == True:
				# At the end of numReadsFile, so stop
				break
		if numReadsFileEnd == True:
			# At the end of numReadsFile, so stop
			break
	numReadsFile.close()
	regionsFile.close()
	outputFile.close()
	
if __name__=="__main__":
   import sys
   numReadsFileName = sys.argv[1] 
   regionsFileName = sys.argv[2]
   outputFileName = sys.argv[3]
   numReadsCol = int(sys.argv[4])
   filterNumReads(numReadsFileName, regionsFileName, outputFileName, numReadsCol)
	