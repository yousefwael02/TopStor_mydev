#!/bin/bash

# Get the current directory
leaderip=`echo $@ | awk '{print $1}'`
current_dir='/TopStordata'

# List the files in the directory
files=$(ls $current_dir | egrep 'Lremote|Rremote')
tasks=`ps -ef | egrep 'Lremote|Rremote'`
# Loop through the files
for file in $files; do
	echo file=$file
	cluster=` echo $file | awk -F'_' '{print $2}'`
	ttype=`echo $file | awk -F'/' '{print $NF}' | awk -F'_' '{print $1}'`
	echo cluster $ttype $cluster
	echo tasks$tasks | grep $file  >/dev/null
	if [ $? -ne 0 ];
	then
		echo running $file
		kill -9 ` ps -eo pid,args |grep $ttype | grep $cluster | awk '{print $1}'`
		$current_dir/$file & disown
		if [ $? -ne 0 ];
		then
			echo Somthing went wrong, removing active links to this remote node
			kill -9 ` ps -eo pid,args |grep $ttype | grep $cluster | awk '{print $1}'`
		fi
	else
		cmd=`cat $current_dir/$file | grep '_REMOTE_' | awk -F'_REMOTE_' '{print $2}'`
		#cmd=`cat $current_dir/$file `
		echo cmd=$cmd
		$cmd > /dev/null
		if [ $? -ne 0 ];
		then
			#kill -9 `pgrep -f $file | awk '{print $1}'`
			echo killing $ttype  $cluster
			kill -9 ` ps -eo pid,args |grep $ttype | grep $cluster | awk '{print $1}'`
		else
			echo it is working
		fi
	fi

done

for file in $files; do
	cluster=` echo $file | awk -F'_' '{print $2}'`
	ttype=`echo $file | awk -F'/' '{print $NF}' | awk -F'_' '{print $1}'`
	node=`echo $file | awk -F"$cluster" '{print $NF}'`
	echo $node $ttype $node 
done
revports=`/TopStor/etcdget.py $leaderip replirev --prefix | awk -F',' '{print $2}' | awk -F"'" '{print $2}'`
for revport in $revports; do
	echo revport $revport
	netstat -ant | awk '{print $4}' | grep -w $revport
	if [ $? -eq 0 ];
	then
		echo $revport is open
		/TopStor/etcdgetnoport.py $leaderip $revport ready --prefix | grep 'not reachable'
		if [ $? -eq 0 ];
		then
			echo the reverse remote host is not running
			kill -9 $(lsof -t -i:$revport)
		fi
		
	else
		echo $revport is already closed
	fi
done
