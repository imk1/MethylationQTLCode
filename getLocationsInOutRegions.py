def getRegion(regionLine):
	if regionLine == "":
		# At the end of the region file, so stop
		return [("", 0, 0), True]
	regionLineElements = regionLine.strip().split("\t")
	return [(regionLineElements[0], int(regionLineElements[1]), int(regionLineElements[2]), regionLineElements[3]), False]

def getSNPOrMethylInOutRegions(locationFileName, regionFileName, outputInFileName, outputOutFileName):
	# Get SNP, C pairs where at least 1 of the SNP or the C is in the region or neither are in the region
	# ASSUMES THAT locationFile IS SORTED BY CHROMOSOME, POSITION
	# ASSUMES THAT regionFile IS SORTED BY CHROMOSOME, START, END
	locationFile = open(locationFileName)
	regionFile = open(regionFileName)
	outputInFile = open(outputInFileName, 'w+')
	outputOutFile = open(outputOutFileName, 'w+')
	[region, atEnd] = getRegion(regionFile.readline())
	for line in locationFile:
		# Iterate through the locations and record them in their appropriate output files
		lineElements = line.strip().split("\t")
		location = (lineElements[0], int(lineElements[1]))
		if atEnd == True:
			# At the end of the region file, so record the location to the output file for locations not in any regions
			outputOutFile.write(line)
		while (atEnd == False) and (region[0] < location[0]):
			# Iterate through the regions until a region on the proper chromosome has been reached
			[region, atEnd] = getRegion(regionFile.readline())
		while (atEnd == False) and ((region[0] == location[0]) and (region[2] < location[1])):
			# Iterate through the regions until a region that does to come before the location has been reached
			[region, atEnd] = getRegion(regionFile.readline())
		if (region[0] == location[0]) and ((region[1] <= location[1]) and (region[2] > location[1])):
			# The location is in a region, so record the location to the output file for locations that are in a region
			outputInFile.write(location[0] + "\t" + str(location[1]) + "\t" + region[3] + "\n")
		else:
			outputOutFile.write(line)
	locationFile.close()
	regionFile.close()
	outputInFile.close()
	outputOutFile.close()

if __name__=="__main__":
   import sys
   locationFileName = sys.argv[1] 
   regionFileName = sys.argv[2]
   outputInFileName = sys.argv[3]
   outputOutFileName = sys.argv[4]
   getSNPOrMethylInOutRegions(locationFileName, regionFileName, outputInFileName, outputOutFileName)