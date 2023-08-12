#!/bin/bash
leaderip=`echo $@ | awk '{print $1}'`
res=1
while [ $res -le 5 ];
do
	noden=`/TopStor/etcdget.py $leaderip clusternode`
	res=$(echo $noden | wc -c)
	
done
res=1
while [ $res -le 5 ];
do
	nodei=`/TopStor/etcdget.py $leaderip clusternodeip`
	res=$(echo $nodei | wc -c)
done
res=1
while [ $res -lt 2 ];
do
	replinextport=`/TopStor/etcdget.py $leaderip replinextport`
	res=$(echo $replinextport | wc -c)
	
done
leader=`/TopStor/etcdget.py $leaderip leader`
echo _result_${noden}_${nodei}_${replinextport}_$leader_
