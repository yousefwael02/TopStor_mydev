#!/bin/sh
myhost=`docker exec etcdclient /TopStor/etcdgetlocal.py clusternode`
leader=`docker exec etcdclient /TopStor/etcdgetlocal.py leader`
echo $leader | grep $myhost
if [ $? -eq 0 ];
then
	$@
fi
