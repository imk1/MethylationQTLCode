def makeGetPerfectLDScript(genotypeFileNameListFileName, suffix, distanceCutoff, scriptFileName, codePath, pythonPath):
	# Make a script that runs getPerfectLDSNPs.py on a list of files
	genotypeFileNameListFile = open(genotypeFileNameListFileName)
	scriptFile = open(scriptFileName, 'w+')
	for line in genotypeFileNameListFile:
		# Iterate through the file names and make a line in the script for each
		outputFileName = line.strip() + "." + str(suffix)
		pythonCmd = pythonPath + "/" + "python"
		codeCmd = codePath + "/" + "getPerfectLDSNPs.py"
		scriptFile.write(pythonCmd + " " + codeCmd + " " + line.strip() + " " +  outputFileName + " " + str(distanceCutoff) + "\n")
	genotypeFileNameListFile.close()
	scriptFile.close()
	
if __name__=="__main__":
	import sys
	genotypeFileNameListFileName = sys.argv[1]
	suffix = sys.argv[2] # Should not start with .
	distanceCutoff = int(sys.argv[3])
	scriptFileName = sys.argv[4]
	codePath = sys.argv[5] # Should not end with /
	pythonPath = sys.argv[6] # Should not end with /
	makeGetPerfectLDScript(genotypeFileNameListFileName, suffix, distanceCutoff, scriptFileName, codePath, pythonPath)