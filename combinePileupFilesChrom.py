def initializePileupFiles(pileupFileNameListFileName, chrom):
	# Make a list of all of the pileup files and their first loations
	pileupFileNameListFile = open(pileupFileNameListFileName)
	pileupFileList = []
	pileupFileLocations = []
	endFileList = []
	chromt = chrom + "\t"
	for line in pileupFileNameListFile:
		# Iterate through the pileup files and open each
		print line
		pileupFileList.append(open(line.strip()))
		pileupLine = pileupFileList[-1].readline()
		while chromt not in pileupLine:
			# Iterate through the pileup file until the correct chromosome is reached
			# ASSUMES THAT ALL FILES HAVE AT LEAST 1 READ ON EACH CHROMOSOME
			pileupLine = pileupFileList[-1].readline()
		pileupLineElements = pileupLine.strip().split("\t")
		pileupFileLocations.append((pileupLineElements[0], int(pileupLineElements[1]), int(pileupLineElements[3])))
		endFileList.append(False)
	pileupFileNameListFile.close()
	return [pileupFileList, pileupFileLocations, endFileList]

def combinePileupFiles(pileupFileList, pileupFileLocations, endFileList, chromLengthsFileName, outputFileName, chromForOutput):
	# Merge pileup files by summing the number of reads for each base in each	
	chromLengthsFile = open(chromLengthsFileName)
	outputFile = open(outputFileName, 'w+')
	for line in chromLengthsFile:
		# Iterate through the chromosomes and count the number of reads at each position
		lineElements = line.strip().split("\t")
		chrom = lineElements[0]
		if chrom != chromForOutput:
			# At the wrong chromosome, so continue
			continue
		print chrom
		chromLength = int(lineElements[1])
		i = 1
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
					pileupLine = pileupFileList[j].readline().strip()
					if pileupLine == "":
						# At the endo of the current pileup file
						endFileList[j] = True
						continue
					pileupLineElements = pileupLine.split("\t")
					pileupFileLocations[j] = (pileupLineElements[0], int(pileupLineElements[1]), int(pileupLineElements[3]))
			outputFile.write(chrom + "\t" + str(i) + "\t" + str(numReads) + "\n")
			i = i + 1
		break
	chromLengthsFile.close()
	outputFile.close()

if __name__=="__main__":
   import sys
   pileupFileNameListFileName = sys.argv[1]
   chromLengthsFileName = sys.argv[2]
   outputFileName = sys.argv[3]
   chrom = sys.argv[4]
   [pileupFileList, pileupFileLocations, endFileList] = initializePileupFiles(pileupFileNameListFileName, chrom)
   combinePileupFiles(pileupFileList, pileupFileLocations, endFileList, chromLengthsFileName, outputFileName, chrom)
