#!/usr/bin/python3
from etcdgetlocalpy import etcdget as get
from etcdput import etcdput as put
from etcddel import etcddel as deli
from time import time as stamp
import sys
myhost = get('clusternode')[0]
leader=get('leader')[0]
leaderip=get('leaderip')[0]
def getipstatus(ipaddr,ipsubnet,vol):
 allvols=get('ipaddr/'+ipaddr+'/'+ipsubnet)
 return allvols[0]

def clearvol(vol):
 allvols=get('ipaddr','--prefix')
 volin=[x for x in allvols if vol in x[1] and '/' not in x[1].replace('/'+vol,'')]
 for x in volin:
  deli(leaderip, x[0],x[0])
 stampi = str(stamp())
 put(leaderip, 'sync/ipaddr/request','ipaddr_'+stampi)
 put(leaderip, 'sync/ipaddr/request/'+leader,'ipaddr_'+stampi)
 if len(volin) > 0:
  print('result='+volin[0][1].replace('/'+vol,''))
  return volin[0][1].replace('/'+vol,'')
 else:
  print('result=-1')
  return '-1' 

def redvol(vol):
 allvols=get('ipaddr','--prefix')
 remvol=[(x[0],x[1].replace('/'+vol,'')) for x in allvols if vol in x[1] and '/' in x[1].replace('/'+vol,'')]
 for x in remvol:
  put(leaderip, x[0],x[1])
 stampi = str(stamp())
 put(leaderip, 'sync/ipaddr/request','ipaddr_'+stampi)
 put(leaderip, 'sync/ipaddr/request/'+leader,'ipaddr_'+stampi)
 if len(remvol) > 0:
  print('result='+remvol[0][1].split('/')[0])
  return 'result='+remvol[0][1].split('/')[0]
 else:
  print('result=-1')
  return 'result=-1' 

if __name__=='__main__':
# getipstatus(*sys.argv[1:])
 func={}
 func['getipstatus']=getipstatus
 func['clearvol']=clearvol
 func['redvol']=redvol
 func[sys.argv[1]](*sys.argv[2:])
