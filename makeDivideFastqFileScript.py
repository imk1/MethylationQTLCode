def makeDivideFastqFileScript(fastqFileNameListFileName, numLinesPerOutputFile, scriptFileName, codePath):
	# Make a script that will divide each fastq file in a list
	fastqFileNameListFile = open(fastqFileNameListFileName)
	scriptFile = open(scriptFileName, 'w+')	
	for line in fastqFileNameListFile:
		# Iterate through the chromosomes and write a line in the script for each for each population
		fastqFileName = line.strip()
		scriptFile.write("python " + codePath + "/" + "divideFastqFile.py " + fastqFileName + " " + str(numLinesPerOutputFile) + "\n")
	fastqFileNameListFile.close()
	scriptFile.close()

if __name__=="__main__":
   import sys
   fastqFileNameListFileName = sys.argv[1] # Entries should end with .gz
   numLinesPerOutputFile = int(sys.argv[2]) # Using 5,000,000
   scriptFileName = sys.argv[3]
   codePath = sys.argv[4] # Should not end with /
   makeDivideFastqFileScript(fastqFileNameListFileName, numLinesPerOutputFile, scriptFileName, codePath)
