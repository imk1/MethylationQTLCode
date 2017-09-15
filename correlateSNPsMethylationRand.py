def outputRandCorr(SNP, methyl, SNPVec, methylVec, SNPMethylCorrsFile):
	# Compute and output the correlation if the reads and MAF cutoffs are satisfied
	corr = scipy.stats.spearmanr(SNPVec, methylVec)[0] # REQUIRES SCIPY 12+ (scipy 8 maybe o.k.)
	SNPMethylCorrsFile.write(SNP[0] + "\t" + str(SNP[1]) + "\t" + methyl[0] + "\t" + str(methyl[1]) + "\t" + str(corr) + "\n")


def correlateSNPsMethylationRand(SNPMethylCorrsFileNamePrefix, SNPVecFileName, methylVecFileName, iterNumber):
	# Compute the correlation between genotype and methylation with shuffled methylation states
	# ASSUMES THAT LINES IN SNPVecFile AND methylVecFile CORRESPOND TO EACH OTHER
	# SNPMethylCorrsFile will have the following information:
	# 1.  SNP chromosome
	# 2.  SNP position in chromosome
	# 3.  Methylation chromosome
	# 4.  Methylation position in chromosome
	# 5.  Correlation between genotype and methylation
	# ASSUMES THAT SNP, methylation pairs that do not have at least minReadsCutoff reads have not been included
	# ASSUMES THAT SNPs that do not have at least MAFCutoff frequency of minor alleles have not been included
	# ASSUMES THAT C's that are not methylated/unmethylated in at least methylCutoff of reads have not been included
	SNPMethylCorrsFile = gzip.open(SNPMethylCorrsFileNamePrefix + str(iterNumber) + ".gz", 'wb')
	SNPVecFile = gzip.open(SNPVecFileName, 'rb')
	methylVecFile = gzip.open(methylVecFileName, 'rb')
	random.seed()

	for line in SNPVecFile:
		# Iterate through the SNP, methylation pairs and find the correlation for each SNP and shuffled methylation
		SNPLineElements = line.strip().split("\t")
		methylLineElements = methylVecFile.readline().strip().split("\t")
		SNP = (SNPLineElements[0], int(SNPLineElements[1]))
		methyl = (methylLineElements[0], int(methylLineElements[1]))
		SNPVec = []
		methylVec = []
		for i in range(2, len(SNPLineElements)):
			# Iterate through the SNPs and methylation states and put the numbers into vectors
			SNPVec.append(int(SNPLineElements[i]))
			methylVec.append(int(methylLineElements[i]))
		random.shuffle(methylVec)
		outputRandCorr(SNP, methyl, SNPVec, methylVec, SNPMethylCorrsFile)

	SNPMethylCorrsFile.close()
	SNPVecFile.close()
	methylVecFile.close()


if __name__=="__main__":
	import sys
	import scipy
	from scipy import stats
	import gzip
	import random
	SNPMethylCorrsFileNamePrefix = sys.argv[1]
	SNPVecFileName = sys.argv[2] # Should end with .gz
	methylVecFileName = sys.argv[3] # Should end with .gz
	iterNumber = int(sys.argv[4])

	correlateSNPsMethylationRand(SNPMethylCorrsFileNamePrefix, SNPVecFileName, methylVecFileName, iterNumber)
