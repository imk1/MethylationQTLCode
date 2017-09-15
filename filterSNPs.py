def filterSNPs(locationsFileName, locationsToKeepFileName, outputFileName):
	# Records all locations from a list that are in another list
	# ASSUMES THAT BOTH FILES ARE SORTED BY CHROMOSOME AND THEN BY LOCATION AND HAVE NO REPEATS
	locationsFile = open(locationsFileName)
	locationsToKeepFile = open(locationsToKeepFileName)
	outputFile = open(outputFileName, 'w+')
	locationsToKeepLineElements = locationsToKeepFile.readline().split("\t")
	for line in locationsFile:
		# Iterate through locations and record only those that do not need to be Keepd
		lineElements = line.split("\t")
		while lineElements[0] > locationsToKeepLineElements[0]:
			# Iterate through locations until a location on the proper chromosome has been reached
			locationsToKeepLineElements = locationsToKeepFile.readline().split("\t")
			if locationsToKeepLineElements[0] == "":
				# At the end of the locations that will be kept, so stop
				break
		if lineElements[0] == locationsToKeepLineElements[0]:
			# Check that the chromosomes for the current location and the location to be filtered are the same
			while int(lineElements[1].strip()) > int(locationsToKeepLineElements[1].strip()):
				# Iterate through filt. locations until a location with a start >= location start is reached
				locationsToKeepLineElements = locationsToKeepFile.readline().split("\t")
				if locationsToKeepLineElements[0] == "":
					# At the end of the locations that will be kept, so stop
					break
				if lineElements[0] < locationsToKeepLineElements[0]:
					# On the next chromosome for filtered locations, so stop
					break
		if locationsToKeepLineElements[0] == "":
			# At the end of the locations that will be kept, so stop
			break
		if (lineElements[0] == locationsToKeepLineElements[0]) and (int(lineElements[1].strip()) == int(locationsToKeepLineElements[1].strip())):
			# Record the current location
			outputFile.write(line)
	locationsFile.close()
	locationsToKeepFile.close()
	outputFile.close()

if __name__=="__main__":
	import sys
	locationsFileName = sys.argv[1]
	locationsToKeepFileName = sys.argv[2]
	outputFileName = sys.argv[3]
	filterSNPs(locationsFileName, locationsToKeepFileName, outputFileName)
