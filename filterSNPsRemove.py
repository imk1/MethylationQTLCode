def filterSNPsRemove(locationsFileName, locationsToRemoveFileName, overlapDist, overlapDistPre, outputFileName):
	# Records all locations from a list that are in another list
	# ASSUMES THAT BOTH FILES ARE SORTED BY CHROMOSOME AND THEN BY LOCATION AND HAVE NO REPEATS
	locationsFile = open(locationsFileName)
	locationsToRemoveFile = open(locationsToRemoveFileName)
	outputFile = open(outputFileName, 'w+')
	locationsToRemoveLineElements = locationsToRemoveFile.readline().split("\t")
	for line in locationsFile:
		# Iterate through locations and record only those that do not need to be Keepd
		lineElements = line.split("\t")
		while lineElements[0] > locationsToRemoveLineElements[0]:
			# Iterate through locations until a location on the proper chromosome has been reached
			locationsToRemoveLineElements = locationsToRemoveFile.readline().split("\t")
			if locationsToRemoveLineElements[0] == "":
				# At the end of the locations that will be removed, so stop
				break
		if lineElements[0] == locationsToRemoveLineElements[0]:
			# Check that the chromosomes for the current location and the location to be filtered are the same
			while int(lineElements[1].strip()) - overlapDistPre > int(locationsToRemoveLineElements[1].strip()):
				# Iterate through filt. locations until a location with a start >= location start is reached
				locationsToRemoveLineElements = locationsToRemoveFile.readline().split("\t")
				if locationsToRemoveLineElements[0] == "":
					# At the end of the locations that will be removed, so stop
					break
				if lineElements[0] < locationsToRemoveLineElements[0]:
					# On the next chromosome for filtered locations, so stop
					break
		if locationsToRemoveLineElements[0] == "":
			# At the end of the locations that will be remove, so record the current location
			outputFile.write(line)
		if (lineElements[0] == locationsToRemoveLineElements[0]) and (int(locationsToRemoveLineElements[1].strip()) in range(int(lineElements[1].strip()) - overlapDistPre, int(lineElements[1].strip()) + overlapDist + 1)):
			# Do not record the current location
			 continue
		# Record the current location
		outputFile.write(line)
	locationsFile.close()
	locationsToRemoveFile.close()
	outputFile.close()

if __name__=="__main__":
	import sys
	locationsFileName = sys.argv[1]
	locationsToRemoveFileName = sys.argv[2]
	overlapDist = int(sys.argv[3])
	overlapDistPre = int(sys.argv[4])
	outputFileName = sys.argv[5]
	filterSNPsRemove(locationsFileName, locationsToRemoveFileName, overlapDist, overlapDistPre, outputFileName)
