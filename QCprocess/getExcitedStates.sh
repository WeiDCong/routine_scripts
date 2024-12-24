#!/bin/bash
# Extract CD Spectrum from TD-DFT calculations by ORCA

if [[ $# -eq 1 ]]
then
	echo -e "Usage: $0 NRoots"
	exit 101
fi

if -f tddft.dat
then
    rm -f tddft.dat
fi

touch tddft.dat

nroots=$1

for outf in *.log
do
    echo "processing $outf..."

    fName=${outf/.log/}

    startMark=`grep -n 'CD SPECTRUM' $outf | awk -F ':' '{print $1}'`
    startLine=$(($startMark+5))

    endLine=$(($startLine+$nroot))

    echo $fName >> tddft.dat
    sed -n "$startLine,$endLine p" $outf | awk '{print $3,$4}' >> tddft.dat

done

