#!/usr/bin/python3
from etcdput import etcdput as put
from etcdgetpy import etcdget as get 
from etcddel import etcddel as dels 
from time import time as stamp
from time import sleep


cmdline='docker exec etcdclient /TopStor/etcdgetlocal.py leaderip'
leaderip=subprocess.run(cmdline.split(),stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n','').replace(' ','')
cmdline='docker exec etcdclient /TopStor/etcdgetlocal.py mynodeip'
myhostip=subprocess.run(cmdline.split(),stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n','').replace(' ','')
stampi = str(stamp())
myactpools = get(myhostip, 'ActPool','--prefix')
activepools = get(leaderip, 'ActPool','--prefix')
for poolinfo in myactpools:
    pool = poolinfo[0].split('/')[1]
    if pool not in str(activepools)
        put(leaderip, poolinfo[0], poolinfo[1])
    if pool in str(activepools) and poolinfo[1] not in str(activepools):
        dels(myhostip, 'ActPool/'+pool)
    
