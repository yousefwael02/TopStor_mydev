#!/usr/bin/python3
import sys
from etcdgetlocalpy import etcdget as get
from time import time as stamp
from etcdputlocal import etcdput as put 
from etcdput import etcdput as putp 

dev='enp0s8'
def updatenamespace(*args):
  myhost = get('clusternode')[0] 
  leaderip=get('leaderip')[0]
  stampi = str(stamp())
  put('namespace/mgmtip',args[0])
  putp(leaderip, 'sync/namespace/mgmtip_'+args[0]+'/request/'+myhost,'namespace_'+stampi)
  putp(leaderip, 'sync/namespace/mgmtip_'+args[0]+'/request','namespace_'+stampi)
  
if __name__=='__main__':
 updatenamespace(*sys.argv[1:])
