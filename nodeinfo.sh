#!/bin/bash
res=1
while [ $res -le 5 ];
do
	noden=$(docker exec etcdclient /TopStor/etcdgetlocal.py clusternode)
	res=$(echo $noden | wc -c)
	
done
res=1
while [ $res -le 5 ];
do
	nodei=$(docker exec etcdclient /TopStor/etcdgetlocal.py clusternodeip)
	res=$(echo $nodei | wc -c)
	replinextport=$(docker exec etcdclient /TopStor/etcdgetlocal.py replinextport)
done
res=1
while [ $res -le 5 ];
do
	replinextport=$(docker exec etcdclient /TopStor/etcdgetlocal.py replinextport)
	res=$(echo $replinextport | wc -c)
	
done
echo _result_${noden}_${nodei}_${replinextport}_
