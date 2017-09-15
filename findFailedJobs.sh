# Code written by Trevor Martin

# Finds which jobs failed and creates file to rerun them

# Must be run on Output directory that only has output files

# Will not catch if last file in sequence failed


ls ./Output/ | sed -e s/[^0-9]//g | sort -n > runnumbers.txt

awk 'p && p != $1 { for( i = p; i < $1; i++ ) print i; } {p = $1 + 1 }' runnumbers.txt > missingnumbers.txt

sed 's,^,R CMD BATCH --no-save --no-restore /oasis/projects/nsf/sua135/trevorm/TemporalQTL/tss/10000/null/carlo/Programs/tcortqtlanalysisnullclusterregressfullselectperm,' missingnumbers.txt > temp.txt

sed 's/$/.r/' temp.txt > resetjobs.txt

rm temp.txt runnumbers.txt missingnumbers.txt