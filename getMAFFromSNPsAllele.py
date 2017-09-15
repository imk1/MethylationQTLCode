def getMAFFromSNPsAllele(SNPsAlleleFileName, outputFileName):
	# Gets the MAF for each SNP from a file with SNP locations and alleles
	# SNPsAlleleFile has the following columns:
	# 1.  SNP chromosome
	# 2.  SNP position
	# 3.  Allele on read
	# SNPsMethylAlleleLastFile will have repeated SNP, C pairs, where each pair is listed for each read it is on
	# ASSUMES THAT SNPsMethylAlleleLastFile IS SORTED BY SNP CHROMOSOME, SNP POSITION
	SNPsAlleleFileName = gzip.open(SNPsAlleleFileName)
	outputFile = open(outputFileName, 'w+')
	lastPosition = ("", 0)
	alleles = []
	
	for line in SNPsAlleleFileName:
		# Iterate through the SNPs on the reads and find the MAF for each SNP
		lineElements = line.strip().split("\t")
		currentPosition = (lineElements[0], int(lineElements[1]))
		if currentPosition != lastPosition:
			# At a new SNP, so record the information from the last SNP
			if len(alleles) > 0:
				# Not at the beginning of the file
				numAltAllele = sum(alleles)
				numRefAllele = len(alleles) - numAltAllele
				MAF = 0
				if numRefAllele > numAltAllele:
					# The alternate allele is the minor allele
					MAF = float(numAltAllele)/float(len(alleles))
				else:
					MAF = float(numRefAllele)/float(len(alleles))
				outputFile.write(lastPosition[0] + "\t" + str(lastPosition[1]) + "\t" + str(MAF) + "\n")
			lastPosition = currentPosition
			alleles = []
		alleles.append(float(lineElements[2]))
			
	numAltAllele = sum(alleles)
	numRefAllele = len(alleles) - numAltAllele
	MAF = 0
	if numRefAllele > numAltAllele:
		# The alternate allele is the minor allele
		MAF = float(numAltAllele)/float(len(alleles))
	else:
		MAF = float(numRefAllele)/float(len(alleles))
	outputFile.write(lastPosition[0] + "\t" + str(lastPosition[1]) + "\t" + str(MAF) + "\n")
	SNPsAlleleFileName.close()
	outputFile.close()
	

if __name__=="__main__":
	import sys
	import math
	import gzip
	SNPsAlleleFileName = sys.argv[1]
	outputFileName = sys.argv[2]
	
	getMAFFromSNPsAllele(SNPsAlleleFileName, outputFileName)
