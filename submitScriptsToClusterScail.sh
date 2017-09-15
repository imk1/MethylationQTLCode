#!/bin/sh

Filename='/afs/cs.stanford.edu/u/imk1/scr2/MethylationQTLProject/src/correlateSNPsMethylationCpG0005RandInMoenMore2001To2500ScailScript1.sh'
Ouptprefix='/afs/cs.stanford.edu/u/imk1/scr2/MethylationQTLProject/src/correlateSNPsMethylationCpG0005RandInMoenMore2001To2500Scail'
Name='correlateSNPsMethylationCpG0005RandInMoenMore2001To2500Scail'
Count=0

while read line;
do
        ((Count=Count+1));
        Outfilename=$Ouptprefix$Count".sh";
        echo -e "$line" > $Outfilename;
        command1="qsub -l mem=1G -w e -N $Name$Count -V -o ";
        command2="$Ouptprefix$Count.o -e ";
        command3="$Ouptprefix$Count.e ";
        command4=$Outfilename;
        num_jobs_queued=`qstat -u imk1 | grep ' Q ' | wc -l`;
        while [ $num_jobs_queued -ge 50 ]; # Limits to 50 jobs in queue
        do
                sleep 100
                num_jobs_queued=`qstat -u imk1 | grep ' Q ' | wc -l`;
        done
        $command1$command2$command3$command4;
        sleep .2;
done < $Filename
