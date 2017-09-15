def getRandomPositionPairs(distCountsFileName, chromName, chromLength, outputFileName):
	# Get a list of random position pairs that have the same length distribution as the true position pairs
	distCountsFile = open(distCountsFileName)
	outputFile = open(outputFileName, 'w+')
	dist = 0
	random.seed()
	
	for line in distCountsFile:
		# Iterate through the distances and get the appropriate number of random pairs for each distance
		for i in range(int(line.strip())):
			# Create the appropriate number of random pairs for the current distance
			randStart = random.randint(1, chromLength - dist)
			randEnd = randStart + dist
			outputFile.write(chromName + "\t" + str(randStart) + "\t" + str(randEnd) + "\n")
		dist = dist + 1
	
	distCountsFile.close()
	outputFile.close()

	
if __name__=="__main__":
	import sys
	import random
	distCountsFileName = sys.argv[1]
	chromName = sys.argv[2]
	chromLength = int(sys.argv[3])
	outputFileName = sys.argv[4]

	getRandomPositionPairs(distCountsFileName, chromName, chromLength, outputFileName)