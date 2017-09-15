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
	
	else:
		minMinorReads = readsToMinMinorReads[vecLen]
		if (numFirst >= minMinorReads) and (numSecond >= minMinorReads):
			# There are enough reads for a significant p-value to be possible
			return True
	return False


def outputFisherExactRandPlusPlus(SNP, methyl, SNPVec, methylVec, minReadsCutoff, minReadsCutoffSingleMinor, readsToMinMinorReads, SNPMethylFisherExactFile):
	# Compute and output the Fisher's exact test p-values if the reads, MAF, and methylation cutoffs are satisfied
	vecLen = len(methylVec)
	if vecLen >= minReadsCutoff:
		# The minimum reads cutoff is satisfied
		numRefAlleles = SNPVec.count(0)
		numAltAlleles = SNPVec.count(1)
		if sufficientMinor(numRefAlleles, numAltAlleles, vecLen, minReadsCutoffSingleMinor, readsToMinMinorReads) == True:
			# Both alleles have sufficiently high numbers of reads
			numMethyl = methylVec.count(1)
			numUnmethyl = methylVec.count(0)
			if  sufficientMinor(numMethyl, numUnmethyl, vecLen, minReadsCutoffSingleMinor, readsToMinMinorReads) == True:
				# C is methylated and unmethylated in a sufficient number of reads
				random.shuffle(methylVec) #Shuffles the methylation data
				numRefMethyl = 0
				numAltMethyl = 0
				numRefUnmethyl = 0
				numAltUnmethyl = 0
				for i in range(vecLen):
					# Iterate through the SNP and methylation vectors and count the number of SNP, C pairs in each category
					if (SNPVec[i] == 0) and (methylVec[i] == 0):
						# The SNP has the reference allele and the C is unmethylated
						numRefUnmethyl = numRefUnmethyl + 1
					elif (SNPVec[i] == 0) and (methylVec[i] == 1):
						# The SNP has the reference allele and the C is methylated
						numRefMethyl = numRefMethyl + 1
					elif (SNPVec[i] == 1) and (methylVec[i] == 0):
						# The SNP has the alternate allele and the C is unmethylated
						numAltUnmethyl = numAltUnmethyl + 1
					elif (SNPVec[i] == 1) and (methylVec[i] == 1):
						# The SNP has the alternate allele and the C is methylated
						numAltMethyl = numAltMethyl + 1
					else:
						print SNPVec[i]
						print methylVec[i]
						print "Problem!"
				[oddsRatio, pVal] = scipy.stats.fisher_exact([[numRefMethyl, numAltMethyl], [numRefUnmethyl, numAltUnmethyl]])
				SNPMethylFisherExactFile.write(SNP[0] + "\t" + str(SNP[1]) + "\t" + methyl[0] + "\t" + str(methyl[1]) + "\t" + str(pVal) + "\n")


def fisherExactSNPsMethylationRandPlusPlus(SNPMethylFileName, SNPMethylFisherExactFileName, readsToMinMinorReads):
	# Use Fisher's exact test to determine whether the distribution of alleles for methylation statuses is more skewed than would be expected by chance
	# ASSUMES THAT SNPMethylFile IS SORTED BY METHYLATION CHROM., METHYLATION POSITION, SNP CHROM., SNP POSITION
	# SNPMethylFisherExactFile will have the following information:
	# 1.  SNP chromosome
	# 2.  SNP position in chromosome
	# 3.  Methylation chromosome
	# 4.  Methylation position in chromosome
	# 5.  Hypergeometric p-value between genotype and methylation
	# Reference allele will be recorded as 0; alternate allele will be recorded as 1
	# Methylated will be recorded as 1; unmethylated will be recorded as 0
	# Excludes SNP, methylation pairs that do not have at least the minimum number of reads with the minor allele and methylation status for their number of reads
	SNPMethylFile = gzip.open(SNPMethylFileName, 'rb')
	SNPMethylFisherExactFile = open(SNPMethylFisherExactFileName, 'wb')
	minReadsCutoff = min(readsToMinMinorReads.keys())
	minReadsCutoffSingleMinor = max(readsToMinMinorReads.keys()) + 1
	lastSNP = ("", 0)
	lastMethyl = ("", 0)
	SNPVec = []
	methylVec = []
	random.seed()

	for line in SNPMethylFile:
		# Iterate through the lines of the SNP methylation file and compute the hygpergeometric p-value for each SNP, C pair
		lineElements = line.strip().split("\t")
		currentSNP = (lineElements[1], int(lineElements[2]))
		currentMethyl = (lineElements[4], int(lineElements[5]))
		if (currentSNP != lastSNP) or (currentMethyl != lastMethyl):
			# At a new SNP or methylation location, so find the hypergeometric p-value for the previous one
			outputFisherExactRandPlusPlus(lastSNP, lastMethyl, SNPVec, methylVec, minReadsCutoff, minReadsCutoffSingleMinor, readsToMinMinorReads, SNPMethylFisherExactFile)
			lastSNP = currentSNP
			lastMethyl = currentMethyl
			SNPVec = []
			methylVec = []
		
		SNPVec.append(int(lineElements[3]))
		methylVec.append(int(lineElements[6]))

	outputFisherExactRandPlusPlus(lastSNP, lastMethyl, SNPVec, methylVec, minReadsCutoff, minReadsCutoffSingleMinor, readsToMinMinorReads, SNPMethylFisherExactFile)
	SNPMethylFile.close()
	SNPMethylFisherExactFile.close()


if __name__=="__main__":
	import sys
	import scipy
	from scipy import stats
	import gzip
	import random
	SNPMethylFileName = sys.argv[1] # Should end with .gz
	SNPMethylFisherExactFileName = sys.argv[2]
	readsToMinMinorReadsFileName = sys.argv[3]

	readsToMinMinorReads = makeIntDict(readsToMinMinorReadsFileName)
	fisherExactSNPsMethylationRandPlusPlus(SNPMethylFileName, SNPMethylFisherExactFileName, readsToMinMinorReads)
