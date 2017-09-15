def makeMergeSortedPosMethylFiles(methylSortedFileNameListFileName, fileListFileNameSuffix, outputFileNameSuffix, CGDist, scriptFileName, codePath):
	# Make a script that will merge sorted methylation files
	# ASSUMES THAT EVERY 2 FILES SHOULD BE MERGED
	methylSortedFileNameListFile = open(methylSortedFileNameListFileName)
	scriptFile = open(scriptFileName, 'w+')
	methylSortedFileName = methylSortedFileNameListFile.readline().strip()
	while methylSortedFileName != "":
		# Go through the list of sorted methylation file names and make a line in the script for every 2
		methylSortedFileNameElements = methylSortedFileName.split("_")
		fileListFileName = methylSortedFileNameElements[0] + "_" + fileListFileNameSuffix
		outputFileName = methylSortedFileNameElements[0] + "_" + outputFileNameSuffix
		fileListFile = open(fileListFileName, 'w+')
		fileListFile.write(methylSortedFileName + "\n")
		fileListFile.write(methylSortedFileNameListFile.readline())
		fileListFile.close()
		scriptFile.write("python " + codePath + "/" + "mergeSortedPosMethylFiles.py " + fileListFileName + " " + outputFileName + " " + str(CGDist) + "\n")
		methylSortedFileName = methylSortedFileNameListFile.readline().strip()
	methylSortedFileNameListFile.close()
	scriptFile.close()

if __name__=="__main__":
   import sys
   import gzip
   methylSortedFileNameListFileName = sys.argv[1]
   fileListFileNameSuffix = sys.argv[2] 
   outputFileNameSuffix = sys.argv[3]
   CGDist = int(sys.argv[4]) # 1 for CpGs, 2 for CHGs, 0 for CHHs
   scriptFileName = sys.argv[5]
   codePath = sys.argv[6]
   makeMergeSortedPosMethylFiles(methylSortedFileNameListFileName, fileListFileNameSuffix, outputFileNameSuffix, CGDist, scriptFileName, codePath)