def makeConvertGenotypesFileToBedgzipScript(populationGenotypeFileNamePrefix, chromListFileName, populationGenotypeFileNameSuffix, chromCol, positionCol,  scriptFileName, codePath):
	# Make a script that will use gatk to convert Hapmap files to VCF files
	chromListFile = open(chromListFileName)
	scriptFile = open(scriptFileName, 'w+')
	populationGenotypeFileNameSuffixElements = populationGenotypeFileNameSuffix.split(".")
	fileTypeLength = len(populationGenotypeFileNameSuffixElements[-1])

	for line in chromListFile:
		# Iterate through the chromosomes and write a line in the script for each for each population
		chrom = line.strip()
		inputFileName = populationGenotypeFileNamePrefix + "_" + chrom + "_" + populationGenotypeFileNameSuffix
		outputFileName = populationGenotypeFileNamePrefix + "_" + chrom + "_" + populationGenotypeFileNameSuffix[0:len(populationGenotypeFileNameSuffix) - fileTypeLength] + "bed"
		scriptFile.write("python " + codePath + "/" + "convertGenotypesFileToBedgzip.py " + inputFileName  + " " + str(chromCol) + " " + str(positionCol) + " " + outputFileName + "\n")

	chromListFile.close()
	scriptFile.close()


if __name__=="__main__":
	import sys
	populationGenotypeFileNamePrefix = sys.argv[1] # Should not contain _ at the end
	chromListFileName = sys.argv[2]
	populationGenotypeFileNameSuffix = sys.argv[3] # Should not contain _ at the beginning
	chromCol = int(sys.argv[4])
	positionCol = int(sys.argv[5])
	scriptFileName = sys.argv[6]
	codePath = sys.argv[7] # Should not contain / at the end

	makeConvertGenotypesFileToBedgzipScript(populationGenotypeFileNamePrefix, chromListFileName, populationGenotypeFileNameSuffix, chromCol, positionCol, scriptFileName, codePath)
