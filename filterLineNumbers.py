def makeIntList(intFileName):
	# Make a list of ints from a file
	intFile = open(intFileName)
	intList = []
	for line in intFile:
		# Iterate through the lines of intFile and put each int into the list
		intList.append(int(line.strip()))
	intFile.close()
	return intList

def filterLineNumbers(inputFileName, lineNumbersToKeep, outputFileName):
	# Filter a file so that only lines in lineNumbersToKeep remain
	# ASSUMES THAT lineNumbersToKeep ARE 0-INDEXED OR 1-INDEXED IF inputFile HAS A HEADER LINE
	inputFile = open(inputFileName)
	count = 0
	outputFile = open(outputFileName, 'w+')
	for line in inputFile:
		# Iterate through the lines of the input file and record those whose indexes are in lineNumbersToKeep
		if count in lineNumbersToKeep:
			# Record the current line
			outputFile.write(line)
		count = count + 1
	inputFile.close()
	outputFile.close()

if __name__=="__main__":
   import sys
   inputFileName = sys.argv[1] 
   lineNumbersToKeepFileName = sys.argv[2]
   outputFileName = sys.argv[3]
   lineNumbersToKeep = makeIntList(lineNumbersToKeepFileName)
   filterLineNumbers(inputFileName, lineNumbersToKeep, outputFileName)