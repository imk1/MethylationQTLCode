def getNextRegion(regionsFile):
	# Gets the next region
		regionLine = regionsFile.readline()
		if regionLine == "":
			# At the end of the region, so stop
			return [("", 0, 0), True]
		
		regionLineElements = regionLine.strip().split("\t")
		region = (regionLineElements[0], int(regionLineElements[1]), int(regionLineElements[2]))
		return [region, False]


def getRegionsWithPositions(regionsFileName, positionsFileName, outputFileName):
	# Make a list of regions that overlap positions
	# ASSUMES THAT REGIONS AND POSITIONS ARE EITHER BOTH 1-INDEXED (for sam) OR BOTH 0-INDEXED
	# ASSUMES THAT REGIONS ARE SORTED BY CHROMOSOME, START, END AND THAT POSITIONS ARE SORTED BY CHROMOSOME, LOCATION
	regionsFile = open(regionsFileName)
	positionsFile = open(positionsFileName)
	outputFile = open(outputFileName, 'w+')
	[region, atEnd] = getNextRegion(regionsFile)
	if atEnd == True:
		# At the end of the regions, so stop
		return
	atEnd = False
	
	for line in positionsFile:
		# Iterate through the positions and find those that are in a region
		lineElements = line.strip().split("\t")
		while region[0] < lineElements[0]:
			# The region is on an earlier chromosome, so go to the next region
			[region, atEnd] = getNextRegion(regionsFile)
			if atEnd == True:
				# At the end of the regions, so stop
				break
		if atEnd == True:
				# At the end of the regions, so stop
				break
		
		while (region[2] < int(lineElements[1])) and (region[0] == lineElements[0]):
			# The region is at an earlier location, so go to the next region
			[region, atEnd] = getNextRegion(regionsFile)
			if atEnd == True:
				# At the end of the regions, so stop
				break
		if atEnd == True:
				# At the end of the regions, so stop
				break
		
		while (region[0] == lineElements[0]) and ((region[1] <= int(lineElements[1])) and (region[2] >= int(lineElements[1]))):
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
	positionsFile.close()
	outputFile.close()

	
if __name__=="__main__":
	import sys
	regionsFileName = sys.argv[1]
	positionsFileName = sys.argv[2]
	outputFileName = sys.argv[3]

	getRegionsWithPositions(regionsFileName, positionsFileName, outputFileName)