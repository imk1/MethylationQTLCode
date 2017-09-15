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


def outputCorrPlusPlus(SNP, methyl, SNPVec, methylVec, minReadsCutoff, minReadsCutoffSingleMinor, SNPMethylCorrsFile):
	# Compute and output the correlation if the reads and MAF cutoffs are satisfied
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
				# C is methylated and unmethylated a sufficient fraction of the time
				
				corr = scipy.stats.pearsonr(SNPVec, methylVec)[0] # REQUIRES SCIPY 12+ (scipy 8 maybe o.k.)
				SNPMethylCorrsFile.write(SNP[0] + "\t" + str(SNP[1]) + "\t" + methyl[0] + "\t" + str(methyl[1]) + "\t" + str(corr) + "\n")


def correlateSNPsMethylationPlusPlus(SNPMethylFileName, SNPMethylCorrsFileName, readsToMinMinorReads):
	# Compute the correlation between genotype and methylation
	# ASSUMES THAT SNPMethylFile IS SORTED BY METHYLATION CHROM., METHYLATION POSITION, SNP CHROM., SNP POSITION
	# SNPMethylCorrsFile will have the following information:
	# 1.  SNP chromosome
	# 2.  SNP position in chromosome
	# 3.  Methylation chromosome
	# 4.  Methylation position in chromosome
	# 5.  Correlation between genotype and methylation
	# For each SNP, methylation location pair, there will be a line in SNPVecFile and a line in methylVecFile
	# These lines will contain the SNP/methylation chromosome, position, and vector used in computing the correlation
	# Reference allele will be recorded as 0; alternate allele will be recorded as 1
	# Methylated will be recorded as 1; unmethylated will be recorded as 0
	# Excludes SNP, methylation pairs that do not have at least the minimum number of reads with the minor allele and methylation status for their number of reads
	SNPMethylFile = gzip.open(SNPMethylFileName, 'rb')
	SNPMethylCorrsFile = open(SNPMethylCorrsFileName, 'wb')
	minReadsCutoff = min(readsToMinMinorReads.keys())
	minReadsCutoffSingleMinor = max(readsToMinMinorReads.keys()) + 1
	lastSNP = ("", 0)
	lastMethyl = ("", 0)
	SNPVec = []
	methylVec = []

	for line in SNPMethylFile:
		# Iterate through the lines of the SNP methylation file and compute the correlation for each SNP, C pair
		lineElements = line.strip().split("\t")
		currentSNP = (lineElements[1], int(lineElements[2]))
		currentMethyl = (lineElements[4], int(lineElements[5]))
		if (currentSNP != lastSNP) or (currentMethyl != lastMethyl):
			# At a new SNP or methylation location, so find the correlation for the previous one
			outputCorrPlusPlus(lastSNP, lastMethyl, SNPVec, methylVec, minReadsCutoff, minReadsCutoffSingleMinor, SNPMethylCorrsFile)
			lastSNP = currentSNP
			lastMethyl = currentMethyl
			SNPVec = []
			methylVec = []
		
		SNPVec.append(int(lineElements[3]))
		methylVec.append(int(lineElements[6]))

	outputCorrPlusPlus(lastSNP, lastMethyl, SNPVec, methylVec, minReadsCutoff, minReadsCutoffSingleMinor, SNPMethylCorrsFile)
	SNPMethylFile.close()
	SNPMethylCorrsFile.close()


if __name__=="__main__":
	import sys
	import scipy
	from scipy import stats
	import gzip
	SNPMethylFileName = sys.argv[1] # Should end with .gz
	SNPMethylCorrsFileName = sys.argv[2]
	readsToMinMinorReadsFileName = sys.argv[3]

	readsToMinMinorReads = makeIntDict(readsToMinMinorReadsFileName)
	correlateSNPsMethylationPlusPlus(SNPMethylFileName, SNPMethylCorrsFileName, readsToMinMinorReads)
