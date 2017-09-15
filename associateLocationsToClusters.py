def getNextLocation(clusterFile):
	# Gets the location of the next region in a cluster
	currentClusterLine = clusterFile.readline()
	if currentClusterLine != "":
		# Not at the end of the file
		currentClusterLineElements = currentClusterLine.split("\t")
		currentClusterLocation = (currentClusterLineElements[0], int(currentClusterLineElements[1]), int(currentClusterLineElements[2].strip()))
	else:
		currentClusterLocation = ("", -1, -1)
	return currentClusterLocation


def associateLocationsToClusters(locationFileName, clusterFileNameListFileName, outputFileName, defaultClustNum):
	# Find the cluster for each location
	# Assumes that each base has been assigned to exactly 1 cluster
	# ASSUMES THAT REGION AND CLUSTER FILES HAVE BEEN SORTED BY CHROM, THEN START, THEN END
	locationFile = open(locationFileName)
	clusterFileNameListFile = open(clusterFileNameListFileName)
	outputFile = open(outputFileName, 'w+')
	clusterFileList = []
	currentClusterLocationList = []
	for line in clusterFileNameListFile:
		# Iterate through the cluster file names and open each file
		clusterFile = open(line.strip())
		clusterFileList.append(clusterFile)
		currentClusterLine = clusterFile.readline()
		currentClusterLineElements = currentClusterLine.split("\t")
		currentClusterLocation = (currentClusterLineElements[0], int(currentClusterLineElements[1]), int(currentClusterLineElements[2].strip()))
		currentClusterLocationList.append(currentClusterLocation)

	for line in locationFile:
		# Iterate through regions and find the cluster for each region
		lineElements = line.split("\t")
		chrom = lineElements[0]
		location = int(lineElements[1])
		clusterNum = -1
		for i in range(len(clusterFileList)):
			# Iterate through clusters until the cluster with the middle of the region has been found
			if currentClusterLocationList[i][0] == "":
				# All parts of the current cluster have been seen, so continue
				continue
			allClusterSeen = False
			while currentClusterLocationList[i][0] < chrom:
				# Iterate through the cluster's regions until one on the same chromosome has been found
				if currentClusterLocationList[i][0] == "":
					# All parts of the current cluster have been seen, so stop
					allClusterSeen = True
					break
				currentClusterLocationList[i] = getNextLocation(clusterFileList[i])
			if allClusterSeen == True:
				# All of the current cluster has been seen, so continue
				continue
			while (currentClusterLocationList[i][2] < location) and (currentClusterLocationList[i][0] == chrom):
				# Iterate through the cluster's regions until one not before location has been found
				currentClusterLocationList[i] = getNextLocation(clusterFileList[i])
				if currentClusterLocationList[i][0] == "":
					# All parts of the current cluster have been seen, so stop
					allClusterSeen = True
					break
			if allClusterSeen == True:
				# All of the current cluster has been seen, so continue
				continue
			if (location >= currentClusterLocationList[i][1]) and (location < currentClusterLocationList[i][2]):
				# The region belongs to the current cluster
				clusterNum = i + 1
				break
		if clusterNum == -1:
			print "Problem!"
			print line[:-1]
			print currentClusterLocationList
			clusterNum = defaultClustNum
		outputFile.write(str(clusterNum) + "\n")

	locationFile.close()
	for clusterFile in clusterFileList:
		# Iterate through the files with the clusters and close each cluster
		clusterFile.close()
	outputFile.close()


if __name__=="__main__":
	import sys
	locationFileName = sys.argv[1]
	clusterFileNameListFileName = sys.argv[2]
	outputFileName = sys.argv[3]
	defaultClustNum = int(sys.argv[4])
                        
	associateLocationsToClusters(locationFileName, clusterFileNameListFileName, outputFileName, defaultClustNum)
