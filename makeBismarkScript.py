def makeBismarkScript(fastqFileListFileName, genomeFolder, pathToBowtie2, outputFilePath, scriptFileName):
	# Make a script that runs trim_galore on the fastq files in a list
	# ASSUMES THAT, IN THE FILE WITH NAME fastqFileListFileName, ALL PAIRS ARE LISTED TOGETHER, WITH THE LEFT READS FIRST
	# ASSUMES THAT Bowtie2 WILL BE USED
	fastqFileListFile = open(fastqFileListFileName)
	scriptFile = open(scriptFileName, 'w+')
	fastqFileList = fastqFileListFile.readlines()
	fastqFileListFile.close()
	fastqFileIndex = 0
	while fastqFileIndex < len(fastqFileList):
		# Iterate through the pairs of fastq files and make a call to Bismark for each pair
		fastqFileLeft = fastqFileList[fastqFileIndex].strip()
		fastqFileRight = fastqFileList[fastqFileIndex + 1].strip()
		scriptFile.write("bismark --path_to_bowtie " + pathToBowtie2 + " --bowtie2 --gzip -o " + outputFilePath + " " + genomeFolder + " -1 " + fastqFileLeft + " -2 " + fastqFileRight + "\n")
		fastqFileIndex = fastqFileIndex + 2
	scriptFile.close()

if __name__=="__main__":
	import sys
	fastqFileListFileName = sys.argv[1]
	genomeFolder = sys.argv[2]
	pathToBowtie2 = sys.argv[3]
	outputFilePath = sys.argv[4]
	scriptFileName = sys.argv[5]
	makeBismarkScript(fastqFileListFileName, genomeFolder, pathToBowtie2, outputFilePath, scriptFileName)
