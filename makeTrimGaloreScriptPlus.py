def makeTrimGaloreScriptPlus(fastqFileListFileName, stringency, quality, outputFilePath, scriptFileName):
	# Make a script that runs trim_galore on the fastq files in a list
	# ASSUMES THAT, IN THE FILE WITH NAME fastqFileListFileName, ALL PAIRS ARE LISTED TOGETHER, WITH THE LEFT READS FIRST
	fastqFileListFile = open(fastqFileListFileName)
	scriptFile = open(scriptFileName, 'w+')
	fastqFileList = fastqFileListFile.readlines()
	fastqFileListFile.close()
	fastqFileIndex = 0
	while fastqFileIndex < len(fastqFileList):
		# Iterate through the pairs of fastq files and make a call to TopHat for each pair
		fastqFileLeft = fastqFileList[fastqFileIndex].strip()
		fastqFileRight = fastqFileList[fastqFileIndex + 1].strip()
		fastqFileElements = fastqFileLeft.split("/")
		scriptFile.write("trim_galore --stringency " + str(stringency) + " --quality " + str(quality) + " -o " + outputFilePath + " --paired " + fastqFileLeft + " " + fastqFileRight + "\n")
		fastqFileIndex = fastqFileIndex + 2
	scriptFile.close()

if __name__=="__main__":
	import sys
	fastqFileListFileName = sys.argv[1] # Name of file with list of fastq files for trimming; pairs should be listed consecutively, with left before right
	stringency = int(sys.argv[2]) # Number of bases overlapping adapter on read end for read end to be trimmed
	quality = int(sys.argv[3]) # Minimum quality of base on read end that will be kept
	outputFilePath = sys.argv[4] # Directory where output files with trimmed reads will be written
	scriptFileName = sys.argv[5] # Name of file that will contain the script for running Trim Galore!
	makeTrimGaloreScriptPlus(fastqFileListFileName, stringency, quality, outputFilePath, scriptFileName)
