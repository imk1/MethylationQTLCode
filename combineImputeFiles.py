def combineImputeFiles(imputeFileNameListFileName, outputFileName):
	# Combine the files with imputed genotypes
	imputeFileNameListFile = open(imputeFileNameListFileName)
	outputFile = open(outputFileName, 'w+')
	# Columns of output:
	# 1.  Chromosome
	# 2.  Position on chromosome
	# 3.  rsid
	# 4.  Reference allele (might not be reference)
	# 5.  Alternate allele (might not be alternate)
	for line in imputeFileNameListFile:
		# Iterate through the files with the SNPs and record each SNP in the output file
		imputeFileName = line.strip()
		imputeFile = gzip.open(imputeFileName, 'rb')
		imputeFileNameElements = imputeFileName.split("/")
		chromElements = imputeFileNameElements[-1].split(".")
		chrom = chromElements[0]
		for SNPLine in imputeFile:
			# Iterate through the SNPs and record a line for each SNP in the output file
			SNPLineElements = SNPLine.strip().split(" ")
			outputFile.write(chrom + "\t" + SNPLineElements[2] + "\t" + SNPLineElements[1] + "\t" + SNPLineElements[3] + "\t" + SNPLineElements[4] + "\n")
		imputeFile.close()
	imputeFileNameListFile.close()
	outputFile.close()

if __name__=="__main__":
	import sys
	import gzip
	imputeFileNameListFileName = sys.argv[1]
	outputFileName = sys.argv[2]
	combineImputeFiles(imputeFileNameListFileName, outputFileName)
