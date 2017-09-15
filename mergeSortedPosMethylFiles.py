def getMethylInfo(line, isTop, CGDist):
	# Get the information for the methylation of the current C
	methylLineElements = line.strip().split()
	isMethyl = False
	if methylLineElements[1] == "+":
		# The current location is methylated
		isMethyl = True
	if isTop == True:
		# On the top strand, so do not need to correct the C position
		return (methylLineElements[2], int(methylLineElements[3]), isMethyl)
	else:
		return (methylLineElements[2], int(methylLineElements[3]) - CGDist, isMethyl)

def getNextMethylLocation(currentMethylList, methylFileCompleted):
	# Get the earliest methylation location left in the files
	firstNonCompleted = methylFileCompleted.index(False)
	currentChrom = currentMethylList[firstNonCompleted][0]
	currentPosition = currentMethylList[firstNonCompleted][1]
	currentMethylStateList = [currentMethylList[firstNonCompleted][2]]
	currentMethylFileNumList = [firstNonCompleted]
	for i in range(firstNonCompleted + 1, len(currentMethylList)):
		# Find the first chromosome and position
		if methylFileCompleted[i] == True:
			# At the end of the current methylation file, so skip it
			continue
		currentMethyl = currentMethylList[i]
		if (currentMethyl[0] < currentChrom) or ((currentMethyl[0] == currentChrom) and  (currentMethyl[1] < currentPosition)):
			# The current location comes before the earliest location so far
			currentChrom = currentMethyl[0]
			currentPosition = currentMethyl[1]
			currentMethylStateList = [currentMethyl[2]]
			currentMethylFileNumList = [i]
		elif (currentMethyl[0] == currentChrom) and  (currentMethyl[1] == currentPosition):
			# Another read with the current methylation status has been found
			currentMethylStateList.append(currentMethyl[2])
			currentMethylFileNumList.append(i)
	return [currentChrom, currentPosition, currentMethylStateList, currentMethylFileNumList]

def countNumMethyl(currentChrom, currentPosition, currentMethylStateList, currentMethylFileNumList, currentMethylList, methylFileList, methylFileCompleted, isTopList, outputFile, CGDist):
	# Count the number of times the current C is methylated
	while len(currentMethylFileNumList) > 0:
		# Find all of the reads with the current C
		methylFileNumToRemoveList = []
		for methylFileNum in currentMethylFileNumList:
			# Check if the next read from each file with the current C is the same C
			methylLine = methylFileList[methylFileNum].readline()
			if methylLine == "":
				# At the end of the current file
				methylFileCompleted[methylFileNum] = True
				methylFileNumToRemoveList.append(methylFileNum)
				currentMethylList[methylFileNum] = ("", 0, False)
				continue
			currentMethylList[methylFileNum] = getMethylInfo(methylLine, isTopList[methylFileNum], CGDist)
			if (currentMethylList[methylFileNum][0] != currentChrom) or (currentMethylList[methylFileNum][1] != currentPosition):
				# No longer at the current C
				methylFileNumToRemoveList.append(methylFileNum)
				continue
			currentMethylStateList.append(currentMethylList[methylFileNum][2])
		for methylFileNumToRemove in methylFileNumToRemoveList:
			# Remove each file number for which the file is no longer at the current C
			currentMethylFileNumList.remove(methylFileNumToRemove)
	numMethyl = currentMethylStateList.count(True)
	numReads = len(currentMethylStateList)
	fracMethyl = float(numMethyl)/float(numReads)
	outputFile.write(currentChrom + "\t" + str(currentPosition) + "\t" + str(numMethyl) + "\t" + str(numReads) + "\t" + str(fracMethyl) + "\n")
	return [currentMethylList, methylFileCompleted]

def mergeSortedPosMethylFiles (methylFileNameListFileName, outputFileName, CGDist):
	# Determine the number and fraction of times each C is methylated across a list of files
	# ASSUMES THAT EACH METHYLATION FILE IS SORTED BY CHROMOSOME, POSITION
	# outputFile will contain the following columns:
	# 1.  Chromosome
	# 2.  Position
	# 3.  Number of methylated reads
	# 4.  Number of reads
	# 5.  Fraction of methylated reads
	methylFileNameListFile = open(methylFileNameListFileName)
	methylFileList = []
	currentMethylList = []
	methylFileCompleted = []
	isTopList = []
	for methylFileName in methylFileNameListFile:
		# Open each methylation file
		if "_OB" in methylFileName:
			# On the bottom strand
			isTopList.append(False)
		else:
			isTopList.append(True)
		methylFile = gzip.open(methylFileName.strip())
		methylFileList.append(methylFile)
		currentMethylList.append(getMethylInfo(methylFile.readline(), isTopList[-1], CGDist))
		methylFileCompleted.append(False)
	methylFileNameListFile.close()
	outputFile = open(outputFileName, 'w+')
	while methylFileCompleted.count(True) < len(methylFileCompleted):
		# Count the number of times each C in any of the files is methylated
		[currentChrom, currentPosition, currentMethylStateList, currentMethylFileNumList] = getNextMethylLocation(currentMethylList, methylFileCompleted)
		[currentMethylList, methylFileCompleted] = countNumMethyl(currentChrom, currentPosition, currentMethylStateList, currentMethylFileNumList, currentMethylList, methylFileList, methylFileCompleted, isTopList, outputFile, CGDist)
	for methylFile in methylFileList:
		# Close all of the methylation files
		methylFile.close()
	outputFile.close()
	
if __name__=="__main__":
   import sys
   import gzip
   methylFileNameListFileName = sys.argv[1] 
   outputFileName = sys.argv[2]
   CGDist = int(sys.argv[3]) # 1 for CpGs, 2 for CHGs, 0 for CHHs
   mergeSortedPosMethylFiles (methylFileNameListFileName, outputFileName, CGDist)