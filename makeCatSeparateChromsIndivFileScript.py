def makeCatSeparateChromsScript(fileNameListFileName, chromListFileName, outputFilePath, chromCol, scriptFileName, codePath):
	# Make a script that separtes each file into a different file for each chromosome
	# ASSUMES THAT THE CHROMOSOME IS IN THE 2ND COLUMN AND IS THE SAME FOR SNPS AND C'S
	scriptFile = open(scriptFileName, 'w+')
	fileNameListFile = open(fileNameListFileName)
	for fileName in fileNameListFile:
		# Iterate through the files and put a line to separate each file into chromosomes in the script
		scriptFile.write("python " + codePath + "/" + "catSeparateChromsIndivFile.py " + fileName.strip() + " " + chromListFileName + " " + outputFilePath + " " + str(chromCol) + " \n")
	fileNameListFile.close()
	scriptFile.close()

if __name__=="__main__":
   import sys
   import gzip
   fileNameListFileName = sys.argv[1] 
   chromListFileName = sys.argv[2]
   outputFilePath = sys.argv[3] # Should not end in /
   chromCol = int(sys.argv[4]) # 0-indexed; 1 for SNPMethyl, 2 for methylation
   scriptFileName = sys.argv[5]
   codePath = sys.argv[6] # Should not end in /
   makeCatSeparateChromsScript(fileNameListFileName, chromListFileName, outputFilePath, chromCol, scriptFileName, codePath)