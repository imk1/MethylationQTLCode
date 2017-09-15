def makeSNPLocationDict(SNPLocationFileName):
	# Make a dictionary that makes rsIDs to SNP Locations
	SNPLocationFile = open(SNPLocationFileName)
	SNPToLocationDict = {}
	for line in SNPLocationFile:
		# Iterate through the lines of the SNP file and enter the location for the SNP in each file
		# EXCLUDE INDELS
		lineElements = line.strip().split("\t")
		if lineElements[2][0:2] != "rs":
			# At an indel, so continue
			continue
		SNPToLocationDict[lineElements[2]] = (lineElements[0], int(lineElements[1]))
	SNPLocationFile.close()
	return SNPToLocationDict

def makeCpGLocationDict(CpGLocationFileName):
	# Make a dictionary that maps Illumina IDs to CpG Locations
	CpGLocationFile = open(CpGLocationFileName)
	CpGToLocationDict = {}
	for line in CpGLocationFile:
		# Iterate through the lines of the CpG file and enter the location for the CpG on each line in the file
		lineElements = line.strip().split(",")
		chrom = "chr" + lineElements[1]
		CpGToLocationDict[lineElements[0]] = (chrom, int(lineElements[2]))
	CpGLocationFile.close()
	return CpGToLocationDict

def getMoenYRImQTLLocations(mQTLFileName, SNPToLocationDict, CpGToLocationDict, distanceCutoff, outputFileName):
	# Find the YRI mQTLs for which the SNP and CpG are within distanceCutoff of each other
	# ASSUMES THAT THERE ARE NO NAS IN THE LAST COLUMN (code does not implicitly make that assumption, but NAs are not checked for)
	mQTLFile = open(mQTLFileName)
	mQTLFile.readline() # REMOVE THE HEADER
	outputFile = open(outputFileName, 'w+')
	for line in mQTLFile:
		# Iterate through the mQTLs and get the locations for each
		lineElements = line.strip().split("\t")
		try:
			SNPLocation = SNPToLocationDict[lineElements[1]]
		except:
			print lineElements[1]
			continue
		CpGLocation = CpGToLocationDict[lineElements[0]]
		if SNPLocation[0] != CpGLocation[0]:
			# The SNPs and CpGs are on different chromosomes, so do not include them
			continue
		if abs(SNPLocation[1] - CpGLocation[1]) > distanceCutoff:
			# The SNP and CpG are not close to each other, so do not include them
			continue
		outputFile.write(SNPLocation[0] + "\t" + str(SNPLocation[1]) + "\t" + CpGLocation[0] + "\t" + str(CpGLocation[1]) + "\t" + lineElements[7] + "\n")
	mQTLFile.close()
	outputFile.close()

if __name__=="__main__":
	import sys
	mQTLFileName = sys.argv[1]
	SNPLocationFileName = sys.argv[2]
	CpGLocationFileName = sys.argv[3]
	distanceCutoff = int(sys.argv[4])
	outputFileName = sys.argv[5]
	SNPToLocationDict = makeSNPLocationDict(SNPLocationFileName)
	CpGToLocationDict = makeCpGLocationDict(CpGLocationFileName)
	getMoenYRImQTLLocations(mQTLFileName, SNPToLocationDict, CpGToLocationDict, distanceCutoff, outputFileName)