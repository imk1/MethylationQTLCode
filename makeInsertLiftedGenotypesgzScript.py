def makeInsertLiftedGenotypesgzScript(populationGenotypeFileNamePrefix, chromListFileName, populationGenotypeFileNameSuffix, newAssembly, scriptFileName, codePath):
	# Make a script that will use gatk to convert Hapmap files to VCF files
	chromListFile = open(chromListFileName)
	scriptFile = open(scriptFileName, 'w+')
	populationGenotypeFileNameSuffixElements = populationGenotypeFileNameSuffix.split(".")
	fileTypeLength = len(populationGenotypeFileNameSuffixElements[-1])

	for line in chromListFile:
		# Iterate through the chromosomes and write a line in the script for each for each population
		chrom = line.strip()
		inputFileName = populationGenotypeFileNamePrefix + "_chr" + chrom + "_" + populationGenotypeFileNameSuffix
		liftedFileName = populationGenotypeFileNamePrefix + "_chr" + chrom + "_" + populationGenotypeFileNameSuffix[0:len(populationGenotypeFileNameSuffix) - fileTypeLength] + "lifted.bed"
		unmappedFileName = populationGenotypeFileNamePrefix + "_chr" + chrom + "_" + populationGenotypeFileNameSuffix[0:len(populationGenotypeFileNameSuffix) - fileTypeLength] + "unmapped.bed"
		outputFileName = populationGenotypeFileNamePrefix + "_chr" + chrom + "_" + populationGenotypeFileNameSuffix[0:len(populationGenotypeFileNameSuffix) - fileTypeLength] + "lifted.txt"
		scriptFile.write("python " + codePath + "/" + "insertLiftedGenotypesgzip.py " + inputFileName + " " + liftedFileName + " " + unmappedFileName + " " + outputFileName + " " + newAssembly + "\n")

	chromListFile.close()
	scriptFile.close()


if __name__=="__main__":
	import sys
	populationGenotypeFileNamePrefix = sys.argv[1] # Should not contain _ at the end
	chromListFileName = sys.argv[2]
	populationGenotypeFileNameSuffix = sys.argv[3] # Should not contain _ at the beginning
	newAssembly = sys.argv[4]
	scriptFileName = sys.argv[5]
	codePath = sys.argv[6] # Should not contain / at the end

	makeInsertLiftedGenotypesgzScript(populationGenotypeFileNamePrefix, chromListFileName, populationGenotypeFileNameSuffix, newAssembly, scriptFileName, codePath)
