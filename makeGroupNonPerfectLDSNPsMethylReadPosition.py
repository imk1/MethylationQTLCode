def makeGroupNonPerfectLDSNPsSNPsMethylReadPositionScript(SNPMethylFileNameListFileName, perfectLDSNPsFileNameListFileName, chromListFileName, outputFileNameSuffix, distanceCutoff, rCutoff, scriptFileName, codePath):
	# Make a script that will group SNP, CpG pairs for each chromosome based on LD
	# ASSUMES THAT THE ROWS IN SNPMethylFileNameListFile, perfectLDSNPsFileNameListFile, AND chromListFile LINE UP WITH EACH OTHER
	SNPMethylFileNameListFile = open(SNPMethylFileNameListFileName)
	perfectLDSNPsFileNameListFile = open(perfectLDSNPsFileNameListFileName)
	chromListFile = open(chromListFileName)
	scriptFile = open(scriptFileName, 'w+')
	for line in SNPMethylFileNameListFile:
		# Iterate through the SNPMethyl files and make a line in the script for each
		SNPMethylFileName = line.strip()
		perfectLDSNPsFileName = perfectLDSNPsFileNameListFile.readline().strip()
		chromName = chromListFile.readline().strip()
		SNPMethylFileNameElements = SNPMethylFileName.split("_")
		outputFileName = SNPMethylFileName[0:len(SNPMethylFileName)-len(SNPMethylFileNameElements[-1])] + outputFileNameSuffix
		cmd = "python " + codePath + "/" + "groupNonPerfectLDSNPsMethylReadPosition.py"
		scriptFile.write(cmd + " " + SNPMethylFileName + " " + perfectLDSNPsFileName + " " + chromName + " " + outputFileName + " " + str(distanceCutoff) + " " + str(rCutoff) + "\n")
	SNPMethylFileNameListFile.close()
	perfectLDSNPsFileNameListFile.close()
	chromListFile.close()
	scriptFile.close()

if __name__=="__main__":
	import sys
	import gzip
	SNPMethylFileNameListFileName = sys.argv[1] # Each line in it should end with .gz
	perfectLDSNPsFileNameListFileName = sys.argv[2]
	chromListFileName = sys.argv[3]
	outputFileNameSuffix = sys.argv[4] # Should end with .gz
	distanceCutoff = int(sys.argv[5])
	rCutoff = float(sys.argv[6])
	scriptFileName = sys.argv[7]
	codePath = sys.argv[8]
	makeGroupNonPerfectLDSNPsSNPsMethylReadPositionScript(SNPMethylFileNameListFileName, perfectLDSNPsFileNameListFileName, chromListFileName, outputFileNameSuffix, distanceCutoff, rCutoff, scriptFileName, codePath)