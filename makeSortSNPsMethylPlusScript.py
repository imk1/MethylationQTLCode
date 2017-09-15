def makeStringList(stringListFileName):
	# Make a list of Strings from a file
	stringListFile = open(stringListFileName)
	stringList = []
	for line in stringListFile:
		# Iterate through the lines of the file and add each line to the list
		stringList.append(line.strip())
	stringListFile.close()
	return stringList

def makeSortSNPsMethylPlusScript(readsFileNameSuffix, filePath, chromListFileName, ouputFileNameSuffix, scriptFileName):
	# Make a script that will divide a file with reads into a separate file for each chrom. and sort the dividied files
	chromList = makeStringList(chromListFileName)
	scriptFile = open(scriptFileName, 'w+')
	readsFileNameElements = readsFileNameSuffix.split(".")
	for chrom in chromList:
		# Iterate through the chromosomes and write a line that will create a separate, sorted file for each
		inputFileName = filePath + "/" + chrom + "_" + readsFileNameSuffix
		outputFileName = filePath + "/" + chrom + "_" + readsFileNameSuffix[0:len(readsFileNameSuffix)-len(readsFileNameElements[-1]) - 1] + "_" + ouputFileNameSuffix
		scriptFile.write("zcat " +inputFileName + " | sort -k5,5 -k6,6n -k2,2 -k3,3n -T /tmp " + " | gzip > " + outputFileName + "\n")
	scriptFile.close()

if __name__=="__main__":
   import sys
   readsFileNameSuffix = sys.argv[1] # Should not start with _, but should end with .gz
   filePath = sys.argv[2] # Should not end with /
   chromListFileName = sys.argv[3]
   ouputFileNameSuffix = sys.argv[4] # Should not start with _, but should end with .gz
   scriptFileName = sys.argv[5]
   makeSortSNPsMethylPlusScript(readsFileNameSuffix, filePath, chromListFileName, ouputFileNameSuffix, scriptFileName)
