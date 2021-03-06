def makeIGVToolsSortScript(bismarkFileNameListFileName, suffix, scriptFileName, codePath):
	# Make a script that will use gatk to convert Hapmap files to VCF files
	bismarkFileNameListFile = open(bismarkFileNameListFileName)
	scriptFile = open(scriptFileName, 'w+')	

	for line in bismarkFileNameListFile:
		# Iterate through the chromosomes and write a line in the script for each for each population
		bismarkFileName = line.strip()
		bismarkFileNameElements = bismarkFileName.split(".")
		fileTypeLength = len(bismarkFileNameElements[-1])
		outputFileName = bismarkFileName[0:len(bismarkFileName) - fileTypeLength] + suffix
		scriptFile.write("java -Xmx4g -jar " + codePath + "/" + "igvtools.jar sort " + bismarkFileName + " " + outputFileName + "\n")

	bismarkFileNameListFile.close()
	scriptFile.close()


if __name__=="__main__":
	import sys
	bismarkFileNameListFileName = sys.argv[1]
	suffix = sys.argv[2]
	scriptFileName = sys.argv[3]
	codePath = sys.argv[4] # Should not contain a / at the end

	makeIGVToolsSortScript(bismarkFileNameListFileName, suffix, scriptFileName, codePath)
