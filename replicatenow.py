#!/usr/bin/python3
import sys, subprocess
from allphysicalinfo import getall 
from etcdgetpy import etcdget as get
from pumpkeys import pumpkeys, initpumpkeys
from time import sleep

leaderip = '0'
etcdip = '0'

allinfo = {}
phrase = ''
myclusterip = ''
pport = ''
nodeloc = ''
replitype = 'Receiver'
isitopen = 'closed'
def checkpartner(receiver, nodeip, cmd, isnew):
 global allinfo, phrase, myclusterip, pport, nodeloc, replitype, leaderip, etcdip, isitopen
 if isitopen == 'closed':
    tempcmd = nodeloc+' ls'
    count = 0
    while count < 10:
        result=subprocess.run(tempcmd.split(),stdout=subprocess.PIPE)
        if result.returncode == 0: 
            isitopen = 'open'
            break
        if count == 0:
            print('start pump')
            pumpkeys(nodeip, replitype, pport, phrase)
            print('finish pump')
        count += 1
        sleep(1)
 if isitopen == 'open':
    print(" ".join(cmd))
    result=subprocess.run(cmd,stdout=subprocess.PIPE)
 return isitopen , result.stdout.decode()

def replitargetget(receiver, volume, volused, snapshot):
 global allinfo, phrase, myclusterip, pport, nodeloc, replitype, leaderip, etcdip
 partnerinfo = get(etcdip, 'Partner/'+receiver)[0].split('/')
 replitype = partnerinfo[1]
 pport = partnerinfo[2]
 phrase = partnerinfo[-1]
 print(replitype, pport, phrase, leaderip )
 nodesinfo = get(etcdip, 'Partnernode/'+receiver,'--prefix')
 print('hi',nodesinfo)
 isopen = 'closed'
 nodesinfo.append(('hi/hi/'+partnerinfo[0],'hi'))
 for node in nodesinfo:
  nodeip = node[0].split('/')[2]
  nodeloc = 'ssh -oBatchmode=yes -i /TopStordata/'+nodeip+'_keys/'+nodeip+' -p '+pport+' -oStrictHostKeyChecking=no '+nodeip 
  print('################################################333')
  print(nodeloc)
  print('################################################333')
  repliselection = nodeloc+' /TopStor/repliSelection.py '+volume+' '+volused+' '+snapshot
  print('start checkpartner')
  isopen, response = checkpartner(receiver, nodeip, repliselection.split(), 'old')
  print('finish checkpartner')
  print('>>>>>>>>>>>>>>>>>>>>',isopen)
  if 'open' in isopen:
   break
 response = response.split('result_')[1]
 return nodeip, 'closed' if 'open' not in isopen else response

