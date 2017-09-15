def getNextRegion(regionsFile):
	# Gets the next region
		regionLine = regionsFile.readline()
		if regionLine == "":
			# At the end of the region, so stop
			return [("", 0, 0), True]
		
		regionLineElements = regionLine.strip().split("\t")
		region = (regionLineElements[0], int(regionLineElements[1]), int(regionLineElements[2]))
		return [region, False]


def getRegionsWithSNPsIndexes(regionsFileName, SNPsFileName, indexStart, indexEnd, outputFileName):
	# Make a list of regions that overlap SNPs/indels
	# ASSUMES THAT REGIONS AND SNPS ARE EITHER BOTH 1-INDEXED (for sam) OR BOTH 0-INDEXED
	# ASSUMES THAT REGIONS ARE SORTED BY CHROMOSOME, START, END AND THAT SNPS ARE SORTED BY CHROMOSOME, LOCATION
	# SKIPS SNPS THAT HAVE "MERGED_DEL" INSTEAD OF AN rsID
	regionsFile = open(regionsFileName)
	SNPsFile = open(SNPsFileName)
	outputFile = open(outputFileName, 'w+')
	[region, atEnd] = getNextRegion(regionsFile)
	if atEnd == True:
		# At the end of the regions, so stop
		return
	atEnd = False
	
	for line in SNPsFile:
		# Iterate through the positions and find those that are in a region
		lineElements = line.strip().split("\t")
		if "MERGED_DEL" in lineElements[2]:
			# Not a SNP or an indel, so skip it
			continue
		SNPStart = int(lineElements[1])
		SNPEnd = SNPStart + len(lineElements[3]) - 1 # Reference allele is listed first
		while region[0] < lineElements[0]:
			# The region is on an earlier chromosome, so go to the next region
			[region, atEnd] = getNextRegion(regionsFile)
			if atEnd == True:
				# At the end of the regions, so stop
				break
		if atEnd == True:
				# At the end of the regions, so stop
				break
		
		while (region[1] + indexEnd < SNPStart) and (region[0] == lineElements[0]):
			# The region is at an earlier location, so go to the next region
			[region, atEnd] = getNextRegion(regionsFile)
			if atEnd == True:
				# At the end of the regions, so stop
				break
		if atEnd == True:
				# At the end of the regions, so stop
				break
		
		while (region[0] == lineElements[0]) and ((region[1] + indexStart <= SNPEnd) and (region[1] + indexEnd >= SNPStart)):
			# The position is in the current region
			outputFile.write(region[0] + "\t" + str(region[1]) + "\t" + str(region[2]) + "\n")
			[region, atEnd] = getNextRegion(regionsFile)
			if atEnd == True:
				# At the end of the regions, so stop
				break
		if atEnd == True:
				# At the end of the regions, so stop
				break
	
	regionsFile.close()
	SNPsFile.close()
	outputFile.close()

	
if __name__=="__main__":
	import sys
	regionsFileName = sys.argv[1]
	SNPsFileName = sys.argv[2]
	indexStart = int(sys.argv[3])
	indexEnd = int(sys.argv[4])
	outputFileName = sys.argv[5]

	getRegionsWithSNPsIndexes(regionsFileName, SNPsFileName, indexStart, indexEnd, outputFileName)