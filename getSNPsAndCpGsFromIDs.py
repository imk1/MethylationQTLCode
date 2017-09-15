def makeIDsToLocationsDict(IDsToLocationsFileName):
	# Make a dictionary that maps IDs to locations from a file with the information
	IDsToLocationsDict = {}
	IDsToLocationsFile = open(IDsToLocationsFileName)
	for line in IDsToLocationsFile:
		# Iterate through the lines of the file that maps IDs to locations and put each mapping into the dictionary
		lineElements = line.strip().split("\t")
		IDsToLocationsDict[lineElements[0]] = (lineElements[1], int(lineElements[2]))
	IDsToLocationsFile.close()
	return IDsToLocationsDict

def getSNPsAndCpGsFromIDs(SNPCpGIDFileName, rsIDsToLocationsDict, CpGIDsToLocationsDict, outputFileName):
	# Get a list of variant and CpG locations from a list of rsID, CpG ID pairs
	SNPCpGIDFile = open(SNPCpGIDFileName)
	outputFile = open(outputFileName, 'w+')
	for line in SNPCpGIDFile:
		# Iterate through the SNP, CpG ID pairs and write each corresponding location pair to the output file
		lineElements = line.strip().split("\t")
		if (lineElements[0] not in rsIDsToLocationsDict.keys()) or (lineElements[1] not in CpGIDsToLocationsDict.keys()):
			# The SNP or CpG ID's location is not known, so skip the current mQTL
			continue
		SNPLocation = rsIDsToLocationsDict[lineElements[0]]
		CpGLocation = CpGIDsToLocationsDict[lineElements[1]]
		outputFile.write(SNPLocation[0] + "\t" + str(SNPLocation[1]) + "\t" + CpGLocation[0] + "\t" + str(CpGLocation[1]) + "\n")
	SNPCpGIDFile.close()
	outputFile.close()

if __name__=="__main__":
	import sys
	SNPCpGIDFileName = sys.argv[1]
	rsIDsToLocationsDictFileName = sys.argv[2]
	CpGIDsToLocationsDictFileName = sys.argv[3]
	outputFileName = sys.argv[4]
	rsIDsToLocationsDict = makeIDsToLocationsDict(rsIDsToLocationsDictFileName)
	CpGIDsToLocationsDict = makeIDsToLocationsDict(CpGIDsToLocationsDictFileName)
	getSNPsAndCpGsFromIDs(SNPCpGIDFileName, rsIDsToLocationsDict, CpGIDsToLocationsDict, outputFileName)
	