def makeRunHomerScript(fastaFileName, miniFastaFileNamePrefix, organismName, outputFileDirPrefix, backgroundFileName, scriptFileName):
	# Make a script that will create a file and output directory for each fasta line run Homer's findMotifs.pl it
	count = 0
	fastaFile = open(fastaFileName)
	fastaHeader = fastaFile.readline()
	scriptFile = open(scriptFileName, 'w+')
	while fastaHeader != "":
		# Iterate through the fasta entries, make a mini file and Homer output directory for each, and make a script that will run Homer on each
		fastaSequence = fastaFile.readline()
		count = count + 1
		miniFastaFileName = miniFastaFileNamePrefix + str(count)
		miniFastaFile = open(miniFastaFileName, 'w+')
		miniFastaFile.write(fastaHeader)
		miniFastaFile.write(fastaSequence)
		miniFastaFile.close()
		outputFileDir = outputFileDirPrefix + str(count)
		os.system('mkdir ' + outputFileDir)
		scriptFile.write("findMotifs.pl " + miniFastaFileName + " "  + organismName + " " + outputFileDir + " -fasta " + backgroundFileName + "\n")
		fastaHeader = fastaFile.readline()
	fastaFile.close()
	scriptFile.close()
	
if __name__=="__main__":
	import sys
	import os
	fastaFileName = sys.argv[1]
	miniFastaFileNamePrefix = sys.argv[2]
	organismName = sys.argv[3]
	outputFileDirPrefix = sys.argv[4]
	backgroundFileName = sys.argv[5]
	scriptFileName = sys.argv[6]
	makeRunHomerScript(fastaFileName, miniFastaFileNamePrefix, organismName, outputFileDirPrefix, backgroundFileName, scriptFileName)