def makempileupScript(referenceGenomeFileName, bamFileNameListFileName, outputFileNamePrefix, outputFileNameSuffix, scriptFileName):
	# Make a script that will run mpileup on a list of bam files
	bamFileNameListFile = open(bamFileNameListFileName)
	scriptFile = open(scriptFileName, 'w+')
	for line in bamFileNameListFile:
		# Iterate through the bam files and write a line in the script for each
		lineElements = line.split("/")
		bamFileNameElements = lineElements[-1].split(".")
		outputFileName = outputFileNamePrefix + "/" + bamFileNameElements[0] + "." + outputFileNameSuffix
		scriptFile.write("samtools mpileup -f " + referenceGenomeFileName + " " + line.strip() + " > " + outputFileName + "\n")
	bamFileNameListFile.close()
	scriptFile.close()

if __name__=="__main__":
   import sys
   referenceGenomeFileName = sys.argv[1] 
   bamFileNameListFileName = sys.argv[2]
   outputFileNamePrefix = sys.argv[3] # Should not end with /
   outputFileNameSuffix = sys.argv[4] # Should not start with .
   scriptFileName = sys.argv[5]
   makempileupScript(referenceGenomeFileName, bamFileNameListFileName, outputFileNamePrefix, outputFileNameSuffix, scriptFileName)	
