#!/bin/bash

THREAD=$1
TMPFIFO=/tmp/$$.fifo

mkfifo $TMPFIFO
exec 5<>${TMPFIFO}
rm -rf ${TMPFIFO}

for((i=1;i<=$THREAD;i++))
do
echo ;
done >&5 

for inf in *.inp
do
    
    read -u5
    {

    name=${inf%.*}
    echo "Running ORCA calculation for $inf " >> $2/$3.out
    /share/apps/orca501/orca  $inf > $2/$name.log
    
    count=`grep "ORCA TERMINATED NORMALLY" $2/$name.log | wc | awk '{print $1}'`
    if [ $count -ne 0 ]
    then
        echo "Normal ternmination for $inf" >> $2/$3.out
    else
        echo "Error termination for $inf" >> $2/$3.out
    fi

    echo "">&5
} &
done
wait

exec 5>&- 