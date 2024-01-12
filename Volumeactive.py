#!/usr/bin/python3
import sys, logmsglocal, subprocess
from privthis import privthis 
from etcdgetpy import etcdget as get
from etcdput import etcdput as put 


def getippos(vtype):
    if ('cifs' or 'home') in vtype.lower():
        return 7
    elif 'nfs' in vtype.lower():
        return 9
    else: 
        return 0

def volumeactive(leaderip, myhost, pool,volname,prot,active,userreq):
 with open('/root/volumactivepy','w') as f:
  f.write(' '.join([leaderip, myhost, pool,volname,prot,active,userreq]))
 leader = get(leaderip,'leader')[0]
 if leader != myhost:
   etcdip = get(leaderip,'ready/'+myhost)[0]
 else:
   etcdip = leaderip
 logmsglocal.initlog(leaderip, myhost,etcdip)
 if privthis(etcdip, prot,userreq) != 'true':
  print('not authorized user to do this task ')
  return
 logmsglocal.sendlog('Unmoutst01','info',userreq,volname,active)
 volinfo=get(leaderip, 'volumes',volname)[0]
 print('volinfo',volinfo,prot)
 volright = volinfo[1].split('/')
 volright[-1] = active
 ippos = getippos(prot)
 ipaddr = volright[ippos]+'/'+volright[ippos+1]
 volright = '/'.join(volright)
 volleft = volinfo[0]
 cmdline='/TopStor/Volumeactivesh.sh '+leaderip+' '+myhost+' '+pool+' '+volname+' '+prot+' '+active+' '+ipaddr+' '+userreq
 print('cmdline',cmdline)
 result = subprocess.run(cmdline.split(),stdout=subprocess.PIPE).stdout.decode('utf-8')
 put(leaderip, volleft,volright)
 logmsglocal.sendlog('Unmoutsu01','info',userreq,volname,active)
 put(etcdip, 'dirty/volume','0')
 return
 
if __name__=='__main__':
 leaderip = sys.argv[1]
 myhost = sys.argv[2]
 volumeactive(*sys.argv[1:])
