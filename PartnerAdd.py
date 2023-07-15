#!/usr/bin/python3
import sys, subprocess
from etcdput import etcdput as put
from etcdget import etcdget as get 
from etcddel import etcddel as dels
from logmsg import sendlog, initlog
from sendhost import sendhost
from privthis import privthis 
from time import time as stamp



def dosync(leader,sync,  *args):
  global leaderip
  dels(leaderip, sync) 
  put(leaderip, *args)
  put(leaderip, args[0]+'/'+leader,args[1])
  return 

def initpartner(*args):
    global leader, leaderip, clusterip, myhost, myhostip
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
    initlog(clusterip, myhost)

def addpartner(*bargs):
 global leader, leaderip, clusterip, myhost, myhostip
 if myhost == leader:
    etcd = leaderip
 else:
    etcd = myhostip
 partnerip = bargs[0]
 partneralias = bargs[1].replace('_','').replace('/',':::')
 replitype = bargs[2]
 repliport = bargs[3]
 phrase = bargs[4]
 userreq = bargs[5]
 init = bargs[6]
 if (privthis(etcd,'Replication',userreq) != 'true'):
  print('not authorized to add partner')
  return
 sendlog('Partner1000','info',userreq,partneralias,replitype)
 if 'Sender' not in replitype:
  cmdline = '/TopStor/preparekeys.sh '+partnerip
  result = subprocess.run(cmdline.split(),stdout=subprocess.PIPE).stdout.decode('utf-8').split('\n')[0].replace(' ','_spc_')
  z=['/TopStor/receivekeys.sh',myhost,myhostip,clusterip, replitype, repliport, phrase, result]
  msg={'req': 'Exchange', 'reply':z}
  print(msg)
  sendhost(partnerip, str(msg),'recvreply',myhost)
  cmdline = '/TopStor/checkpartner.sh '+partneralias+' '+replitype+' '+partnerip+' '+repliport+' '+clusterip+' '+phrase+' '+'new'
  print('sending',cmdline.split())
  result = subprocess.run(cmdline.split(),stdout=subprocess.PIPE).stdout.decode('utf-8')
  if 'open' not in result:
   sendlog('Partner1fa2','error',userreq,partneralias,replitype)
   return
 if 'init' in init:
  put(leaderip, 'Partner/'+partneralias+'_'+replitype , partnerip+'/'+replitype+'/'+str(repliport)+'/'+phrase) 
  dosync(myhost,'Partnr_str_', 'sync/Partnr/Add_'+partneralias+':::'+replitype+'_'+partnerip+'::'+replitype+'::'+str(repliport)+'::'+phrase+'/request','Partnr_str_'+str(stamp())) 

 sendlog('Partner1002','info',userreq,partneralias,replitype)
 

if __name__=='__main__':
 initpartner('init')
 with open('/root/PartnerAdd','w') as f:
    import json
    json.dump(sys.argv[1:], f)
 addpartner(*sys.argv[1:])
