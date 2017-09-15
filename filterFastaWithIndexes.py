def getIntList(intFileName):
	# Get a list of integers from a file
	intFile = open(intFileName)
	intList = []
	for line in intFile:
		# Iterate through the lines of the file and add each integer to list
		intList.append(int(line.strip()))
	intFile.close()
	return intList

def filterFastaWithIndexes(fastaFileName, indexesList, outputFileName):
	# Filter a fasta file to include only specificied entires
	fastaFile = open(fastaFileName)
	outputFile = open(outputFileName, 'w+')
	count = 0
	for line in fastaFile:
		# Iterate through the lines of the fasta file and record the entries specified in indexesList
		if line[0] == ">":
			# At the beginning of a new fasta entry
			count = count + 1
		if count in indexesList:
			# Record the current fasta entry
			outputFile.write(line)
	fastaFile.close()
	outputFile.close()

if __name__=="__main__":
   import sys
   fastaFileName = sys.argv[1] 
   indexesListFileName = sys.argv[2] # ASSUMES THAT THIS IS 1-INDEXED
   outputFileName = sys.argv[3]
   indexesList = getIntList(indexesListFileName)
   filterFastaWithIndexes(fastaFileName, indexesList, outputFileName)