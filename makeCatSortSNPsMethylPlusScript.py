def makeStringList(stringListFileName):
	# Make a list of Strings from a file
	stringListFile = open(stringListFileName)
	stringList = []
	for line in stringListFile:
		# Iterate through the lines of the file and add each line to the list
		stringList.append(line.strip())
	stringListFile.close()
	return stringList

def makeStringLastList(stringListFileName, delim):
	# Make a list of Strings from a file
	stringListFile = open(stringListFileName)
	stringList = []
	for line in stringListFile:
		# Iterate through the lines of the file and add each line to the list
		lineElements =line.strip().split(delim)
		stringList.append(lineElements[-1])
	stringListFile.close()
	return stringList

def makeCatSortSNPsMethylPlusScript(fileNameListFileName, chromListFileName, filePath, ouputFileNameSuffix, scriptFileName, tempFileName):
	# Make a script that will concatenate the files with reads from each chromosome and sort the concatenated files
	chromList = makeStringList(chromListFileName)
	fileNameList = makeStringLastList(fileNameListFileName, "/")
	scriptFile = open(scriptFileName, 'w+')
	for chrom in chromList:
		# Iterate through the chromosomes and write a line that will create a separate, sorted file for each
		scriptFile.write("zcat")
		for fileName in fileNameList:
			# Concatenate every file for the current chromosome
			chromFileName = filePath + "/" + chrom + "_" + fileName
			scriptFile.write(" " + chromFileName)
		outputFileName = filePath + "/" + chrom + "_" + ouputFileNameSuffix
		scriptFile.write(" | sort -k5,5 -k6,6n -k2,2 -k3,3n -T " + tempFileName + " | gzip > " + outputFileName + "\n")
	scriptFile.close()

if __name__=="__main__":
   import sys
   fileNameListFileName = sys.argv[1] # SHOULD BE SNPsMethyl PRE-CHROMOSOME-SEPARATION FILE NAMES
   chromListFileName = sys.argv[2]
   filePath = sys.argv[3] # Should not end with /
   ouputFileNameSuffix = sys.argv[4] # Should not start with _, but should end with .gz
   scriptFileName = sys.argv[5]
   tempFileName = sys.argv[6] # Should start with /
   makeCatSortSNPsMethylPlusScript(fileNameListFileName, chromListFileName, filePath, ouputFileNameSuffix, scriptFileName, tempFileName)