#!/bin/sh
noden=`docker exec etcdclient /TopStor/etcdgetlocal.py clusternode`
nodei=`docker exec etcdclient /TopStor/etcdgetlocal.py clusternodeip`
echo _result_${noden}_${nodei}
