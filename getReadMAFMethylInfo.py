def makeIntList(intFileName):
	# Make a list of ints from a file
	intFile = open(intFileName)
	intList = []
	
	for line in intFile:
		# Iterate through the lines of the file and make a new int for the int in each line
		intList.append(int(line.strip()))
		
	intFile.close()
	return intList

	
def processSNPMethylPlusLine(SNPMethylPlusLine):
	# Get the location information of a SNP, C pair on a line from the SNPMethylPlusFile
	SNPMethylPlusLineElements = SNPMethylPlusLine.split("\t")
	
	SNPMethylPlusSNPLocation = (SNPMethylPlusLineElements[1], int(SNPMethylPlusLineElements[2]))
	SNPMethylPlusMethylLocation = (SNPMethylPlusLineElements[4], int(SNPMethylPlusLineElements[5]))
	return [SNPMethylPlusLineElements, SNPMethylPlusSNPLocation, SNPMethylPlusMethylLocation]
	
	
def getReadMAFMethylInfo(SNPMethylEffectSizesFileName, SNPMethylPlusFileName, effectSizesLinesFileName, outputFileName):
	# Get the number of reads, MAF, and number of reads for a list of SNP, C pairs, where the pair indexes correspond to the lines in the effect sizes file
	effectSizesLines = []
	if len(effectSizesLinesFileName) > 0:
		# There are specific lines of interest
		effectSizesLines = makeIntList(effectSizesLinesFileName) # ASSUMES THAT THESE ARE 1-INDEXED
	SNPMethylEffectSizesFile = open(SNPMethylEffectSizesFileName)
	SNPMethylPlusFile = gzip.open(SNPMethylPlusFileName)
	[SNPMethylPlusLineElements, SNPMethylPlusSNPLocation, SNPMethylPlusMethylLocation] = processSNPMethylPlusLine(SNPMethylPlusFile.readline())
	outputFile = open(outputFileName, 'w+')
	count = 0
	
	for line in SNPMethylEffectSizesFile:
		# Iterate through the SNP, C pairs and find the information for those in the list
		count = count + 1 # INCREMENTING count AT BEGINNING BECAUSE ASSUMING effectSizesLines IS 1-INDEXED
		
		if len(effectSizesLinesFileName) > 0:
			# There are specific lines of interest
			if count not in effectSizesLines:
				# The current SNP, C is not in the list
				continue
		
		lineElements = line.strip().split("\t")
		SNPLocation = (lineElements[0], int(lineElements[1]))
		methylLocation = (lineElements[2], int(lineElements[3]))
		
		while methylLocation[0] > SNPMethylPlusMethylLocation[0]:
			# Iterate through the SNP methylation file until the correct chromosome has been reached
			[SNPMethylPlusLineElements, SNPMethylPlusSNPLocation, SNPMethylPlusMethylLocation] = processSNPMethylPlusLine(SNPMethylPlusFile.readline())
		while methylLocation[1] > SNPMethylPlusMethylLocation[1]:
			# Iterate through the SNP methylation file until the correct methylation location has been reached
			[SNPMethylPlusLineElements, SNPMethylPlusSNPLocation, SNPMethylPlusMethylLocation] = processSNPMethylPlusLine(SNPMethylPlusFile.readline())
		while SNPLocation[1] > SNPMethylPlusSNPLocation[1]:
			# Iterate through the SNP methylation file until the correct SNP location has been reached (assumes that SNP and methylation chromsomes are the same)
			[SNPMethylPlusLineElements, SNPMethylPlusSNPLocation, SNPMethylPlusMethylLocation] = processSNPMethylPlusLine(SNPMethylPlusFile.readline())
			
		# ASSUMES THAT EVERY SNP, C PAIR IN SNPMethylEffectSizesFile IS ALSO IN SNPMethylPlusFile AND BOTH FILES ARE SORTED BY METHYL. THEN SNP
		currentSNPs = []
		currentMethyls = []
		while ((methylLocation[0] == SNPMethylPlusMethylLocation[0]) and (methylLocation[1] == SNPMethylPlusMethylLocation[1])) and ((SNPLocation[0] == SNPMethylPlusSNPLocation[0]) and (SNPLocation[1] == SNPMethylPlusSNPLocation[1])):
			# Iterate through the reads for the current SNP, C pair and add to their SNP and methylation information
			currentSNPs.append(round(float(SNPMethylPlusLineElements[3]))) # ASSUMES ONLY PERFECT LD EXPANSION
			currentMethyls.append(round(float(SNPMethylPlusLineElements[6]))) # ASSUMES ONLY PERFECT LD EXPANSION
			[SNPMethylPlusLineElements, SNPMethylPlusSNPLocation, SNPMethylPlusMethylLocation] = processSNPMethylPlusLine(SNPMethylPlusFile.readline())
			
		numReads = len(currentSNPs)
		if numReads == 0:
			print line
			print SNPMethylPlusLineElements
		MAF = float(currentSNPs.count(1))/float(numReads)
		if MAF > 0.5:
			# MAF is 1 minus the current allele frequency
			MAF = 1 - MAF
		methylFreq = float(currentMethyls.count(1))/float(numReads)
		if methylFreq > 0.5:
			# The minor methylation situation is 1 minus the current methylation situation
			methylFreq = 1 - methylFreq
		outputFile.write(SNPLocation[0] + "\t" + str(SNPLocation[1]) + "\t" + methylLocation[0] + "\t" + str(methylLocation[1]) + "\t" + lineElements[4] + "\t" + str(numReads) + "\t" + str(MAF) + "\t" + str(methylFreq) + "\n")
	outputFile.close()


if __name__=="__main__":
	import sys
	import gzip
	SNPMethylEffectSizesFileName = sys.argv[1] # Should NOT end with .gz
	SNPMethylPlusFileName = sys.argv[2] # Should end with .gz
	outputFileName = sys.argv[3] # Should NOT end with .gz
	effectSizesLinesFileName = ""
	if len(sys.argv) > 4:
		# Specific lines have been selected
		effectSizesLinesFileName = sys.argv[4]
	
	getReadMAFMethylInfo(SNPMethylEffectSizesFileName, SNPMethylPlusFileName, effectSizesLinesFileName, outputFileName)