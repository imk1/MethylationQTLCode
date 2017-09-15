def initializePileupFiles(pileupFileNameListFileName):
	# Make a list of all of the pileup files and their first loations
	pileupFileNameListFile = open(pileupFileNameListFileName)
	pileupFileList = []
	pileupFileLocations = []
	endFileList = []
	for line in pileupFileNameListFile:
		# Iterate through the pileup files and open each
		pileupFileList.append(open(line.strip()))
		pileupLine = pileupFileList[-1].readline()
		pileupLineElements = pileupLine.split("\t")
		pileupFileLocations.append((pileupLineElements[0], int(pileupLineElements[1]), int(pileupLineElements[3])))
		endFileList.append(False)
	pileupFileNameListFile.close()
	return [pileupFileList, pileupFileLocations, endFileList]

def combinePileupFiles(pileupFileList, pileupFileLocations, endFileList, chromLengthsFileName, outputFileName):
	# Merge pileup files by summing the number of reads for each base in each	
	chromLengthsFile = open(chromLengthsFileName)
	outputFile = open(outputFileName, 'w+')
	for line in chromLengthsFile:
		# Iterate through the chromosomes and count the number of reads at each position
		lineElements = line.strip().split("\t")
		chrom = lineElements[0]
		print chrom
		chromLength = int(lineElements[1])
		i = 0
		while i < chromLength:
			# Iterate through the chromosome positions and count the number of reads at each
			numReads = 0
			for j in range(len(pileupFileList)):
				# Iterate through the pileup files and add the number of reads at the current location to numReads
				if endFileList[j] == True:
					# At the end of the current file, so skip it
					continue
				if pileupFileLocations[j][0] != chrom:
					# The current file is at the next chromosome, so skip it
					continue
				if pileupFileLocations[j][1] == i:
					# At the correct location, so add the current number of reads
					numReads = numReads + pileupFileLocations[j][2]
					pileupLine = pileupFileList[j].readline()
					if pileupLine == "":
						# At the endo of the current pileup file
						endFileList[j] = True
						continue
					pileupLineElements = pileupLine.split("\t")
					pileupFileLocations[j] = (pileupLineElements[0], int(pileupLineElements[1]), int(pileupLineElements[3]))
			outputFile.write(chrom + "\t" + str(i) + "\t" + str(numReads) + "\n")
			i = i + 1
	chromLengthsFile.close()
	outputFile.close()

if __name__=="__main__":
   import sys
   pileupFileNameListFileName = sys.argv[1] 
   chromLengthsFileName = sys.argv[2]
   outputFileName = sys.argv[3]
   [pileupFileList, pileupFileLocations, endFileList] = initializePileupFiles(pileupFileNameListFileName)
   combinePileupFiles(pileupFileList, pileupFileLocations, endFileList, chromLengthsFileName, outputFileName)
