#!/usr/bin/python3
import sys, subprocess
from etcdput import etcdput as put
from etcdget import etcdget as get 
from etcddel import etcddel as dels
from logmsg import sendlog, initlog
from sendhost import sendhost
from privthis import privthis 
from time import time as stamp
from replicatenow import syncpush, repliinit


def dosync(leader,sync,  *args):
  global leaderip
  dels(leaderip, sync) 
  put(leaderip, *args)
  put(leaderip, args[0]+'/'+leader,args[1])
  return 

def initpartner(*args):
    global leader, leaderip, clusterip, myhost, myhostip, etcdip
    if args[0] == 'init':
        cmdline='docker exec etcdclient /TopStor/etcdgetlocal.py leader'
        leader=subprocess.run(cmdline.split(),stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n','').replace(' ','')
        cmdline='docker exec etcdclient /TopStor/etcdgetlocal.py leaderip'
        leaderip=subprocess.run(cmdline.split(),stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n','').replace(' ','')
        cmdline='docker exec etcdclient /TopStor/etcdgetlocal.py clusternode'
        myhost=subprocess.run(cmdline.split(),stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n','').replace(' ','')
        cmdline='docker exec etcdclient /TopStor/etcdgetlocal.py clusternodeip'
        myhostip=subprocess.run(cmdline.split(),stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n','').replace(' ','')
    else:
        leader = args[0]
        leaderip = args[1]
        myhost = args[2]
        myhostip = args[3]
    clusterip = leaderip 
    if myhost == leader:
        etcdip = leaderip
    else:
        etcdip = myhostip
    initlog(clusterip, myhost)

def delpartner(*bargs):
 global leader, leaderip, clusterip, myhost, myhostip, etcdip
 partner = bargs[0]
 issync = bargs[1]
 userreq = bargs[2]
 if (privthis(etcdip,'Replication',userreq) != 'true'):
  print('not authorized to add partner')
  return
 sendlog('Partner1003','info',userreq,partner)
 dels(etcdip,'Partner',partner)
 dels(etcdip,'repli',partner)
 if 'yes' in issync:
  cmdline = '/TopStor/SnapShotPeriodDelete '+leaderip+' '+partner+' '+'system'
  result = subprocess.run(cmdline.split(),stdout=subprocess.PIPE)
  stampit = str(stamp())
  dels(etcdip,'sync',partner.replace('_',':::'))
  put(leaderip, 'sync/Partnr/Del_'+partner.replace('_',':::')+':no:'+userreq+'/request','Partnr_'+stampit)
  dosync(myhost,'Partnr_', 'sync/Partnr/Del_'+partner.replace('_',':::')+':no:'+userreq+'/request','Partnr_'+stampit) 
 
 sendlog('Partner1004','info',userreq,partner)

if __name__=='__main__':
 initpartner('init')
 with open('/root/PartnerDel','w') as f:
    import json
    json.dump(sys.argv[1:], f)
 delpartner(*sys.argv[1:])
