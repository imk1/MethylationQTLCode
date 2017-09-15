def processLineMethylShort(line, isTop, CGDist):
	# Get the information for a line from the methylation file
	lineElements = line.split("\t")
	chrom = lineElements[2]
	position = int(lineElements[3])
	
	if isTop == False:
		# On the bottom strand, so the CpG/CHG starts CGDist positions earlier
		position = position - CGDist
	return [chrom, position]
	

def getNextRegion(regionWithSNPsFile):
	# Get the next region
	regionWithSNPsLine = regionWithSNPsFile.readline()
	atEnd = False
	if regionWithSNPsLine == "":
		# At the end of the region file
		atEnd = True
		return [("", 0), True]
	regionWithSNPsLineElements = regionWithSNPsLine.split("\t")
	regionWithSNPs = (regionWithSNPsLineElements[0], int(regionWithSNPsLineElements[1]))
	return [regionWithSNPs, False]	


def removeMethylWithSNPs(bismarkMethylationFileName, regionsWithSNPsFileName, CGDist, outputFileName):
	# Remove the CpGs that contain SNPs from the methylation file from Bismark
	# ASSUMES THAT regionsWithSNPsFile AND bismarkMethylationFile ARE SORTED BY CHROMOSOME, POSITION
	isTop = True
	bismarkMethylationFileNameElements = bismarkMethylationFileName.split("/") # Only considering last part in file name
	if bismarkMethylationFileNameElements[-1][4:6] == "OB":
		# On the bottom strand
		isTop = False
	print isTop
	bismarkMethylationFile = gzip.open(bismarkMethylationFileName, 'rb')
	regionWithSNPsFile = open(regionsWithSNPsFileName)
	outputFile = gzip.open(outputFileName, 'wb')
	[regionWithSNPs, atEnd] = getNextRegion(regionWithSNPsFile)
	
	for line in bismarkMethylationFile:
		# Iterate through the lines of the methylation file and remove those whose coordinates are the same as C*Gs with SNPs
		if atEnd == True:
			# All regions with SNPs have been read, so this region does not have a SNP
			outputFile.write(line)
			continue
		region = processLineMethylShort(line, isTop, CGDist)
		while regionWithSNPs[0] < region[0]:
			# Iterate through the regions with regions with SNPs until one on the correct chromosome has been reached
			[regionWithSNPs, atEnd] = getNextRegion(regionWithSNPsFile)
			if atEnd == True:
				# At the end, so stop
				break
		if atEnd == True:
			# All regions with SNPs have been read, so this region does not have a SNP
			outputFile.write(line)
			continue
		while (regionWithSNPs[0] == region[0]) and (regionWithSNPs[1] < region[1]):
			# Iterate through the regions with regions with SNPs until one in the correct location has been reached
			[regionWithSNPs, atEnd] = getNextRegion(regionWithSNPsFile)
			if atEnd == True:
				# At the end, so stop
				break
		if atEnd == True:
			# All regions with SNPs have been read, so this region does not have a SNP
			outputFile.write(line)
			continue
		if (regionWithSNPs[0] != region[0]) or (regionWithSNPs[1] != region[1]):
			# The current region is not in a region with a SNP
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

	removeMethylWithSNPs(bismarkMethylationFileName, regionsWithSNPsFileName, CGDist, outputFileName)
