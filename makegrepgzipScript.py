def makegrepgzipScript(fileNameListFileName, outputFileNameSuffix, grepPhrase, scriptFileName):
	# Iterate through folders and make a script that will concatenate all of the files with a certain name in the folders
	fileNameListFile = open(fileNameListFileName)
	scriptFile = open(scriptFileName, 'w+')
	for line in fileNameListFile:
		# Itereate through the file names and write them all to the folder
		scriptFile.write("zcat")
		scriptFile.write(" " + line.strip())
		outputFileName = line.strip()[:-2] + outputFileNameSuffix
		scriptFile.write(" | grep -P '" + grepPhrase + "' > " + outputFileName + "\n")
	fileNameListFile.close()
	scriptFile.close()

if __name__=="__main__":
   import sys
   fileNameListFileName = sys.argv[1] 
   outputFileNameSuffix = sys.argv[2] # Should not start with .
   grepPhrase = sys.argv[3]
   scriptFileName = sys.argv[4]
   makegrepgzipScript(fileNameListFileName, outputFileNameSuffix, grepPhrase, scriptFileName)
