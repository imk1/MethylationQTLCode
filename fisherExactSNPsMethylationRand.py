def outputFisherExactRand(SNP, methyl, SNPVec, methylVec, minReadsCutoff, MAFCutoff, methylCutoff, SNPMethylFisherExactRandFile):
	# Compute and output the hypergeometric p-values if the reads, MAF, and methylation cutoffs are satisfied
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
				SNPMethylFisherExactRandFile.write(SNP[0] + "\t" + str(SNP[1]) + "\t" + methyl[0] + "\t" + str(methyl[1]) + "\t" + str(pVal) + "\n")


def fisherExactSNPsMethylationRand(SNPMethylFileName, SNPMethylFisherExactRandFileName, minReadsCutoff, MAFCutoff, methylCutoff):
	# Use the Fisher's exact test to determine whether the distribution of alleles for shuffled methylation statuses is more skewed than would be expected by chance
	# ASSUMES THAT SNPMethylFile IS SORTED BY METHYLATION CHROM., METHYLATION POSITION, SNP CHROM., SNP POSITION
	# SNPMethylFisherExactRandFile will have the following information:
	# 1.  SNP chromosome
	# 2.  SNP position in chromosome
	# 3.  Methylation chromosome
	# 4.  Methylation position in chromosome
	# 5.  Fisher's exact p-value between genotype and shuffled methylation
	# Reference allele will be recorded as 0; alternate allele will be recorded as 1
	# Methylated will be recorded as 1; unmethylated will be recorded as 0
	# SNP, methylation pairs that do not have at least minReadsCutoff reads will not be included
	# SNPs that do not have at least MAFCutoff frequency of minor alleles will not be included
	# C's that are not methylated/unmethylated in at least methylCutoff fraction of reads will not be included
	SNPMethylFile = gzip.open(SNPMethylFileName, 'rb')
	SNPMethylFisherExactRandFile = open(SNPMethylFisherExactRandFileName, 'wb')
	lastSNP = ("", 0)
	lastMethyl = ("", 0)
	SNPVec = []
	methylVec = []
	random.seed()

	for line in SNPMethylFile:
		# Iterate through the lines of the SNP methylation file and compute the Fisher's exact p-value for each SNP, C pair
		lineElements = line.strip().split("\t")
		currentSNP = (lineElements[1], int(lineElements[2]))
		currentMethyl = (lineElements[4], int(lineElements[5]))
		if (currentSNP != lastSNP) or (currentMethyl != lastMethyl):
			# At a new SNP or methylation location, so find the Fisher's exact p-value for the previous one
			outputFisherExactRand(lastSNP, lastMethyl, SNPVec, methylVec, minReadsCutoff, MAFCutoff, methylCutoff, SNPMethylFisherExactRandFile)
			lastSNP = currentSNP
			lastMethyl = currentMethyl
			SNPVec = []
			methylVec = []
		
		SNPVec.append(int(lineElements[3]))
		methylVec.append(int(lineElements[6]))

	outputFisherExactRand(lastSNP, lastMethyl, SNPVec, methylVec, minReadsCutoff, MAFCutoff, methylCutoff, SNPMethylFisherExactRandFile)
	SNPMethylFile.close()
	SNPMethylFisherExactRandFile.close()


if __name__=="__main__":
	import sys
	import scipy
	from scipy import stats
	import gzip
	import random
	SNPMethylFileName = sys.argv[1] # Should end with .gz
	SNPMethylFisherExactRandFileName = sys.argv[2]
	minReadsCutoff = int(sys.argv[3])
	MAFCutoff = float(sys.argv[4])
	methylCutoff = float(sys.argv[5])

	fisherExactSNPsMethylationRand(SNPMethylFileName, SNPMethylFisherExactRandFileName, minReadsCutoff, MAFCutoff, methylCutoff)
