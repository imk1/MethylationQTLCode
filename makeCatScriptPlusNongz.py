def makeCatScriptPlus(fileNameListFileName, outputFileName, catedFileName):
	# Iterate through folders and make a script that will concatenate all of the files with a certain name in the folders
	fileNameListFile = open(fileNameListFileName)
	outputFile = open(outputFileName, 'w+')
	outputFile.write("cat")
	for line in fileNameListFile:
		# Itereate through the file names and write them all to the folder
		outputFile.write(" " + line.strip())
	outputFile.write(" > " + catedFileName)
	fileNameListFile.close()
	outputFile.close()

if __name__=="__main__":
   import sys
   fileNameListFileName = sys.argv[1] 
   outputFileName = sys.argv[2]
   catedFileName = sys.argv[3]
   makeCatScriptPlus(fileNameListFileName, outputFileName, catedFileName)
