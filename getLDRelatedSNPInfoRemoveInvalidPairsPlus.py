def processGenotypeLineVcf (genotypeLine):
	# Process a line from a vcf genotype file
	genotypeLineElements = genotypeLine.split()
	SNP = genotypeLineElements[2]
	location = int(genotypeLineElements[1])
	alleleOne = genotypeLineElements[3]
	alleleTwo = genotypeLineElements[4]
	genotypeList = []
	for gle in genotypeLineElements[9:len(genotypeLineElements)]:
		# Iterate through the genotypes and add each to the array
		# ASSUMES THAT ALL SNPS HAVE BEEN PHASED IN THE SAME WAY
		# Treating each chromosome from each individual separately
		gleElements = gle.strip().split("|")
		genotypeList.append(int(gleElements[0]))
		genotypeList.append(int(gleElements[1]))
	SNPInfo = [SNP, alleleOne, alleleTwo, genotypeList]
	return [location, SNPInfo]

def getLDRelatedSNPInfoRemoveInvalidPairsPlus (genotypeFileName, outputFileName, distanceCutoff, rCutoff):
	# Find close SNPs, and compute their LD and related probabilities
	# Do not include SNPs whose |correlation| < rCutoff
	# Excludes C/T, T/C, G/A, and A/G SNPs
	# ASSUMES THAT SNPS ARE SORTED BASED ON LOCATION
	# The output file will have the following information:
	# 1.  rsID of SNP 1
	# 2.  Location of SNP 1
	# 3.  Allele 1 of SNP 1
	# 4.  Allele 2 of SNP 1
	# 5.  rsID of SNP 2
	# 6.  Location of SNP 2
	# 7.  Allele of SNP 2 that is associated with allele 1 of SNP 1
	# 8.  Allele of SNP 2 that is associated with allele 2 of SNP 1
	# 9.  Corr. of SNPs (1 if reference allele of SNP 1 matches with reference allele with SNP 2; -1 if reference allele of SNP 1 matches with alternate allele of SNP 2)
	# 10.  Probability first SNP is alternate allele given second SNP is alternate allele
	# 11.  Probability first SNP is alternate allele given second SNP is reference allele
	previousSNPDict = {}
	genotypeFile = gzip.open(genotypeFileName)
	outputFile = open(outputFileName, 'w+')
	for line in genotypeFile:
		# Iterate through the SNPs and find other SNPs that are in perfect LD with that SNP
		if line[0] == "#":
			# In a header line, so skip it
			continue
		[location, SNPInfo] = processGenotypeLineVcf(line.strip())
		if (((SNPInfo[1] == "C") and (SNPInfo[2] == "T")) or ((SNPInfo[1] == "T") and (SNPInfo[2] == "C"))) or (((SNPInfo[1] == "G") and (SNPInfo[2] == "A")) or ((SNPInfo[1] == "A") and (SNPInfo[2] == "G"))):
			# The SNP is a C/T, T/C, G/A, or A/G SNP, so skip it
			continue
		for otherSNPLocation in previousSNPDict.keys():
			# Iterate through the previous SNPs and compute the genotype correlation for those that are close to the current SNP
			if abs(location - otherSNPLocation) > distanceCutoff:
				# The previous SNP is too far away, so remove it
				previousSNPDict.pop(otherSNPLocation)
				continue
			otherSNPInfo = previousSNPDict[otherSNPLocation]
			[corr, pVal] = scipy.stats.pearsonr(np.array(SNPInfo[3]), np.array(otherSNPInfo[3]))
			if math.isnan(corr):
				# The current correlation is nan, so skip this SNP pair
				continue
			if abs(corr) < rCutoff:
				# The |correlation| is too small, so do not record it
				continue
			pOne = float(sum(otherSNPInfo[3]))/float(len(otherSNPInfo[3]))
			qOne = float(sum(SNPInfo[3]))/float(len(SNPInfo[3]))
			xOneOneCount = 0
			xOneZeroCount = 0
			for i in range(len(SNPInfo[3])):
				# Iterate through the individuals and count the number of each combination of alleles
				if otherSNPInfo[3][i] == 1:
					# At allele 1 for the first SNP
					if SNPInfo[3][i] == 1:
						# At allele 1 for the second SNP
						xOneOneCount = xOneOneCount + 1
					else:
						xOneZeroCount = xOneZeroCount + 1
			xOneOne = float(xOneOneCount)/float(len(SNPInfo[3]))
			xOneZero = float(xOneZeroCount)/float(len(SNPInfo[3]))
			probFirstOneGivenSecondOne = 0
			if qOne > 0:
				# There is at least 1 occurrence of the alternate allele for the second SNP
				probFirstOneGivenSecondOne = xOneOne/qOne # Probability first SNP is alternate allele given second SNP is alternate allele
			probFirstOneGivenSecondZero = 0
			if qOne < 1:
				# There is at least 1 read where the second SNP has the reference allele
				probFirstOneGivenSecondZero = xOneZero/(1 - qOne) # Probability first SNP is alternate allele given second SNP is reference allele
			LDString = str(corr) + "\t" + str(probFirstOneGivenSecondOne) + "\t" + str(probFirstOneGivenSecondZero)
			outputFile.write(otherSNPInfo[0] + "\t" + str(otherSNPLocation) + "\t" + otherSNPInfo[1] + "\t" + otherSNPInfo[2] + "\t" + SNPInfo[0] + "\t" + str(location) + "\t" + SNPInfo[1] + "\t" + SNPInfo[2] + "\t" + LDString  + "\n")
		previousSNPDict[location] = SNPInfo
	genotypeFile.close()
	outputFile.close()

if __name__=="__main__":
	import sys
	import gzip
	import math
	import numpy as np
	import scipy.stats
	genotypeFileName = sys.argv[1]
	outputFileName = sys.argv[2]
	distanceCutoff = int(sys.argv[3])
	rCutoff = float(sys.argv[4])
	getLDRelatedSNPInfoRemoveInvalidPairsPlus(genotypeFileName, outputFileName, distanceCutoff, rCutoff)