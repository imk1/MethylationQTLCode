def makeRemoveBedFromSamScript (samFileNameListFileName, bedFileName, outputFileNameSuffix, scriptFileName, codePath):
	samFileNameListFile = open(samFileNameListFileName)
	scriptFile = open(scriptFileName, 'w+')
	
	for line in samFileNameListFile:
		# Iterate through the sam file names and make a line in the script for each
		lineElements = line.strip().split(".")
		outputFileName = line[0:len(line)-len(lineElements[-1])-1] + outputFileNameSuffix
		scriptFile.write("python " + codePath + "/removeBedFromSam.py " + line.strip() + " " + bedFileName + " " + outputFileName + "\n")
		
	samFileNameListFile.close()
	scriptFile.close()


if __name__=="__main__":
	import sys
	samFileNameListFileName = sys.argv[1]
	bedFileName = sys.argv[2]
	outputFileNameSuffix = sys.argv[3] # Should not start with .
	scriptFileName = sys.argv[4]
	codePath = sys.argv[5] # Should not end with /

	makeRemoveBedFromSamScript (samFileNameListFileName, bedFileName, outputFileNameSuffix, scriptFileName, codePath)