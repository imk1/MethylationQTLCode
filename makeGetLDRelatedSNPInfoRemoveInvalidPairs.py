def makeGetLDRelatedSNPInfoRemoveInvalidPairs(genotypeFileNameListFileName, suffix, distanceCutoff, scriptFileName, codePath):
	# Make a script that will run getLDRelatedSNPInfoRemoveInvalidPairs.py for each file in a list
	genotypeFileNameListFile = open(genotypeFileNameListFileName)
	scriptFile = open(scriptFileName, 'w+')
	for line in genotypeFileNameListFile:
		# Iterate through the genotype files and make a line in the script for each
		genotypeFileName = line.strip()
		genotypeFileNameElements = genotypeFileName.split(".")
		fileTypeLength = len(genotypeFileNameElements[-1]) + 1 +  len(genotypeFileNameElements[-2])
		outputFileName = genotypeFileName[0:len(genotypeFileName) - fileTypeLength] + suffix
		scriptFile.write("python " + codePath + "/" + "getLDRelatedSNPInfoRemoveInvalidPairs.py " + genotypeFileName + " " + outputFileName + " " + str(distanceCutoff) + "\n")
	genotypeFileNameListFile.close()
	scriptFile.close()

if __name__=="__main__":
	import sys
	genotypeFileNameListFileName = sys.argv[1]
	suffix = sys.argv[2] # Should not start with .
	distanceCutoff = int(sys.argv[3])
	scriptFileName = sys.argv[4]
	codePath = sys.argv[5] # Should not end with /
	makeGetLDRelatedSNPInfoRemoveInvalidPairs(genotypeFileNameListFileName, suffix, distanceCutoff, scriptFileName, codePath)