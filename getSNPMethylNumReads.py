def getSNPMethylNumReads(SNPMethylPlusFileName, numReadsFileName):
	# Compute the effect size for each SNP, C
	# ASSUMES THAT SNPMethylPlusFile IS SORTED BY METHYLATION CHROM., METHYLATION POSITION, SNP CHROM., SNP POSITION
	SNPMethylPlusFile = gzip.open(SNPMethylPlusFileName)
	# Columns of SNPMethylPlusFile:
	# 1.  Read Name
	# 2.  SNP chromosome
	# 3.  SNP position in chromosome
	# 4.  1 or 0 indicating allele of SNP
	# 5.  Methylation chromosome
	# 6.  Methylation position in chromosome
	# 7.  1 or 0 indicating whether C is methylated (1 means methylated)
	# 8.  Number indicating which file (replicate and strand) read came from
	numReadsFile = open(numReadsFileName, 'w+')
	# numReadsFile will have the following information for each C, SNP pair that meets the cutoffs:
	# 1.  SNP chromosome
	# 2.  SNP position in chromosome
	# 3.  Methylation chromosome
	# 4.  Methylation position in chromosome
	# 5.  Number of reads
	lastSNP = ("", 0)
	lastMethyl = ("", 0)
	numReads = 0

	for line in SNPMethylPlusFile:
		# Iterate through the lines of the SNP methylation file and compute the number of reads for each SNP, C pair
		lineElements = line.strip().split("\t")
		currentSNP = (lineElements[1], int(lineElements[2]))
		currentMethyl = (lineElements[4], int(lineElements[5]))
		if ((currentSNP != lastSNP) or (currentMethyl != lastMethyl)):
			# At a new SNP or methylation location, so find the number of reads for the previous one
			if lastSNP[0] != "":
				# Not at the beginning of the file
				SNPMethylDist = lastSNP[1] - lastMethyl[1]
				numReadsFile.write(lastSNP[0] + "\t" + str(lastSNP[1]) + "\t" + lastMethyl[0] + "\t" + str(lastMethyl[1]) + "\t" + str(numReads) + "\t" + str(SNPMethylDist) + "\n")
			lastSNP = currentSNP
			lastMethyl = currentMethyl
			numReads = 0
		numReads = numReads + 1

	SNPMethylDist = lastSNP[1] - lastMethyl[1]
	numReadsFile.write(lastSNP[0] + "\t" + str(lastSNP[1]) + "\t" + lastMethyl[0] + "\t" + str(lastMethyl[1]) + "\t" + str(numReads) + "\t" + str(SNPMethylDist) + "\n")
	SNPMethylPlusFile.close()
	numReadsFile.close()


if __name__=="__main__":
	import sys
	import gzip
	SNPMethylPlusFileName = sys.argv[1] # Should end with .gz
	numReadsFileName = sys.argv[2]

	getSNPMethylNumReads(SNPMethylPlusFileName, numReadsFileName)
