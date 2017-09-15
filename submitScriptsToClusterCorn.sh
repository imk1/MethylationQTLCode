#!/bin/sh

Filename='/afs/ir.stanford.edu/users/i/m/imk1/MethylationQTLProject/src/fisherExactSNPsMethylationCpG0001CornScript1.sh'
Ouptprefix='/afs/ir.stanford.edu/users/i/m/imk1/MethylationQTLProject/src/fisherExactSNPsMethylationCpG0001CornScript1'
Name='fisherExactSNPsMethylationCpG0001CornScript1'
Count=0

while read line;
do
	((Count=Count+1));
	Outfilename=$Ouptprefix$Count".sh";
	echo -e "$line" > $Outfilename;
	command1="qsub -w e -N $Name$Count -V -o ";
	command2="$Ouptprefix$Count.o -e ";
	command3="$Ouptprefix$Count.e ";
	command4=$Outfilename;
	$command1$command2$command3$command4;
	sleep .2;
done < $Filename
