#!/bin/sh
name=`echo $@ | awk '{print $1}'`
latestsnap=`zfs list -t snapshot | grep $name | awk '{print $1}' | awk -F'.' '{print $NF}' | sort | tail -1`
latestsnapn=`zfs list -t snapshot | grep $name | grep -w $latestsnap | awk '{print $1}'`
echo 'hi'$latestsnapn | grep pdhcp
if [ $? -eq 0 ];
then

	echo result_${latestsnap}result_${latestsnapn}result_
else
	echo result_nooldresult_
fi
