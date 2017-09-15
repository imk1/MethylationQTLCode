def makeStringList(stringFileName):
	# Make a list of strings from a file
	stringFile = open(stringFileName)
	stringList = []
	for line in stringFile:
		# Iterate through the strings and add each to the list
		stringList.append(line.strip())
	stringFile.close()
	return stringList

def getVcfInfo(vcfLine):
	# Get the position, reference, and alternate allele of the SNP on a line of a VCF file
	if vcfLine == "":
		# At the end of the VCF file
		return [0, "", ""]
	vcfLineElements = vcfLine.strip().split("\t")
	vcfPosition = int(vcfLineElements[1])
	refAllele = vcfLineElements[3]
	altAllele = vcfLineElements[4]
	return [vcfPosition, refAllele, altAllele]

def convertGenotypes(genotypes, refAllele, altAllele):
	# Convert the genotypes to 0, 1 form
	genotypesZeroOne = []
	for indivGenotype in genotypes:
		# Iterate through the genotypes and convert each
		if indivGenotype == refAllele + refAllele:
			# The genotype is homozygous reference
			genotypesZeroOne.append(0.0)
		elif indivGenotype == refAllele + altAllele:
			# The genotype is heterozygous
			genotypesZeroOne.append(0.5)
		elif indivGenotype == altAllele + refAllele:
			# The genotype is heterozygous
			genotypesZeroOne.append(0.5)
		elif indivGenotype == altAllele + altAllele:
			# The genotype is homozygous for the alternate allele
			genotypesZeroOne.append(1.0)
		else:
			print "Problem!"
			print indivGenotype
			print refAllele
			print altAllele
			return []
	return genotypesZeroOne

def outputGenotypes(outputFile, chrom, position, genotypesZeroOne):
	# Output the genotypes to the output file
	outputFile.write(chrom + "\t" + str(position))
	for genotypeIndivZeroOne in genotypesZeroOne:
		# Record all of the genotypes
		outputFile.write("\t" + str(genotypeIndivZeroOne))
	outputFile.write("\n")

def convertFilterGenotypes(genotypesFileName, indivsList, vcfFileName, outputFileName):
	# Convert the genotypes to 0/1 and remove individual that are not in the individuals file, C/T SNPs, and G/A SNPs
	# ASSUMES THAT ALL DATA IS FROM THE SAME CHROMOSOME
	# ASSUMES THAT genotypesFile AND vcfFile ARE SORTED BY POSITION
	genotypesFile = open(genotypesFileName)
	header = genotypesFile.readline()
	headerElements = header.strip().split()
	indivsIndexes = []
	for indiv in indivsList:
		# Iterate through the individuals and get the indexes for each
		indivIndex = headerElements.index(indiv)
		indivsIndexes.append(indivIndex)
	outputFile = open(outputFileName, 'w+')
	vcfFile = gzip.open(vcfFileName)
	vcfLine = vcfFile.readline()
	while vcfLine[0] == "#":
		# Go through the lines of the VCF file until one with a SNP is reached
		vcfLine = vcfFile.readline()
	[vcfPosition, refAllele, altAllele] = getVcfInfo(vcfLine)
	vcfEnd = False
	for line in genotypesFile:
		# Iterate through the SNPs and record the genotypes for each in 0/0.5/1 form
		lineElements = line.strip().split()
		position = int(lineElements[3])
		while vcfPosition < position:
			# Iterate through the VCF file until a SNP in the correct position has been reached
			[vcfPosition, refAllele, altAllele] = getVcfInfo(vcfFile.readline())
			if vcfPosition == 0:
				# At the end of the VCF file, so stop
				vcfEnd = True
				break
		if vcfEnd == True:
			# At the end of the VCF file, so stop
			break
		if vcfPosition > position:
			# Skip the current SNP because it is not in the VCF file
			continue
		if (((refAllele == "C") and (altAllele == "T")) or ((refAllele == "T") and (altAllele == "C"))) or (((refAllele == "G") and (altAllele == "A")) or ((refAllele == "A") and (altAllele == "G"))):
			# At a C/T or G/A SNP, so skip it
			continue
		genotypes = []
		missingData = False
		for indivIndex in indivsIndexes:
			# Iterate through the individuals and get their genotypes
			indivGenotype = lineElements[indivIndex]
			if "N" in indivGenotype:
				# Missing data, so skip this SNP
				missingData = True
				break
			genotypes.append(indivGenotype)
		if missingData == True:
			# There is missing data for the current SNP, so skip it
			continue
		chrom = lineElements[2].lower()
		genotypesZeroOne = convertGenotypes(genotypes, refAllele, altAllele)
		if len(genotypesZeroOne) == 0:
			# There was a problem with the SNP, so skip it
			continue
		outputGenotypes(outputFile, chrom, position, genotypesZeroOne)
	genotypesFile.close()
	vcfFile.close()
	outputFile.close()

if __name__=="__main__":
   import sys
   import gzip
   genotypesFileName = sys.argv[1]
   indivsListFileName = sys.argv[2]
   vcfFileName = sys.argv[3]
   outputFileName = sys.argv[4]
   indivsList = makeStringList(indivsListFileName)
   convertFilterGenotypes(genotypesFileName, indivsList, vcfFileName, outputFileName)
