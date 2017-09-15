outputmaskedfasta <-
function(sequence,name="",outputloc=getwd(),nameEntry="", numchr=22) { # sequence should not be the list but should be the masked element in the list (for example, $Hsapiensmasked)
# ADDED numchr OPTION
setwd(outputloc)
#numchr = 22
for(i in 1:numchr) {
    hold = sequence[[i]] # Pulls out a single chromosome
    namehold = names(sequence)[i] # Stores chromosome name
    hold2 = DNAStringSet(hold) # Declares as stringset object for below function
    names(hold2) = namehold # Reassigns chromosome name
    writeXStringSet(hold2, file=paste(name,"chr",i,".fasta",sep=""), format="fasta", width=80) # Writes FASTA file for each chromosome; REPLACED write.XStringSet with writeXStringSet
}
}
