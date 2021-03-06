def getInfo(line):
	# Get SNP or methylation information from a line of the file
	lineElements = line.strip().split("\t")
	location = (lineElements[0], int(lineElements[1]))
	
	vals = []
	for le in lineElements[2:]:
		# Iterate through the SNP or methylation values and add them to a vector
		vals.append(float(le))
	return [location, vals]


def makeCorrelateSNPsMethylationMoen(methylFileNameListFileName, SNPsFileNameListFileName, distanceCutoff, outputFileNameSuffix, scriptFileName, codePath):
	# Make a script that correlates methylation statuses and SNPs for data from individual arrays
	# ASSUMES THAT THE ROWS IN methylFileNameListFile AND SNPsFileNameListFile CORRESPOND TO EACH OTHER
	methylFileNameListFile = open(methylFileNameListFileName)
	SNPsFileNameListFile = open(SNPsFileNameListFileName)
	scriptFile = open(scriptFileName, 'w+')
	
	for line in methylFileNameListFile:
		# For each methylation and SNP file, write a line in the script that will correlate the methylation and SNP data
		methylFileName = line.strip()
		SNPFileName = SNPsFileNameListFile.readline().strip()
		methylFileNameElements = methylFileName.split("_")
		outputFileName = methylFileNameElements[0] + "_" + methylFileNameElements[1] + "_" + outputFileNameSuffix
		scriptFile.write("python " + codePath + "/correlateSNPsMethylationMoen.py " + methylFileName + " " + SNPFileName + " " + str(distanceCutoff) + " " + outputFileName + "\n")
	
	methylFileNameListFile.close()
	SNPsFileNameListFile.close()
	scriptFile.close()


if __name__=="__main__":
	import sys
	methylFileNameListFileName = sys.argv[1]
	SNPsFileNameListFileName = sys.argv[2]
	distanceCutoff = int(sys.argv[3])
	outputFileNameSuffix = sys.argv[4] # Should not start with _
	scriptFileName = sys.argv[5]
	codePath = sys.argv[6] # Should not end with /

	makeCorrelateSNPsMethylationMoen(methylFileNameListFileName, SNPsFileNameListFileName, distanceCutoff, outputFileNameSuffix, scriptFileName, codePath)