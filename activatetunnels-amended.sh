#!/bin/bash

# Get the current directory
leaderip=`echo $@ | awk '{print $1}'`
current_dir='/TopStordata'
receivers=$(/TopStor/etcdget.py $leaderip Partner _Receiver)
Lremote='needed'
failednode='NOfailedNode'
#looper over each receive
echo ---------looping over each receiver
for receiver in "${receivers[@]}"; do
	cluster=`echo $receiver | awk -F'/' '{print$2}' | awk -F"'," '{print $1}'`
	clusterip=`echo $receiver | awk -F"', '" '{print$2}' | awk -F"/" '{print $1}'`
	tasks=`ps -ef | egrep 'Rremote' | grep ssh$cluster`
	echo tt$tasks | grep $cluster >/dev/null
	if [ $? -eq 0 ];
	then
	# remote file is already loaded. we should check now if the other end works
	echo --------- remote file is already loaded. we should check now if the other end works
		readyport=`echo $tasks | awk -F":$leaderip" '{print $1}' | awk -F":" '{print $NF}'`
		testport=`/TopStor/etcdgetnoport.py $leaderip $readyport ready --prefix`
		echo $testport | grep _1 >/dev/null
		if [ $? -eq 0 ];
		then
		# test failed then we hve to kill this
			echo -------- loaded files are failing so setting the failednode and the flag is already in $Lremote
			failednode=`echo $tasks | awk -F"_keys/" '{print $2}' | awk '{print $1}'`
		else
			echo It is successful so progressing to the next Receiver
			continue
		fi
	fi
	while [[ $Lremote == 'needed' ]];
	do
		kill -9 ` ps -eo pid,args |egrep 'Rremote|Lremote'  | grep $cluster | awk '{print $1}'` 2>/dev/null
		files=$(ls $current_dir | egrep Rremote | grep $cluster | egrep -v $failednode)
		echo files=$files
		echo file$files | grep $cluster >/dev/null
		if [ $? -eq 0 ];
		then
		 #getting the head of the node list fo the cluster
		 echo -------- we found files mean other nodes for this remote cluster so will set the flag to 'needed'
		        Lremote=$(ls $current_dir | egrep Lremote | grep $cluster | egrep -v $failednode)
		        Rremote=$(ls $current_dir | egrep Rremote | grep $cluster | egrep -v $failednode)
			$current_dir/$Lremote & disown
			$current_dir/$Rremote & disown
			sleep 1
			tasks=`ps -ef | grep Rremote | grep ssh$cluster`
			readyport=`echo $tasks | awk -F":$leaderip" '{print $1}' | awk -F":" '{print $NF}'`
			testport=`/TopStor/etcdgetnoport.py $leaderip $readyport ready --prefix`
			echo testport$testport | grep _1 >/dev/null
			if [ $? -eq 0 ];
			then
			# test failed then we hve to kill this
				echo ---------  test failed then we have to kill this cluster $cluster files
				echo -------- no loaded files so setting the flag to needed
		 		failednode=$failednode'|'`echo $Rremote | awk -F"Receiver_" '{print $2}' | awk -F"_" '{print $1}'`
				echo failednode=$failednode	
				Lremote='needed'
				continue
			else
				echo testport$testport | grep _1 >/dev/null
				if [[  $testport == '' ]];
				then
					Lremote='initialize'
					continue
				fi
			fi
		else
			Lremote='initialize'
		fi
	done
	echo $Lremote | egrep 'initialize|needed' >/dev/null
	if [ $? -eq 0 ];
	then
	echo -------- the Remote flag finished and it is now in $Lremote , so initializing
		leader=`/TopStor/etcdget.py $leaderip leader`
		myhost=`hostname`
		myhostip=`/TopStor/etcdget.py $leaderip clusternodeip`
		echo $leader | grep $myhost
		if [ $? -eq 0 ];
		then
			etcdip=$leaderip
		else
			etcdip=`/TopStor/etcdget.py $leaderip clusternodeip`
		fi
		clusterip=`echo $receiver | awk -F", '" '{print$2}' | awk -F"/" '{print $1}'`
		repliport=`echo $receiver | awk -F"/" '{print$4}'`
		phrase=`echo $receiver | awk -F"/" '{print$5}' | awk -F"'" '{print $1}'`
		echo /TopStor/initreplipartner.py $leaderip $myhostip $myhost $cluster $clusterip $repliport $phrase 
		/TopStor/initreplipartner.py $leaderip $myhostip $myhost $cluster $clusterip $repliport $phrase 
	fi
done
exit
# List the files in the directory
files=$(ls $current_dir | egrep 'Lremote|Rremote')
tasks=`ps -ef | egrep 'Lremote|Rremote'`
# Loop through the files
for file in $files; do
	echo file=$file
	cluster=` echo $file | awk -F'_' '{print $2}'`
	nodeip=` echo $file | awk -F'_' '{print $4}'`
	ttype=`echo $file | awk -F'/' '{print $NF}' | awk -F'_' '{print $1}'`
	echo cluster $ttype $cluster
	echo tasks$tasks | grep $file  >/dev/null
	if [ $? -ne 0 ];
	then
		echo running $file
		kill -9 ` ps -eo pid,args |grep $ttype | grep $cluster | awk '{print $1}'` 2>/dev/null
		echo $file | grep Lremote
		if [ $? -eq 0 ];
		then
			/TopStor/pumpkeys.py pumpthis $nodeip
		fi
	fi
done
for file in $files; do
	echo file=$file
	cluster=` echo $file | awk -F'_' '{print $2}'`
	nodeip=` echo $file | awk -F'_' '{print $4}'`
	ttype=`echo $file | awk -F'/' '{print $NF}' | awk -F'_' '{print $1}'`
	echo cluster $ttype $cluster
	echo tasks$tasks | grep $file  >/dev/null
	if [ $? -ne 0 ];
	then
		echo running $file
		kill -9 ` ps -eo pid,args |grep $ttype | grep $cluster | awk '{print $1}'` 2>/dev/null
		$current_dir/$file & disown
		if [ $? -ne 0 ];
		then
			echo Somthing went wrong, removing active links to this remote node
			echo thefile=$file
			kill -9 ` ps -eo pid,args |grep $ttype | grep $cluster | awk '{print $1}'`
		fi
	else
		echo found it running
		cmd=`cat $current_dir/$file | grep '_REMOTE_' | awk -F'_REMOTE_' '{print $2}'`
		#cmd=`cat $current_dir/$file `
		#$cmd > /dev/null
		cat $current_dir/$file | grep '_REMOTE_' | awk -F'_REMOTE_' '{print $2}'
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
