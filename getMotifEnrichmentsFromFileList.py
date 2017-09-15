def getMotifEnrichmentFromFile(inputFileName, qValueCutoff, outputFile):
	# Get motifs found around a SNP from a file
	inputFile = open(inputFileName)
	inputFile.readline() # Remove the header
	for line in inputFile:
		# Iterate through the motifs in the file and record those with sufficiently low q-values
		lineElements = line.strip().split("\t")
		qValue = float(lineElements[4])
		if qValue < qValueCutoff:
			# The q-value is sufficiently low
			outputFile.write(inputFileName + "\t" + lineElements[0] + "\n")
	inputFile.close()
	return outputFile

def getMotifEnrichmentFromFileList(motifFileNameListFileName, qValueCutoff, outputFileName):
	# Get motifs found around SNPs in a list of files
	# outputFile contains 2 columns:
	# 1.  Name of motif file
	# 2.  Motif
	motifFileNameListFile = open(motifFileNameListFileName)
	outputFile = open(outputFileName, 'w+')
	for line in motifFileNameListFile:
		# Iterate through the files with motifs and get the motifs found in each
		outputFile = getMotifEnrichmentFromFile(line.strip(), qValueCutoff, outputFile)
	motifFileNameListFile.close()
	outputFile.close()

if __name__=="__main__":
	import sys
	motifFileNameListFileName = sys.argv[1]
	qValueCutoff = float(sys.argv[2]) # Usually use 0.05
	outputFileName = sys.argv[3]
	getMotifEnrichmentFromFileList(motifFileNameListFileName, qValueCutoff, outputFileName)
	