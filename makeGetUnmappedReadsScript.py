def makeGetUnmappedReadsScript(samFileNameListFileName, fastqFileNameListFileName, fastqFileNameListTwoFileName, unmappedReadsFileNameSuffix, scriptFileName, codePath):
	# Make a script that will get the unmapped reads for a list of fastq files
	# ASSUMES THAT THE SAME AND FASTQ FILES ON EACH LINE OF THE LISTS CORRESPOND TO EACH OTHER
	samFileNameListFile = open(samFileNameListFileName)
	fastqFileNameListFile = open(fastqFileNameListFileName)
	fastqFileNameListTwoFile = open(fastqFileNameListTwoFileName)
	scriptFile = open(scriptFileName, 'w+')
	
	for line in fastqFileNameListFile:
		# Iterate through the fastq files and make a script for each and its corresponding sam file
		fastqFileName = line.strip()
		fastqFileTwoName = fastqFileNameListTwoFile.readline().strip()
		lineElements = fastqFileName.split(".")
		fastqFileNameSuffixLength = len(lineElements[-2]) + 1 + len(lineElements[-1])
		unmappedReadsFileName = fastqFileName[0:len(fastqFileName)-fastqFileNameSuffixLength-1] + "." + unmappedReadsFileNameSuffix
		unmappedReadsFileTwoName = fastqFileTwoName[0:len(fastqFileTwoName)-fastqFileNameSuffixLength-1] + "." + unmappedReadsFileNameSuffix
		samFileName = samFileNameListFile.readline().strip()
		scriptFile.write("python " + codePath + "/" + "getUnmappedReads.py " + samFileName + " " + fastqFileName + " "  + fastqFileTwoName + " " + unmappedReadsFileName + " " + unmappedReadsFileTwoName + "\n")
	
	samFileNameListFile.close()
	fastqFileNameListFile.close()
	scriptFile.close()

	
if __name__=="__main__":
	import sys
	import gzip
	samFileNameListFileName = sys.argv[1] # Should not end with .
	fastqFileNameListFileName = sys.argv[2] # Lines should end with .gz
	fastqFileNameListTwoFileName = sys.argv[3] # Lines should end with .gz
	unmappedReadsFileNameSuffix = sys.argv[4] # Should end with .gz
	scriptFileName = sys.argv[5]
	codePath = sys.argv[6] # Should not end with /

	makeGetUnmappedReadsScript(samFileNameListFileName, fastqFileNameListFileName, fastqFileNameListTwoFileName, unmappedReadsFileNameSuffix, scriptFileName, codePath)