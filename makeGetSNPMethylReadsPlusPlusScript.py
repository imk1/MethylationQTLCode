def makeGetSNPMethylReadsPlusPlusScript(bismarkSNPFileListFileName, bismarkMethylationFileListFileName, regionsWithSNPsFileName, methylLetter, CGDist, countStart, outputFileNamePath, outputFileNameSuffix, scriptFileName, codePath):
	# Write a script that will run getSNPMethylReads.py on each pair of methylation, SNP files
	bismarkSNPFileListFile = open(bismarkSNPFileListFileName)
	bismarkMethylationFileListFile = open(bismarkMethylationFileListFileName)
	scriptFile = open(scriptFileName, 'w+')
	count = countStart

	for line in bismarkSNPFileListFile:
		# Iterate through the SNP files and make a line in the script for each and its methylation file pair
		# ASSUMES THAT EACH SNP AND METHYLATION FILE IS FROM THE SAME UNIQUE SAMPLE AND STRAND
		bismarkSNPFileName = line.strip()
		bismarkMethylationFileName = bismarkMethylationFileListFile.readline().strip()
		bismarkMethylationFileNameElements = bismarkMethylationFileName.split("/")
		bismarkMethylationFileNameSpecificElements = bismarkMethylationFileNameElements[-1].split("_1_")
		outputFileName = outputFileNamePath + "/" + bismarkMethylationFileNameSpecificElements[0] + "_" + outputFileNameSuffix
		scriptFile.write("python " + codePath + "/" + "getSNPMethylReadsPlusPlus.py " + bismarkSNPFileName + " " + bismarkMethylationFileName + " " + regionsWithSNPsFileName + " " + methylLetter + " " + str(CGDist) + " " + str(count) + " " + outputFileName + "\n")
		count = count + 1

	print count
	bismarkSNPFileListFile.close()
	bismarkMethylationFileListFile.close()
	scriptFile.close()

if __name__=="__main__":
	import sys
	bismarkSNPFileListFileName = sys.argv[1]
	bismarkMethylationFileListFileName = sys.argv[2] # Should end with .gz
	regionsWithSNPsFileName = sys.argv[3]
	methylLetter = sys.argv[4]
	CGDist = int(sys.argv[5])
	countStart = int(sys.argv[6])
	outputFileNamePath = sys.argv[7] # Should not end with /
	outputFileNameSuffix = sys.argv[8] # Should end with .gz
	scriptFileName = sys.argv[9]
	codePath = sys.argv[10] # Should not end with /

	makeGetSNPMethylReadsPlusPlusScript(bismarkSNPFileListFileName, bismarkMethylationFileListFileName, regionsWithSNPsFileName, methylLetter, CGDist, countStart, outputFileNamePath, outputFileNameSuffix, scriptFileName, codePath)
