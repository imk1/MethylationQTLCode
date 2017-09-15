def getSNPNumReads(SNPFileName, numReadsFileName):
	# Compute the number of reads for each SNP
	# ASSUMES THAT SNPMethylPlusFile IS SORTED BY SNP CHROM., SNP POSITION
	SNPFile = gzip.open(SNPFileName)
	# Columns of SNPFile:
	# 1.  Read Name
	# 2.  + or  - indicating allele of SNP
	# 3.  SNP chromosome
	# 4.  SNP position in chromosome
	# 5.  SNP bases
	numReadsFile = open(numReadsFileName, 'w+')
	# numReadsFile will have the following information for each C, SNP pair that meets the cutoffs:
	# 1.  SNP chromosome
	# 2.  SNP position in chromosome
	# 3.  Number of reads
	lastSNP = ("", 0)
	numReads = 0

	for line in SNPFile:
		# Iterate through the lines of the SNP methylation file and compute the number of reads for each SNP, C pair
		lineElements = line.strip().split("\t")
		currentSNP = (lineElements[2], int(lineElements[3]))
		if (currentSNP != lastSNP):
			# At a new SNP, so record the number of reads for the previous one
			if lastSNP[0] != "":
				# Not at the beginning of the file
				numReadsFile.write(lastSNP[0] + "\t" + str(lastSNP[1]) + "\t" +  str(numReads) + "\n")
			lastSNP = currentSNP
			numReads = 0
		numReads = numReads + 1

	numReadsFile.write(lastSNP[0] + "\t" + str(lastSNP[1]) + "\t" +  str(numReads) + "\n")
	SNPFile.close()
	numReadsFile.close()


if __name__=="__main__":
	import sys
	import gzip
	SNPFileName = sys.argv[1] # Should end with .gz
	numReadsFileName = sys.argv[2]

	getSNPNumReads(SNPFileName, numReadsFileName)
