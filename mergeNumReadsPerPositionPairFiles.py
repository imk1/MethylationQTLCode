def mergeNumReadPerPositionPairFiles(numReadsFileNameListFileName, outputFileName, outputReadsFileListFileName):
	# Add the number of reads in each region from each reads file
	numReadsFileNameListFile = open(numReadsFileNameListFileName)
	outputFile = open(outputFileName, 'w+')
	outputReadsFileListFile = open(outputReadsFileListFileName, 'w+')
	numReadsFileList = []
	for line in numReadsFileNameListFile:
		# Iterate through the files with the numbers of reads and open each
		numReadsFileList.append(open(line.strip()))
	for line in numReadsFileList[0]:
		# Iterate through the reads files and make a line in the script for each and all position files
		lineElements = line.strip().split("\t")
		outputReadsFileListFile.write(lineElements[0] + "\t" + lineElements[1] + "\t" + lineElements[2])
		numReads = int(lineElements[3])
		if int(lineElements[3]) > 0:
			# There is at least one read in the current file
			outputReadsFileListFile.write("\t" + str(0))
		for index in range(1, len(numReadsFileList)):
			# Iterate through the files and add the number of reads from each file
			numReadsFile = numReadsFileList[index]
			numReadsLine = numReadsFile.readline()
			numReadsLineElements = numReadsLine.strip().split("\t")
			numReads = numReads + int(numReadsLineElements[3])
			if int(numReadsLineElements[3]) > 0:
				# There is at least one read in the current file
				outputReadsFileListFile.write("\t" + str(index))
		outputFile.write(lineElements[0] + "\t" + lineElements[1] + "\t" + lineElements[2] + "\t" + str(numReads) + "\t" + lineElements[4] + "\n")
		outputReadsFileListFile.write("\n")
	for numReadsFile in numReadsFileList:
		# Close all of the files with numbers of reads
		numReadsFile.close()
	numReadsFileNameListFile.close()
	outputFile.close()
	outputReadsFileListFile.close()
	
if __name__=="__main__":
	import sys
	numReadsFileNameListFileName = sys.argv[1]
	outputFileName = sys.argv[2]
	outputReadsFileListFileName = sys.argv[3]
	mergeNumReadPerPositionPairFiles(numReadsFileNameListFileName, outputFileName, outputReadsFileListFileName)