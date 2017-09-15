def makeBismarkMethylationExtractorScript(bismarkFileNameListFileName, outputDir, scriptFileName):
	# Write a script that will extract the methylation status from Bismark output files
	bismarkFileNameListFile = open(bismarkFileNameListFileName)
	scriptFile = open(scriptFileName, 'w+')
	for line in bismarkFileNameListFile:
		# Iterate through the Bismark output files and write a line in the script to extract the methylation for each
		scriptFile.write("bismark_methylation_extractor -p --no_overlap -o " + outputDir + (" --gzip ") + line.strip() + "\n")
	bismarkFileNameListFile.close()
	scriptFile.close()

if __name__=="__main__":
	import sys
	bismarkFileNameListFileName = sys.argv[1]
	outputDir = sys.argv[2]
	scriptFileName = sys.argv[3]
	makeBismarkMethylationExtractorScript(bismarkFileNameListFileName, outputDir, scriptFileName)
