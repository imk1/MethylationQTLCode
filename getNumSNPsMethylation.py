def makeIntDict(intDictFileName):
	# Make a dictionary from pairs of ints in a file
	intDictFile = open(intDictFileName)
	intDict = {}
	
	for line in intDictFile:
		# Iterate through the lines of the int dictionary file and enter each into the dictionary
		lineElements = line.strip().split("\t")
		intDict[int(lineElements[0])] = int(lineElements[1])
		
	intDictFile.close()
	return intDict


def sufficientMinor(numFirst, numSecond, vecLen, minReadsCutoffSingleMinor, readsToMinMinorReads):
	# Compute if there are enough reads with the minor allele or methylation state
	if vecLen >= minReadsCutoffSingleMinor:
		# Need only 1 minor allele or methylation state for a significant p-value to be possible
		if (numFirst > 0) and (numSecond > 0):
			# There are enough reads for a significant p-value to be possible
			return True
		else:
			return False
	
	else: #Y
		minMinorReads = readsToMinMinorReads[vecLen]
		if (numFirst >= minMinorReads) and (numSecond >= minMinorReads): #Y
			# There are enough reads for a significant p-value to be possible
			return True
	return False


def outputNumSNPsMethylation(SNP, methyl, SNPVec, methylVec, minReadsCutoff, minReadsCutoffSingleMinor, readsToMinMinorReads, numSNPsMethylFile):
	# Compute and output the number of reads for each combination of allele and methylation status if the reads, MAF, and methylation cutoffs are satisfied
	# Round SNP counts to the nearest Natural Number
	vecLen = len(methylVec)
	if vecLen >= minReadsCutoff: #Y
		# The minimum reads cutoff is satisfied
		numAltAlleles = sum(SNPVec)
		numRefAlleles = vecLen - numAltAlleles
		if sufficientMinor(numRefAlleles, numAltAlleles, vecLen, minReadsCutoffSingleMinor, readsToMinMinorReads) == True: #Y
			# Both alleles have sufficiently high numbers of reads
			numMethyl = methylVec.count(1)
			numUnmethyl = methylVec.count(0)
			if  sufficientMinor(numMethyl, numUnmethyl, vecLen, minReadsCutoffSingleMinor, readsToMinMinorReads) == True: #Y
				# C is methylated and unmethylated a sufficient fraction of the time
				numRefMethyl = 0
				numAltMethyl = 0
				numRefUnmethyl = 0
				numAltUnmethyl = 0
				for i in range(vecLen): #Y
					# Iterate through the SNP and methylation vectors and count the number of SNP, C pairs in each category
					if methylVec[i] == 1: #Y
						# The SNP is methylated
						numAltMethyl = numAltMethyl + SNPVec[i]
						numRefMethyl = numRefMethyl + (1 - SNPVec[i])
					elif methylVec[i] == 0: #Y
						# The SNP is unmethylated
						numAltUnmethyl = numAltUnmethyl + SNPVec[i]
						numRefUnmethyl = numRefUnmethyl + (1 - SNPVec[i])
					else:
						print methylVec[i]
						print "Problem!"
				numSNPsMethylFile.write(SNP[0] + "\t" + str(SNP[1]) + "\t" + methyl[0] + "\t" + str(methyl[1]) + "\t" + str(round(numRefMethyl))+ "\t" + str(round(numAltMethyl)) + "\t" + str(round(numRefUnmethyl)) + "\t" + str(round(numAltUnmethyl)) + "\n")


def getNumSNPsMethylation(SNPMethylFileName, numSNPsMethylFileName, readsToMinMinorReads):
	# Get the number of reads for each allele, methylation status combination
	# ASSUMES THAT SNPMethylFile IS SORTED BY METHYLATION CHROM., METHYLATION POSITION, SNP CHROM., SNP POSITION
	# numSNPsMethylFile will have the following information:
	# 1.  SNP chromosome
	# 2.  SNP position in chromosome
	# 3.  Methylation chromosome
	# 4.  Methylation position in chromosome
	# 5.  Number of occurences of reference allele, methylated
	# 6.  Number of occurences of alternate allele, methylated
	# 7.  Number of occurences of reference allele, unmethylated
	# 8.  Number of occurences of alternate allele, unmethylated
	# Excludes SNP, methylation pairs that do not have at least the minimum number of reads with the minor allele and methylation status for their number of reads
	SNPMethylFile = gzip.open(SNPMethylFileName, 'rb')
	numSNPsMethylFile = open(numSNPsMethylFileName, 'wb')
	numSNPsMethylFile.write("SNP chr\tSNP pos\tCpG chr\tCpG pos\tNum ref, methyl\tNum alt, methyl\tNum ref, unmethyl\tNum alt, unmethyl\n")
	minReadsCutoff = min(readsToMinMinorReads.keys())
	minReadsCutoffSingleMinor = max(readsToMinMinorReads.keys()) + 1
	lastSNP = ("", 0)
	lastMethyl = ("", 0)
	SNPVec = []
	methylVec = []

	for line in SNPMethylFile:
		# Iterate through the lines of the SNP methylation file and compute the number of reads for each combintation for each SNP, C pair
		lineElements = line.strip().split("\t")
		currentSNP = (lineElements[1], int(lineElements[2]))
		currentMethyl = (lineElements[4], int(lineElements[5]))
		if (currentSNP != lastSNP) or (currentMethyl != lastMethyl): #Y
			# At a new SNP or methylation location, so find the number of reads for each combination for the previous one
			outputNumSNPsMethylation(lastSNP, lastMethyl, SNPVec, methylVec, minReadsCutoff, minReadsCutoffSingleMinor, readsToMinMinorReads, numSNPsMethylFile)
			lastSNP = currentSNP
			lastMethyl = currentMethyl
			SNPVec = []
			methylVec = []
		
		SNPVec.append(float(lineElements[3]))
		methylVec.append(int(lineElements[6]))

	outputNumSNPsMethylation(lastSNP, lastMethyl, SNPVec, methylVec, minReadsCutoff, minReadsCutoffSingleMinor, readsToMinMinorReads, numSNPsMethylFile)
	SNPMethylFile.close()
	numSNPsMethylFile.close()


if __name__=="__main__":
	import sys
	import gzip
	SNPMethylFileName = sys.argv[1] # Should end with .gz
	numSNPsMethylFileName = sys.argv[2]
	readsToMinMinorReadsFileName = sys.argv[3]

	readsToMinMinorReads = makeIntDict(readsToMinMinorReadsFileName)
	getNumSNPsMethylation(SNPMethylFileName, numSNPsMethylFileName, readsToMinMinorReads)
