def convertMartToMaskgenome(martFileName, outputFileName):
	# Convert a file from Ensembl MART with Chromosome,Position,Minor allele (ALL),Variant Alleles to maskgenome format
	martFile = open(martFileName)
	outputFile = open(outputFileName, 'w+')
	martFile.readline() # Remove the header
	for line in martFile:
		# Iterate through the lines of the MART file and convert each line to the format for maskgenome
		lineElements = line.split(",")
		if lineElements[0] == "":
			# The current line is empty, so skip it
			continue
		alleles = lineElements[3].strip().split("/")
		if len(alleles) != 2:
			# REMOVE SNPS WITH !=2 ALLELES
			continue
		minorAllele = lineElements[2]
		if minorAllele == "":
			# IF NO MINOR ALLELE IS RECORDED, SET THE SECOND ALLELE TO BE THE MINOR ALLELE
			minorAllele = alleles[1]
		majorAllele = alleles[0]
		if alleles[0] == minorAllele:
			# The second allele is the major allele
			majorAllele = alleles[1]
		outputFile.write(lineElements[0] + "\t" + lineElements[1] + "\t" + majorAllele + "\t" + minorAllele + "\n")
	martFile.close()
	outputFile.close()

if __name__=="__main__":
	import sys
	martFileName = sys.argv[1]
	outputFileName = sys.argv[2]
	convertMartToMaskgenome(martFileName, outputFileName)
