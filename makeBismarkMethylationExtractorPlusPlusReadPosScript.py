def makeBismarkMethylationExtractorPlusPlusReadPosScript(bismarkFileNameListFileName, outputDir, ignoreR2Val, maxLen, maxLenR2, scriptFileName, codePath):
	# Write a script that will extract the methylation status from Bismark output files
	bismarkFileNameListFile = open(bismarkFileNameListFileName)
	scriptFile = open(scriptFileName, 'w+')
	for line in bismarkFileNameListFile:
		# Iterate through the Bismark output files and write a line in the script to extract the methylation for each
		scriptFile.write("perl " + codePath + "/bismark_methylation_extractor_plusplus_readPos.pl -p --no_overlap -o " + outputDir + (" --gzip --ignore_r2 ") + str(ignoreR2Val) + " --max_len " + str(maxLen) + " --max_len_r2 " + str(maxLenR2) + " " + line.strip() + "\n")
	bismarkFileNameListFile.close()
	scriptFile.close()

if __name__=="__main__":
	import sys
	bismarkFileNameListFileName = sys.argv[1]
	outputDir = sys.argv[2]
	ignoreR2Val = int(sys.argv[3])
	maxLen = int(sys.argv[4])
	maxLenR2 = int(sys.argv[5])
	scriptFileName = sys.argv[6]
	codePath = sys.argv[7] # Should not end with /
	makeBismarkMethylationExtractorPlusPlusReadPosScript(bismarkFileNameListFileName, outputDir, ignoreR2Val, maxLen, maxLenR2, scriptFileName, codePath)
