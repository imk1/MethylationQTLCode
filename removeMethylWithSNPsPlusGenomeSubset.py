def processLineMethylShortGenomeSubset(line, isTop, CGDist):
	# Get the information for a line from the methylation file
	lineElements = line.split("\t")
	
	# CHROMOSOME COLUMN HAS REGION
	chromElements = lineElements[2].split(":")
	chrom = chromElements[0]
	regionElements = chromElements[1].split("-")
	position = int(lineElements[3]) + int(regionElements[0]) - 1
	
	if isTop == False:
		# On the bottom strand, so the CpG/CHG starts CGDist positions earlier
		position = position - CGDist
	return [chrom, position]
	

def getNextRegionPlus(regionWithSNPsFile):
	# Get the next region
	regionWithSNPsLine = regionWithSNPsFile.readline()
	atEnd = False
	if regionWithSNPsLine == "":
		# At the end of the region file
		atEnd = True
		print atEnd
		return [("", 0), True]
	regionWithSNPsLineElements = regionWithSNPsLine.split("\t")
	regionWithSNPs = (regionWithSNPsLineElements[0], int(regionWithSNPsLineElements[1]), int(regionWithSNPsLineElements[2]))
	return [regionWithSNPs, False]	


def removeMethylWithSNPsPlusGenomeSubset(bismarkMethylationFileName, regionsWithSNPsFileName, CGDist, outputFileName):
	# Remove the CpGs/CHGs/CHHs that contain SNPs from the methylation file from Bismark
	# ASSUMES THAT regionsWithSNPsFile AND bismarkMethylationFile ARE SORTED BY CHROMOSOME, POSITION
	# Removes all CpGs, CHGs, and CHHs that contain a SNP anywhere in the CpG/CHG/CHH, even if the SNP is not at the C that is being considered
	isTop = True
	bismarkMethylationFileNameElements = bismarkMethylationFileName.split("/") # Only considering last part in file name
	if bismarkMethylationFileNameElements[-1][4:6] == "OB":
		# On the bottom strand
		isTop = False
	bismarkMethylationFile = gzip.open(bismarkMethylationFileName, 'rb')
	regionWithSNPsFile = open(regionsWithSNPsFileName, 'rb')
	outputFile = gzip.open(outputFileName, 'wb')
	[regionWithSNPs, atEnd] = getNextRegionPlus(regionWithSNPsFile)
	
	for line in bismarkMethylationFile:
		# Iterate through the lines of the methylation file and remove those whose coordinates are the same as C*Gs with SNPs
		if atEnd == True:
			# All regions with SNPs have been read, so this region does not have a SNP
			outputFile.write(line)
			continue
		region = processLineMethylShortGenomeSubset(line, isTop, CGDist)
		while regionWithSNPs[0] < region[0]:
			# Iterate through the regions with regions with SNPs until one on the correct chromosome has been reached
			[regionWithSNPs, atEnd] = getNextRegionPlus(regionWithSNPsFile)
			if atEnd == True:
				# At the end, so stop
				break
		if atEnd == True:
			# All regions with SNPs have been read, so this region does not have a SNP
			outputFile.write(line)
			continue
		while (regionWithSNPs[0] == region[0]) and (regionWithSNPs[2] < region[1]): # Using regionWithSNPs[2] will not skip a SNP that follows a C
			# Iterate through the regions with regions with SNPs until one in the correct location has been reached
			[regionWithSNPs, atEnd] = getNextRegionPlus(regionWithSNPsFile)
			if atEnd == True:
				# At the end, so stop
				break
		if atEnd == True:
			# All regions with SNPs have been read, so this region does not have a SNP
			outputFile.write(line)
			continue
		if (regionWithSNPs[0] != region[0]) or (region[1] not in range(regionWithSNPs[1], regionWithSNPs[2] + 1)):
			# The current region is not in a region with a SNP (removes all lines with SNPs in [regionWithSNPs[1], regionWithSNPs[2]])
			outputFile.write(line)

	bismarkMethylationFile.close()
	regionWithSNPsFile.close()
	outputFile.close()


if __name__=="__main__":
	import sys
	import gzip
	bismarkMethylationFileName = sys.argv[1] # Should end with .gz (will need to re-sort by read after running this)
	regionsWithSNPsFileName = sys.argv[2]
	CGDist = int(sys.argv[3])
	outputFileName = sys.argv[4] # Should end with .gz

	removeMethylWithSNPsPlusGenomeSubset(bismarkMethylationFileName, regionsWithSNPsFileName, CGDist, outputFileName)
