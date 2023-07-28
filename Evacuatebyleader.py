#!/usr/bin/python3
import subprocess,sys, datetime
from logqueue import queuethis, initqueue
from etcdput import etcdput as put 
from time import sleep
from etcdget import etcdget as get
from etcddel import etcddel as deli 
import logmsg


def setall(*bargs):
 with open('/pacedata/perfmon','r') as f:
  perfmon = f.readline()
 if '1' in perfmon:
  queuethis('Evacuate','running','system')
 myhost = bargs[1] 
 leaderip = bargs[0] 
 initqueue(leaderip, myhost)
 logmsg.initlog(leaderip, myhost)
  
 hostn=bargs[2]
 hostip=bargs[3]
 userreq=bargs[-1]
 print('hihih',hostip, hostn)
 leader=get(leaderip, 'leader')[0]
 print('iiiiiiiiiiiiiiiii',hostn,myhost, leader, hostip)
 print('iam here', hostn, hostip)
 cmdline=['/pace/removetargetdisks.sh', hostn, hostip]
 result=subprocess.run(cmdline,stdout=subprocess.PIPE)
 nextleader = get(leaderip,'nextlead/er')[0] 
 deli(leaderip, "",hostn)
 if nextleader in hostn:
    readies = get(leaderip, 'ready','--prefix')
    for host in readies:
        if myhost not in str(host):
            nextleader = host[0].replace('ready/','')
            put(leaderip, 'nextlead/er',nextleader)
            put(leaderip, 'sync/nextlead/Add_er_'+nextleader+'/request','nextlead_'+str(stamp))
            put(leaderip, 'sync/nextlead/Add_er_'+nextleader+'/request/'+myhost,'nextlead_'+str(stamp))
            break
 logmsg.sendlog('Evacuaesu01','info',userreq ,hostn)
 if '1' in perfmon:
  queuethis('Evacuate','stop','system')
 return

if __name__=='__main__':
 setall(*sys.argv[1:])
