def outputCorr(SNP, methyl, SNPVec, methylVec, minReadsCutoff, MAFCutoff, methylCutoff, SNPMethylCorrsFile, SNPMethylpValsFile):
	# Compute and output the correlation if the reads and MAF cutoffs are satisfied
	vecLen = len(methylVec)
	if vecLen >= minReadsCutoff:
		# The minimum reads cutoff is satisfied
		numAltAlleles = sum(SNPVec)
		numRefAlleles = vecLen - numAltAlleles
		if (float(numRefAlleles)/float(vecLen) > MAFCutoff) and (float(numAltAlleles)/float(vecLen) > MAFCutoff):
			# Both alleles have sufficiently high frequencies
			numMethyl = sum(methylVec)
			numUnmethyl = vecLen - numMethyl
			
			if  (float(numMethyl)/float(vecLen) > methylCutoff) and (float(numUnmethyl)/float(vecLen) > methylCutoff):
				# C is methylated and unmethylated a sufficient fraction of the time
				try:
					[corr, pVal] = scipy.stats.pearsonr(SNPVec, methylVec) # REQUIRES SCIPY 12+ (scipy 8 maybe o.k.)
					SNPMethylCorrsFile.write(SNP[0] + "\t" + str(SNP[1]) + "\t" + methyl[0] + "\t" + str(methyl[1]) + "\t" + str(corr) + "\n")
					SNPMethylpValsFile.write(SNP[0] + "\t" + str(SNP[1]) + "\t" + methyl[0] + "\t" + str(methyl[1]) + "\t" + str(pVal) + "\n")
				except:
					SNPMethylCorrsFile.write(SNP[0] + "\t" + str(SNP[1]) + "\t" + methyl[0] + "\t" + str(methyl[1]) + "\t" + "NaN" + "\n")
					SNPMethylpValsFile.write(SNP[0] + "\t" + str(SNP[1]) + "\t" + methyl[0] + "\t" + str(methyl[1]) + "\t" + "NaN" + "\n")

	
def correlateSNPsMethylationPlus(SNPMethylFileName, SNPMethylCorrsFileName, minReadsCutoff, MAFCutoff, methylCutoff, SNPMethylpValsFileName):
	# Compute the Pearson correlation between genotype and methylation
	# Allows for SNP and methylation values to be probabilities instead of integers
	# ASSUMES THAT SNPMethylFile IS SORTED BY METHYLATION CHROM., METHYLATION POSITION, SNP CHROM., SNP POSITION
	# SNPMethylCorrsFile will have the following information:
	# 1.  SNP chromosome
	# 2.  SNP position in chromosome
	# 3.  Methylation chromosome
	# 4.  Methylation position in chromosome
	# 5.  Pearson correlation between genotype and methylation
	# SNP, methylation pairs that do not have at least minReadsCutoff reads will not be included
	# SNPs that do not have at least MAFCutoff frequency of minor alleles will not be included
	# C's that are not methylated/unmethylated in at least methylCutoff fraction of reads will not be included
	SNPMethylFile = gzip.open(SNPMethylFileName, 'rb')
	SNPMethylCorrsFile = open(SNPMethylCorrsFileName, 'wb')
	SNPMethylpValsFile = open(SNPMethylpValsFileName, 'w+')
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
			outputCorr(lastSNP, lastMethyl, SNPVec, methylVec, minReadsCutoff, MAFCutoff, methylCutoff, SNPMethylCorrsFile, SNPMethylpValsFile)
			lastSNP = currentSNP
			lastMethyl = currentMethyl
			SNPVec = []
			methylVec = []
		
		SNPVec.append(float(lineElements[3]))
		methylVec.append(float(lineElements[6]))

	outputCorr(lastSNP, lastMethyl, SNPVec, methylVec, minReadsCutoff, MAFCutoff, methylCutoff, SNPMethylCorrsFile, SNPMethylpValsFile)
	SNPMethylFile.close()
	SNPMethylCorrsFile.close()
	SNPMethylpValsFile.close()


if __name__=="__main__":
	import sys
	import scipy
	from scipy import stats
	import gzip
	SNPMethylFileName = sys.argv[1] # Should end with .gz
	SNPMethylCorrsFileName = sys.argv[2]
	minReadsCutoff = int(sys.argv[3])
	MAFCutoff = float(sys.argv[4])
	methylCutoff = float(sys.argv[5])
	SNPMethylpValsFileName = sys.argv[6]

	correlateSNPsMethylationPlus(SNPMethylFileName, SNPMethylCorrsFileName, minReadsCutoff, MAFCutoff, methylCutoff, SNPMethylpValsFileName)
