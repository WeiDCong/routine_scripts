#!/bin/bash

echo "Place gjfs to be modified in current dir and opted gjf in subdir 'opt'."

for k in `ls opt/*.gjf`
do
	toModiGjf=`echo $k | awk -F '/' '{print $2}'`
	echo "replacing XYZ in $toModiGjf..."
	startline=`grep -n "[0-9]\s[0-9]" $k | awk -F ":" '{print $1}'`
	endline=`sed -n '/^$/=' $k | awk '{print $3}'` # get the line number of third blank line

	newstartline=`grep -n "[0-9]\s[0-9]" $toModiGjf | awk -F ":" '{print $1}'`

	iLine=0
	oLine=0 # line count in gjf to be modified
	echo "startline: " $startline
	echo "newstartline: " $newstartline
	if [[ $startline -ne $newstartline ]];then
		oLine=$((oLine-1))
	fi

	while read line
	do
		iLine=$((iLine+1))
		oLine=$((oLine+1))
		if [[ $iLine -gt $startline ]];then
			newXYZ=`sed -n "$iLine p" $k`
			if [[ -z $newXYZ ]];then
				break
			else
				sed -i "$oLine c $newXYZ" $toModiGjf
			fi
		fi
	done < $k
done