def replistream(receiver, nodeip, snapshot, nodeowner, poolvol, pool, volume, csnaps):
 global allinfo, phrase, myclusterip, pport, nodeloc, replitype, leaderip, etcdip
 myvol = pool+'/'+volume 
 mysnaps = sorted(allinfo['volumes'][volume]['snapshots'], key= lambda x : x.split('.')[-1], reverse=True)
 oldsnap = 'noold'
 for snap in mysnaps:
  if snap in csnaps:
   oldsnap = snap
   break
 volumeline = get(etcdip, 'volume', volume)[0]
 volumeinfo = volumeline[1].split('/') 
 volip = volumeinfo[7]
 volsubnet = volumeinfo[8]
 volgrps = volumeinfo[4]
 voltype = volumeline[0].split('/')[1]
 cmd = '/usr/sbin/zfs get quota '+myvol+' -H'
 quota=subprocess.run(cmd.split(' '),stdout=subprocess.PIPE).stdout.decode().split('\t')[2]
 extras = ''
 cmd = nodeloc + ' /TopStor/targetcreatevol.sh '+poolvol+' '+volip+' '+volsubnet+' '+quota+' '+voltype+' '+volgrps+' '+oldsnap+' '+extras
 isopen, response = checkpartner(receiver, nodeip, cmd.split(), 'old')
 response = response.split('result_')
 if oldsnap == 'noold':
  response[1] = 'newvol/@new'
 if 'problem/@problem' in response[1]:
  print(' a problem creating/using the volume in the remote cluster')
  return
 elif 'newvol/@new' in response[1]:
  #print('./sendzfs.sh new '+ myvol+'@'+snapshot +' '+ poolvol +' '+ nodeloc.replace(' ','%%'))
  cmd = './sendzfs.sh new '+ myvol+'@'+snapshot +' '+ poolvol +' '+ nodeloc.replace(' ','%%')
 else:
  #cmd = './sendzfs.sh old '+myvol+'@'+lastsnap+' '+myvol+'@'+snapshot+' '+poolvol+' '+nodeloc
  cmd = './sendzfs.sh old '+myvol+'@'+oldsnap+' '+myvol+'@'+snapshot+' '+response[2]+' '+nodeloc.replace(' ','%%')
  print('./sendzfs.sh old '+myvol+'@'+oldsnap+' '+myvol+'@'+snapshot+' '+response[2]+' '+nodeloc.replace(' ','%%'))
 stream = subprocess.run(cmd.split(' '),stdout=subprocess.PIPE).stdout.decode()
 print('streaming: ',stream)
 print('start checking csnaps')
 csnaps = csnaps.split(',')
 cmd = '/usr/sbin/zfs list -t snapshot -o name'
 mysnaps=subprocess.run(cmd.split(' '),stdout=subprocess.PIPE).stdout.decode()
 destroy = ''
 for snap in csnaps:
  if snap == 'csnaps':
   continue
  if snap not in mysnaps:
   destroy = destroy + poolvol+'@'+snap+',' 
 if len(destroy) > 5:
  cmd = nodeloc + ' /TopStor/zfsdestroy.sh '+destroy[:-1]
  with open('/root/destroynow','w') as f:
    f.write(cmd+'\n')
  checkpartner(receiver, nodeip, cmd.split(), 'old')
 
 cmd = '/usr/sbin/zfs list -t snapshot -o name'
 _ , snaps = checkpartner(receiver, nodeip, cmd.split(), 'old')
 print('end checking csnaps')
 if snapshot in str(snaps):
    return 'success' 
 else:
    return 'fail'
 return stream

def repliparam(snapshot, receiver):
 global allinfo, phrase, myclusterip, pport, nodeloc, replitype, leaderip, etcdip
 alldsks = get(etcdip, 'host','current')
 allinfo = getall(leaderip, alldsks)
 volume = snapshot.split('/')[1].split('@')[0]
 pool = snapshot.split('/')[0]
 snapshot = snapshot.split('@')[1].replace(' ','')
 volused = str(allinfo['volumes'][volume]['referenced'])
 snapused = '0' 
 nodeip, selection = replitargetget(receiver, volume, volused, snapshot)
 if selection == 'closed':
  print('no node is open for replication in the '+receiver)
  return 'closed'
 if 'No_vol_space' in str(selection):
  print('No space in the receiver: '+receiver)
  return 'No_Sppue'
 print('selection',selection)
 nodeowner = selection.split(':')[0]
 poolvol = selection.split(':')[1].split('@')[0]
 try:
  csnaps = selection.split('@')[1]
 except:
  csnaps = 'noold'
 result = replistream(receiver, nodeip, snapshot, nodeowner, poolvol, pool, volume, csnaps)
 if 'fail' in result:
  cmd = '/usr/sbin/zfs destroy -r '+' '+pool+'/'+volume+'@'+snapshot 
 else:
  cmd = nodeloc+'  /TopStor/setsnapsender.py '+snapshot+' '+leaderip
  subprocess.run(cmd.split(' '),stdout=subprocess.PIPE).stdout.decode()
  cmd = '/usr/sbin/zfs set partner:receiver='+receiver.split('_')[0]+' '+pool+'/'+volume+'@'+snapshot
 subprocess.run(cmd.split(' '),stdout=subprocess.PIPE).stdout.decode()
 #return _'+volume, volused, snapshot+'result_'
 return result



if __name__=='__main__':
 leaderip =  sys.argv[1]
 etcdip =  sys.argv[2]
 initpumpkeys('init')
 result = repliparam(*sys.argv[3:])
