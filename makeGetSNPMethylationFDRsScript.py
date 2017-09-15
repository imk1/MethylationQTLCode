def makeGetSNPMethylationFDRsScript(SNPMethylEffectSizesFileName, SNPMethylEffectSizesRandFileNamePrefix, numIters, SNPMethylCutoffPlusFileNamePrefix, corrCutoffList, FDRFileNamePrefix, scriptFileName, codePath):
	# Make a script that will get the methylation FDRs for each correlation cutoff
	scriptFile = open(scriptFileName, 'w+')
	for corrCutoff in corrCutoffList:
		# Write the command for each correlation cutoff
		SNPMethylCutoffPlusFileName = SNPMethylCutoffPlusFileNamePrefix + "_" + str(corrCutoff)
		FDRFileName = FDRFileNamePrefix + "_" + str(corrCutoff)
		scriptFile.write("python "  + codePath + "/" + "getSNPMethylationFDRs.py " + SNPMethylEffectSizesFileName + " " + SNPMethylEffectSizesRandFileNamePrefix + " " + str(numIters) + " " + SNPMethylCutoffPlusFileName + " " + str(corrCutoff) + " " + FDRFileName + "\n")
	scriptFile.close()

if __name__=="__main__":
	import sys
	import gzip
	SNPMethylEffectSizesFileName = sys.argv[1] # Should not start with _
	SNPMethylEffectSizesRandFileNamePrefix = sys.argv[2] # Should not start with _
	numIters = int(sys.argv[3])
	SNPMethylCutoffPlusFileNamePrefix = sys.argv[4] # Should start with _
	FDRFileNamePrefix = sys.argv[5]
	scriptFileName = sys.argv[6]
	codePath = sys.argv[7] # Should not end with /
	corrCutoffList = []
	for cc in sys.argv[8:]:
		# Iterate through the correlation cutoffs and add each to the list
		corrCutoffList.append(float(cc))
	makeGetSNPMethylationFDRsScript(SNPMethylEffectSizesFileName, SNPMethylEffectSizesRandFileNamePrefix, numIters, SNPMethylCutoffPlusFileNamePrefix, corrCutoffList, FDRFileNamePrefix, scriptFileName, codePath)