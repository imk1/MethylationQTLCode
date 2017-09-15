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

def convertCpGsToLocations(CpGToLocationDict, CpGsInfoFileName, outputFileName):
	# Replace CpGs with their location in a file that maps CpGs to information (replacement is recorded in a new file)
	CpGsInfoFile = open(CpGsInfoFileName)
	outputFile = open(outputFileName, 'w+')
	for line in CpGsInfoFile:
		# Iterate through the file with the CpG information and re-write each line with the position instead of the CpG
		lineElements = line.strip().split("\t")
		try:
			location = CpGToLocationDict[lineElements[0]]
		except:
			continue
		CpGLength = len(lineElements[0])
		outputFile.write(location[0] + "\t" + str(location[1]) + line[CpGLength:len(line)])
	CpGsInfoFile.close()
	outputFile.close()

if __name__=="__main__":
	import sys
	CpGLocationFileName = sys.argv[1]
	CpGsInfoFileName = sys.argv[2]
	outputFileName = sys.argv[3]
	CpGToLocationDict = makeCpGLocationDict(CpGLocationFileName)
	convertCpGsToLocations(CpGToLocationDict, CpGsInfoFileName, outputFileName)