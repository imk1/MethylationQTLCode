#!/bin/sh

Filename='/science/irene/MethylationQTLProject/src/runBismarkNewControlScript.sh'
Ouptprefix='/science/irene/MethylationQTLProject/src/runBismarkNewControl'
Name='runBismarkNewControl'
Count=0

while read line;
do
	((Count=Count+1));
	Outfilename=$Ouptprefix$Count".sh";
	echo -e "$line" > $Outfilename;
	#command1="qsub -q high_io -l nodes=1 -l mem=1G -w e -N $Name$Count -V -o ";
	command1="qsub -l nodes=1 -l mem=16G -w e -N $Name$Count -V -o ";
	#command1="qsub -l nodes=1:ppn=8 -l mem=16G -w e -N $Name$Count -V -o ";
	command2="$Ouptprefix$Count.o -e ";
	command3="$Ouptprefix$Count.e ";
	command4=$Outfilename;
	num_jobs_queued=`qstat -u imk1 | grep ' Q ' | wc -l`;
    while [ $num_jobs_queued -ge 5000 ]; # Limits to 10000 jobs in queue
     do
         sleep 100
         num_jobs_queued=`qstat -u imk1 | grep ' Q ' | wc -l`;
    done
	$command1$command2$command3$command4;
	sleep .2;
done < $Filename
