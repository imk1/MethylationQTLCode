def makeCatScript(folderNameListFileName, fileName, outputFileName, catedFileName, fileNamePrefix):
	# Iterate through folders and make a script that will concatenate all of the files with a certain name in the folders
	folderNameListFile = open(folderNameListFileName)
	outputFile = open(outputFileName, 'w+')
	outputFile.write("cat")
	for line in folderNameListFile:
		# Itereate through the file names and write them all to the folder
		outputFile.write(" " + fileNamePrefix + line.strip() + "/" + fileName)
	outputFile.write(" > " + catedFileName)
	folderNameListFile.close()
	outputFile.close()

if __name__=="__main__":
   import sys
   folderNameListFileName = sys.argv[1] 
   fileName = sys.argv[2]
   outputFileName = sys.argv[3]
   catedFileName = sys.argv[4]
   fileNamePrefix = ""
   if len(sys.argv) > 5:
	# A file name prefix has been included
	fileNamePrefix = sys.argv[5]
   makeCatScript(folderNameListFileName, fileName, outputFileName, catedFileName, fileNamePrefix)
