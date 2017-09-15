def processGenotypeLine (genotypeLine):
	# Process a line from an IMPUTE genotype file
	genotypeLineElements = genotypeLine.split(" ")
	SNP = genotypeLineElements[1]
	location = int(genotypeLineElements[2])
	alleleOne = genotypeLineElements[3]
	alleleTwo = genotypeLineElements[4]
	genotypeList = []
	for gle in genotypeLineElements[5:len(genotypeLineElements)]:
		# Iterate through the genotypes and add each to the array
		genotypeList.append(float(gle))
	genotypeArray = np.array(genotypeList)
	SNPInfo = [SNP, alleleOne, alleleTwo, genotypeArray]
	return [location, SNPInfo]

def getPerfectLDSNPs (genotypeFileName, outputFileName, distanceCutoff):
	# Find close SNPs that are in perfect LD
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
	previousSNPDict = {}
	genotypeFile = open(genotypeFileName)
	outputFile = open(outputFileName, 'w+')
	for line in genotypeFile:
		# Iterate through the SNPs and find other SNPs that are in perfect LD with that SNP
		[location, SNPInfo] = processGenotypeLine(line.strip())
		for otherSNPLocation in previousSNPDict.keys():
			# Iterate through the previous SNPs and compute the genotype correlation for those that are close to the current SNP
			if abs(location - otherSNPLocation) > distanceCutoff:
				# The previous SNP is too far away, so remove it
				previousSNPDict.pop(otherSNPLocation)
				continue
			otherSNPInfo = previousSNPDict[otherSNPLocation]
			[corr, pVal] = scipy.stats.pearsonr(SNPInfo[3], otherSNPInfo[3])
			if corr == 1:
				# The SNPs are in perfect LD
				outputFile.write(otherSNPInfo[0] + "\t" + str(otherSNPLocation) + "\t" + otherSNPInfo[1] + "\t" + otherSNPInfo[2] + "\t" + SNPInfo[0] + "\t" + str(location) + "\t" + SNPInfo[1] + "\t" + SNPInfo[2] + "\t" + str(corr) + "\n")
			elif corr == -1:
				# The SNPs are in perfect LD with flipped alleles
				outputFile.write(otherSNPInfo[0] + "\t" + str(otherSNPLocation) + "\t" + otherSNPInfo[1] + "\t" + otherSNPInfo[2] + "\t" + SNPInfo[0] + "\t" + str(location) + "\t" + SNPInfo[2] + "\t" + SNPInfo[1] + "\t" + str(corr) + "\n")
		previousSNPDict[location] = SNPInfo
	genotypeFile.close()
	outputFile.close()

if __name__=="__main__":
	import sys
	import numpy as np
	import scipy.stats
	genotypeFileName = sys.argv[1]
	outputFileName = sys.argv[2]
	distanceCutoff = int(sys.argv[3])
	getPerfectLDSNPs (genotypeFileName, outputFileName, distanceCutoff)