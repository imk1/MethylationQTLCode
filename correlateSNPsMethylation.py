def outputCorr(SNP, methyl, SNPVec, methylVec, SNPVecFile, methylVecFile, minReadsCutoff, MAFCutoff, methylCutoff, SNPMethylCorrsFile):
	# Compute and output the correlation if the reads and MAF cutoffs are satisfied
	vecLen = len(methylVec)
	if vecLen >= minReadsCutoff:
		# The minimum reads cutoff is satisfied
		numRefAlleles = SNPVec.count(0)
		numAltAlleles = SNPVec.count(1)
		if (float(numRefAlleles)/float(vecLen) > MAFCutoff) and (float(numAltAlleles)/float(vecLen) > MAFCutoff):
			# Both alleles have sufficiently high frequencies
			numMethyl = methylVec.count(1)
			numUnmethyl = methylVec.count(0)
			if  (float(numMethyl)/float(vecLen) > methylCutoff) and (float(numUnmethyl)/float(vecLen) > methylCutoff):
				# C is methylated and unmethylated a sufficient fraction of the time
				corr = scipy.stats.spearmanr(SNPVec, methylVec)[0] # REQUIRES SCIPY 12+ (scipy 8 maybe o.k.)
				SNPMethylCorrsFile.write(SNP[0] + "\t" + str(SNP[1]) + "\t" + methyl[0] + "\t" + str(methyl[1]) + "\t" + str(corr) + "\n")

				SNPVecFile.write(SNP[0] + "\t" + str(SNP[1]))
				methylVecFile.write(methyl[0] + "\t" + str(methyl[1]))
				for i in range(len(methylVec)):
					# Iterate through the genotype and methylation calls and record each
					SNPVecFile.write("\t" + str(SNPVec[i]))
					methylVecFile.write("\t" + str(methylVec[i]))
				SNPVecFile.write("\n")
				methylVecFile.write("\n")


def correlateSNPsMethylation(SNPMethylFileName, methylLetter, SNPMethylCorrsFileName, SNPVecFileName, methylVecFileName, minReadsCutoff, MAFCutoff, methylCutoff):
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
	# SNP, methylation pairs that do not have at least minReadsCutoff reads will not be included
	# SNPs that do not have at least MAFCutoff frequency of minor alleles will not be included
	# C's that are not methylated/unmethylated in at least methylCutoff fraction of reads will not be included
	SNPMethylFile = gzip.open(SNPMethylFileName, 'rb')
	SNPMethylCorrsFile = gzip.open(SNPMethylCorrsFileName, 'wb')
	SNPVecFile = gzip.open(SNPVecFileName, 'wb')
	methylVecFile = gzip.open(methylVecFileName, 'wb')
	lastSNP = ("", 0)
	lastMethyl = ("", 0)
	SNPVec = []
	methylVec = []

	for line in SNPMethylFile:
		# Iterate through the lines of the SNP methylation file and compute the correlation for each SNP, C pair
		lineElements = line.strip().split("\t")
		currentSNP = (lineElements[1], int(lineElements[2]))
		currentMethyl = (lineElements[5], int(lineElements[6]))
		if (currentSNP != lastSNP) or (currentMethyl != lastMethyl):
			# At a new SNP or methylation location, so find the correlation for the previous one
			outputCorr(lastSNP, lastMethyl, SNPVec, methylVec, SNPVecFile, methylVecFile, minReadsCutoff, MAFCutoff, methylCutoff, SNPMethylCorrsFile)
			lastSNP = currentSNP
			lastMethyl = currentMethyl
			SNPVec = []
			methylVec = []

		if lineElements[3] == "+":
			# The SNP is the reference allele, so add a 0 to the vector
			SNPVec.append(0)
		else:
			SNPVec.append(1)
		if lineElements[8] == methylLetter:
			# The base is methylated, so add a 1 to the vector
			methylVec.append(1)
		else:
			methylVec.append(0)

	outputCorr(lastSNP, lastMethyl, SNPVec, methylVec, SNPVecFile, methylVecFile, minReadsCutoff, MAFCutoff, methylCutoff, SNPMethylCorrsFile)
	SNPMethylFile.close()
	SNPMethylCorrsFile.close()
	SNPVecFile.close()
	methylVecFile.close()


if __name__=="__main__":
	import sys
	import scipy
	from scipy import stats
	import gzip
	SNPMethylFileName = sys.argv[1] # Should end with .gz
	methylLetter = sys.argv[2]
	SNPMethylCorrsFileName = sys.argv[3] # Should end with .gz
	SNPVecFileName = sys.argv[4] # Should end with .gz
	methylVecFileName = sys.argv[5] # Should end with .gz
	minReadsCutoff = int(sys.argv[6])
	MAFCutoff = float(sys.argv[7])
	methylCutoff = float(sys.argv[8])

	correlateSNPsMethylation(SNPMethylFileName, methylLetter, SNPMethylCorrsFileName, SNPVecFileName, methylVecFileName, minReadsCutoff, MAFCutoff, methylCutoff)
