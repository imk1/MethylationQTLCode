def makeStringList(stringListFileName):
	# Make a list of Strings from a file
	stringListFile = open(stringListFileName)
	stringList = []
	for line in stringListFile:
		# Iterate through the lines of the file and add each line to the list
		stringList.append(line.strip())
	stringListFile.close()
	return stringList

def makeGrepSortScript(readsFileName, chromListFileName, scriptFileName):
	# Make a script that will divide a file with reads into a separate file for each chrom. and sort the dividied files
	chromList = makeStringList(chromListFileName)
	scriptFile = open(scriptFileName, 'w+')
	readsFileNameElements = readsFileName.split("/")
	readsFileNameSuffix = readsFileNameElements[-1]
	readsFileNamePath = readsFileName[0:len(readsFileName) - len(readsFileNameSuffix)]
	for chrom in chromList:
		# Iterate through the chromosomes and write a line that will create a separate, sorted file for each
		outputFileName = readsFileNamePath + chrom + "_" + readsFileNameSuffix
		scriptFile.write("zgrep -P '" + chrom + "\\t' " + readsFileName + " | sort -k2,2 -k3,3n -T /tmp | gzip > " + outputFileName + "\n")
	scriptFile.close()

if __name__=="__main__":
   import sys
   readsFileName = sys.argv[1] 
   chromListFileName = sys.argv[2]
   scriptFileName = sys.argv[3]
   makeGrepSortScript(readsFileName, chromListFileName, scriptFileName)
