def processGenotypeLineVcf (genotypeLine):
	# Process a line from a vcf genotype file
	genotypeLineElements = genotypeLine.split()
	chrom = "chr" + str(genotypeLineElements[0])
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
	SNPInfo = [chrom, alleleOne, alleleTwo, genotypeList]
	return [location, SNPInfo]

def getLDRelatedSNPInfoSimplePlusrSquared (genotypeFileName, outputFileName, distanceCutoff, rSquaredCutoff):
	# Find close SNPs, and compute their LD and related probabilities
	# ASSUMES THAT ALL SNPS ARE ON THE SAME CHROMOSOME
	# Does NOT exclude C/T, T/C, G/A, and A/G SNPs
	# ASSUMES THAT SNPS ARE SORTED BASED ON LOCATION
	# The output file will have the following information:
	# 1.  Chromosome of SNPs
	# 2.  Location of SNP 1
	# 3.  Location of SNP 2
	# 4.  Corr.^2 of SNPs
	previousSNPDict = {}
	genotypeFile = gzip.open(genotypeFileName)
	outputFile = open(outputFileName, 'w+')
	for line in genotypeFile:
		# Iterate through the SNPs and find other SNPs that are in perfect LD with that SNP
		if line[0] == "#": #Y
			# In a header line, so skip it
			continue
		[location, SNPInfo] = processGenotypeLineVcf(line.strip()) # SNPInfo has information for the 2nd SNP
		for otherSNPLocation in previousSNPDict.keys():
			# Iterate through the previous SNPs and compute the genotype correlation for those that are close to the current SNP
			if abs(location - otherSNPLocation) > distanceCutoff: #Y
				# The previous SNP is too far away, so remove it
				previousSNPDict.pop(otherSNPLocation)
				continue
			otherSNPInfo = previousSNPDict[otherSNPLocation] # otherSNPInfo has information for the first SNP
			[corr, pVal] = scipy.stats.pearsonr(np.array(SNPInfo[3]), np.array(otherSNPInfo[3]))
			if math.isnan(corr):
				# The current correlation is nan, so skip this SNP pair
				continue
			rSquared = math.pow(corr, 2)
			if rSquared < rSquaredCutoff:
				# The correlation^2 is too small, so do not record it
				continue
			outputFile.write(otherSNPInfo[0] + "\t" + str(otherSNPLocation) + "\t" + str(location) + "\t" +  str(rSquared) + "\n")
		previousSNPDict[location] = SNPInfo
	genotypeFile.close()
	outputFile.close()

if __name__=="__main__":
	import sys
	import gzip
	import math
	import numpy as np
	import scipy.stats
	# NOT DEBUGGED!
	genotypeFileName = sys.argv[1]
	outputFileName = sys.argv[2]
	distanceCutoff = int(sys.argv[3])
	rSquaredCutoff = float(sys.argv[4])
	getLDRelatedSNPInfoSimplePlusrSquared(genotypeFileName, outputFileName, distanceCutoff, rSquaredCutoff)