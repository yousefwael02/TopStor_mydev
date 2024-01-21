#!/bin/bash

# Get the current directory
leaderip=`echo $@ | awk '{print $1}'`
myhost=`hostname`
leader=`/TopStor/etcdget.py $leaderip leader`
myhostip=`/TopStor/etcdget.py $leaderip ready/$myhost`
echo $leader | grep $myhost
if [ $? -eq 0 ];
then
	etcdip=$leaderip
else
	etcdip=$myhostip
fi
current_dir='/TopStordata'
receivers=$(/TopStor/etcdget.py $leaderip Partner _Receiver)
if [[ $receivers == '_1' ]];
then
	echo --- no receivers....exiting
	exit
fi
Lremote='needed'
readyport='0'
failednode='NOfailedNode'
#looper over each receive
echo ---------looping over each receiver
for receiver in "${receivers[@]}"; do
	
	cluster=`echo $receiver | awk -F'/' '{print$2}' | awk -F"'," '{print $1}'`
	clusterip=`echo $receiver | awk -F"', '" '{print$2}' | awk -F"/" '{print $1}'`
	phrase=`echo $receiver | awk -F"/" '{print$5}' | awk -F"'" '{print $1}'`
	repliport=`echo $receiver | awk -F"/" '{print$4}'`
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
			failednode=`echo $tasks | awk -F"$cluster/" '{print $2}' | awk '{print $1}'`
			Lremote='needed'
		else
			echo It is successful so progressing to the next Receiver after checking the readies
			Lremote='continue'
		fi
	fi
	while [[ $Lremote == 'needed' ]];
	do
		kill -9 ` ps -eo pid,args |egrep 'Rremote|Lremote'  | grep $cluster | awk '{print $1}'` 2>/dev/null
		files=$(ls $current_dir/$cluster/ | egrep Rremote | grep $cluster )
		ofiles=$(ls $current_dir/$cluster/ | egrep Rremote | grep $cluster | egrep -v $failednode)
		echo files=$ofiles
		echo file$ofiles | grep $cluster >/dev/null
		if [ $? -eq 0 ];
		then
		 #getting the head of the node list fo the cluster
		 echo -------- we found files mean other nodes for this remote cluster so will set the flag to 'needed'
		        Lremote=$(ls $current_dir/$cluster/ | egrep Lremote |  egrep -v $failednode)
		        Rremote=$(ls $current_dir/$cluster/ | egrep Rremote |  egrep -v $failednode)
			$current_dir/$cluster/$Lremote & disown
			$current_dir/$cluster/$Rremote & disown
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
					continue
				else
				echo ----- test successfull then proceeding to the next receiver
					Lremote='continue'
				fi
			fi
		else
			echo file$files | grep $cluster >/dev/null
			if [ $? -ne 0 ];
			then
				echo ----------------------- No files are initialized before, need to start from scratch
 				/TopStor/etcdput.py $etcdip replinextport 2380 
				Lremote='initialize'
			else
				echo ----------- there are files but no node is up so the remote cluster is considered totally down
				Lremote='receiver is down'
			fi
		fi
	done
	echo $Lremote | egrep 'initialize' >/dev/null
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
		echo /TopStor/initreplipartner.py $leaderip $myhostip $myhost $cluster $clusterip $repliport $phrase
		/TopStor/initreplipartner.py init $leaderip $myhostip $myhost $cluster $clusterip $repliport $phrase 
	fi
	echo $Lremote | grep continue
	if [ $? -eq 0 ];
	then
		echo ------------ checking new remote ready nodes
		echo /TopStor/initreplipartner.py readyonly $cluster $clusterip $myhost $myhostip $leaderip $repliport $phrase $readyport
		/TopStor/initreplipartner.py readyonly $cluster $clusterip $myhost $myhostip $leaderip $repliport $phrase $readyport
		
	fi
done

