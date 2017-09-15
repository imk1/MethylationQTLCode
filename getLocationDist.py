def getLocation(line):
	# Get the location of the CpG island on the current line
	if line == "":
		# There is nothing left in the CpG island file
		return [("", 0, 0), True]
		
	lineElements = line.strip().split()
	location = (lineElements[0], int(lineElements[1]))
	return [location, False]


def getLocationDist(methylFileName, locationFileName, outputFileName):
	# Get the distance of the CpG in each SNP, CpG pair from the location in a list of locations
	# ASSUMES THAT SNPMethylFile IS SORTED BY CpG CHROMOSOME, CpG POSITION
	# ASSUMES THAT locationFile IS SORTED BY LOCATION CHROMOSOME, LOCATION START/POSITION
	# ASSUMES THAT THERE IS AT LEAST 1 CpG ISLAND ON EVERY CHROMOSOME
	methylFile = open(methylFileName)
	locationFile = open(locationFileName)
	outputFile = open(outputFileName, 'w+')
	[location, atLocationFileEnd] = getLocation(locationFile.readline())
	lastLocation = location
	
	for line in methylFile:
		# Iterate through the SNP, CpG file and compute the distance of each CpG from the nearest location in the list of locations
		lineElements = line.split("\t")
		CpGPosition = (lineElements[0], int(lineElements[1]))
		if lastLocation[0] < CpGPosition[0]:
			# Go to the next location
			lastLocation = location
		while lastLocation[0] < CpGPosition[0]:
			# Go to the next location until one on the correct chromosome is reached
			[location, atLocationFileEnd] = getLocation(locationFile.readline())
			lastLocation = location
		smallestDist = min([abs(CpGPosition[1]-lastLocation[1]), abs(CpGPosition[1]-location[1])])
		
		if (not atLocationFileEnd) and (smallestDist == abs(CpGPosition[1]-location[1])):
			# Not at the end of the location file but the closest CpG is the last that was read, so search for closer locations
			lastLocation = location
			while smallestDist > 0:
				# Iterate through the locationsuntil the closest is found
				[location, atLocationFileEnd] = getLocation(locationFile.readline())
				if atLocationFileEnd:
					# At the end of the location file, so stop
					break
				if location[0] > CpGPosition[0]:
					# The location is on a different chromosome, so stop
					break
				currentDist = abs(CpGPosition[1]-location[1])
				if currentDist <= smallestDist:
					# The current location is closer to the CpG than the previous location
					smallestDist = currentDist
					lastLocation = location
				else:
					break
					
		outputFile.write(CpGPosition[0] + "\t" + str(CpGPosition[1]) + "\t" + str(smallestDist) + "\n")
	methylFile.close()
	locationFile.close()
	outputFile.close()
	
	
if __name__=="__main__":
	import sys
	methylFileName = sys.argv[1]
	locationFileName = sys.argv[2]
	outputFileName = sys.argv[3]
	
	getLocationDist(methylFileName, locationFileName, outputFileName)