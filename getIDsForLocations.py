def getLocationsList(locationsFileName):
	# Gets a list of locations, where each location is a chromosome and a base
	locationsFile = open(locationsFileName)
	locationsList = []
	IDsList = []
	for line in locationsFile:
		# Iterate through the locations and add each location to the list of locations
		lineElements = line.split("\t")
		location = (lineElements[0], int(lineElements[1].strip()))
		locationsList.append(location)
		IDsList.append("")
	locationsFile.close()
	return [locationsList, IDsList]

def getIDsForLocations(IDsToLocationsFileName, locationsFileName):
	# Get the IDs for the locations of interest and output them IN THE ORDER OF THE LOCATIONS
	[locationsList, IDsList] = getLocationsList(locationsFileName)
	IDsToLocationsFile = open(IDsToLocationsFileName)
	for line in IDsToLocationsFile:
		# Iterate through the locations and determine which are in the list of locations
		lineElements = line.split("\t")
		location = (lineElements[1], int(lineElements[2].strip()))
		if location in locationsList:
			# The location is a location of interest, so record the ID
			locationIndex = locationsList.index(location)
			IDsList[locationIndex] = lineElements[0]
	IDsToLocationsFile.close()
	return IDsList

def writeStrings(StringsList, outputFileName):
	# Write Strings to an output file
	outputFile = open(outputFileName, 'w+')
	for s in StringsList:
		# Iterate through the Strings and write each to the output file
		outputFile.write(s + "\n")
	outputFile.close()

if __name__=="__main__":
	import sys
	IDsToLocationsFileName = sys.argv[1]
	locationsFileName = sys.argv[2]
	outputFileName = sys.argv[3]
	IDsList = getIDsForLocations(IDsToLocationsFileName, locationsFileName)
	writeStrings(IDsList, outputFileName)
