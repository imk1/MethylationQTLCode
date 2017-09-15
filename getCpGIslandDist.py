def getCpGIsland(line):
	# Get the location of the CpG island on the current line
	if line == "":
		# There is nothing left in the CpG island file
		return [("", 0, 0), True]
		
	lineElements = line.strip().split()
	CpGIsland = (lineElements[0], int(lineElements[1]), int(lineElements[2]))
	return [CpGIsland, False]

	
def getDist(CpGPosition, CpGIsland):
	# Get the distances from a CpG to a CpG island on the same chromosome
	startDist = abs(CpGPosition[1] - CpGIsland[1])
	endDist = abs(CpGPosition[1] - CpGIsland[2])
	
	dist = min([startDist, endDist])
	return dist


def getCpGIslandDist(methylFileName, CpGIslandFileName, outputFileName):
	# Get the distance of the CpG in each SNP, CpG pair from the nearest CpG island
	# ASSUMES THAT SNPMethylFile IS SORTED BY CpG CHROMOSOME, CpG POSITION
	# ASSUMES THAT CpGIslandFile IS SORTED BY CpG ISLAND CHROMOSOME, CpG ISLAND START, CpG ISLAND END
	# ASSUMES THAT THERE IS AT LEAST 1 CpG ISLAND ON EVERY CHROMOSOME
	methylFile = open(methylFileName)
	CpGIslandFile = open(CpGIslandFileName)
	outputFile = open(outputFileName, 'w+')
	[CpGIsland, atCpGIslandFileEnd] = getCpGIsland(CpGIslandFile.readline())
	lastCpGIsland = CpGIsland
	
	for line in methylFile:
		# Iterate through the SNP, CpG file and compute the distance of each CpG from the nearest CpG island
		lineElements = line.split("\t")
		CpGPosition = (lineElements[0], int(lineElements[1]))
		if lastCpGIsland[0] < CpGPosition[0]:
			# Go to the next CpG island
			lastCpGIsland = CpGIsland
		while lastCpGIsland[0] < CpGPosition[0]:
			# Go to the next CpG island until one on the correct chromosome is reached
			[CpGIsland, atCpGIslandFileEnd] = getCpGIsland(CpGIslandFile.readline())
			lastCpGIsland = CpGIsland
		smallestDist = min([getDist(CpGPosition, lastCpGIsland), getDist(CpGPosition, CpGIsland)])
		
		if (not atCpGIslandFileEnd) and (smallestDist == getDist(CpGPosition, CpGIsland)):
			# Not at the end of the CpG island file but the closest CpG is the last that was read, so search for closer CpG islands
			lastCpGIsland = CpGIsland
			while smallestDist > 0:
				# Iterate through the CpG islands until the closest is found
				[CpGIsland, atCpGIslandFileEnd] = getCpGIsland(CpGIslandFile.readline())
				if atCpGIslandFileEnd:
					# At the end of the CpG island file, so stop
					break
				if CpGIsland[0] > CpGPosition[0]:
					# The CpG island is on a different chromosome, so stop
					break
				currentDist = getDist(CpGPosition, CpGIsland)
				if currentDist < smallestDist:
					# The current CpG island is closer to the CpG than the previous CpG island
					smallestDist = currentDist
					lastCpGIsland = CpGIsland
				else:
					break
					
		outputFile.write(CpGPosition[0] + "\t" + str(CpGPosition[1]) + "\t" + str(smallestDist) + "\n")
	methylFile.close()
	CpGIslandFile.close()
	outputFile.close()
	
	
if __name__=="__main__":
	import sys
	methylFileName = sys.argv[1]
	CpGIslandFileName = sys.argv[2]
	outputFileName = sys.argv[3]
	
	getCpGIslandDist(methylFileName, CpGIslandFileName, outputFileName)