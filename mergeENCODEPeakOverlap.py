def mergeENCODEPeakOverlap(ENCODEPeakOverLapFileNameListFileName, outputCountsFileName):
	# Merge the ENCODE overlap files and count the number of overlaps in each file
	ENCODEPeakOverLapFileNameListFile = open(ENCODEPeakOverLapFileNameListFileName)
	outputJoinList = []
	outputCountsFile = open(outputCountsFileName, 'w+')
	
	for ENCODEPeakOverLapFileName in ENCODEPeakOverLapFileNameListFile:
		# Iterate through the ENCODE peak overlaps, add each binary vector to the join list, and record the sum of each binary vector
		ENCODEPeakOverLapFile = open(ENCODEPeakOverLapFileName.strip())
		currentJoinList = []
		for line in ENCODEPeakOverLapFile:
			# Iterate for the ENCODE data and store whether the peak overlaps for each of the SNPs
			lineElements = line.strip().split("\t")
			currentJoinList.append(int(lineElements[2]))
		
		numSNPsOverlap = sum(currentJoinList)
		outputCountsFile.write(ENCODEPeakOverLapFileName.strip() + "\t" + str(numSNPsOverlap) + "\n")
		outputJoinList.append(currentJoinList)
	
	ENCODEPeakOverLapFileNameListFile.close()
	outputCountsFile.close()
	return outputJoinList


def recordJoinList(outputJoinList, outputJoinListFileName):
	# Record each element of outputJoinList as a column in outputJoinListFile
	outputJoinFile = open(outputJoinListFileName, 'w+')
	
	for i in range(len(outputJoinList[0])):
		# Iterate through the rows of each element in outputJoinList, and record the number in each row to the output file
		for j in range(len(outputJoinList)):
			# Iterate through the elements of outputJoinList and write the number at the current row of each element to the output file
			outputJoinFile.write(str(outputJoinList[j][i]) + "\t")
		outputJoinFile.write("\n")
	outputJoinFile.close()


if __name__=="__main__":
	import sys
	import math
	ENCODEPeakOverLapFileNameListFileName = sys.argv[1]
	outputCountsFileName = sys.argv[2]
	outputJoinListFileName = sys.argv[3]
	
	outputJoinList = mergeENCODEPeakOverlap(ENCODEPeakOverLapFileNameListFileName, outputCountsFileName)
	recordJoinList(outputJoinList, outputJoinListFileName)