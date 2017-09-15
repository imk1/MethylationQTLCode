def makeGetSNPMethylReadsPlusReadPositionScript(bismarkSNPFileListFileName, bismarkMethylationFileListFileName, methylLetter, CGDist, outputFileNamePath, outputFileNameSuffix, scriptFileName, codePath):
	# Write a script that will run getSNPMethylReads.py on each pair of methylation, SNP files
	bismarkSNPFileListFile = open(bismarkSNPFileListFileName)
	bismarkMethylationFileListFile = open(bismarkMethylationFileListFileName)
	scriptFile = open(scriptFileName, 'w+')

	for line in bismarkSNPFileListFile:
		# Iterate through the SNP files and make a line in the script for each and its methylation file pair
		# ASSUMES THAT EACH SNP AND METHYLATION FILE IS FROM THE SAME UNIQUE SAMPLE AND STRAND
		bismarkSNPFileName = line.strip()
		bismarkMethylationFileName = bismarkMethylationFileListFile.readline().strip()
		bismarkMethylationFileNameElements = bismarkMethylationFileName.split("/")
		bismarkMethylationFileNameSpecificElements = bismarkMethylationFileNameElements[-1].split("_1_")
		outputFileName = outputFileNamePath + "/" + bismarkMethylationFileNameSpecificElements[0] + "_" + outputFileNameSuffix
		scriptFile.write("python " + codePath + "/" + "getSNPMethylReadsPlusReadPosition.py " + bismarkSNPFileName + " " + bismarkMethylationFileName + " " + methylLetter + " " + str(CGDist) + " " + outputFileName + "\n")

	bismarkSNPFileListFile.close()
	bismarkMethylationFileListFile.close()
	scriptFile.close()

if __name__=="__main__":
	import sys
	bismarkSNPFileListFileName = sys.argv[1]
	bismarkMethylationFileListFileName = sys.argv[2]
	methylLetter = sys.argv[3]
	CGDist = int(sys.argv[4])
	outputFileNamePath = sys.argv[5] # Should not end with /
	outputFileNameSuffix = sys.argv[6] # Should end with .gz
	scriptFileName = sys.argv[7]
	codePath = sys.argv[8] # Should not end with /

	makeGetSNPMethylReadsPlusReadPositionScript(bismarkSNPFileListFileName, bismarkMethylationFileListFileName, methylLetter, CGDist, outputFileNamePath, outputFileNameSuffix, scriptFileName, codePath)
