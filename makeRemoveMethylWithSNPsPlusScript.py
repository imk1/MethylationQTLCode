def makeRemoveMethylWithSNPsPlusScript(bismarkMethylationFileListFileName, regionsWithSNPsFileName, CGDist, outputFileNameSuffix, scriptFileName, codePath):
	# Make a script that will the CpGs that contain SNPs from the methylation file from Bismark
	bismarkMethylationFileListFile = open(bismarkMethylationFileListFileName)
	scriptFile = open(scriptFileName, 'w+')
	
	for line in bismarkMethylationFileListFile:
		# Iterate through the files and write a line in the script for each
		bismarkMethylationFileName = line.strip()
		bismarkMethylationFileNameElements = bismarkMethylationFileName.split(".")
		outputFileNamePrefix = bismarkMethylationFileName[0:len(bismarkMethylationFileName) - len(bismarkMethylationFileNameElements[-1]) - 1]
		outputFileName = outputFileNamePrefix + "." + outputFileNameSuffix
		scriptFile.write("python " + codePath + "/" + "removeMethylWithSNPsPlus.py " + bismarkMethylationFileName + " " + regionsWithSNPsFileName + " " + str(CGDist) + " " + outputFileName + "\n")
		
	bismarkMethylationFileListFile.close()
	scriptFile.close()


if __name__=="__main__":
	import sys
	import gzip
	bismarkMethylationFileListFileName = sys.argv[1] # Files should end with .gz
	regionsWithSNPsFileName = sys.argv[2]
	CGDist = int(sys.argv[3])
	outputFileNameSuffix = sys.argv[4] # Should end with .gz, should not start with .
	scriptFileName = sys.argv[5]
	codePath = sys.argv[6]

	makeRemoveMethylWithSNPsPlusScript(bismarkMethylationFileListFileName, regionsWithSNPsFileName, CGDist, outputFileNameSuffix, scriptFileName, codePath)
