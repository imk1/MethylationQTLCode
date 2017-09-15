def makeStringList(stringListFileName):
	# Make a list of Strings from a file
	stringList = []
	stringListFile = open(stringListFileName)
	
	for line in stringListFile:
		# Iterate through the Strings in the file and put each into the list
		stringList.append(line.strip())
		
	stringListFile.close()
	return stringList

def makeCatRandScript(chromList, fileNameMiddle, outputFileNamePrefix, filePath, iterStart, iterEnd, scriptFileName):
	# Make a script that will concatenate the chromosomes from each random iteration
	scriptFile = open(scriptFileName, 'w+')
	for i in range(iterStart, iterEnd + 1):
		# Make a line in the script for each iteration
		scriptFile.write("cat ")
		
		for chrom in chromList:
			# Iterate through the chromosomes and put each in the script
			fileName = filePath + "/" + chrom + "_" + fileNameMiddle + str(i)
			scriptFile.write(fileName + " ")
		
		allChromFileName = filePath + "/" + outputFileNamePrefix + str(i)
		scriptFile.write("> " + allChromFileName + "\n")
	scriptFile.close()

	
if __name__=="__main__":
	import sys
	chromListFileName = sys.argv[1]
	fileNameMiddle = sys.argv[2] # Should not start with _
	outputFileNamePrefix = sys.argv[3]
	filePath = sys.argv[4] # Should not end with /
	iterStart = int(sys.argv[5])
	iterEnd = int(sys.argv[6])
	scriptFileName = sys.argv[7]

	chromList = makeStringList(chromListFileName)
	makeCatRandScript(chromList, fileNameMiddle, outputFileNamePrefix, filePath, iterStart, iterEnd, scriptFileName)
