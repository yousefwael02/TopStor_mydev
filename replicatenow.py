#!/usr/bin/python3
import sys, subprocess, logmsg
from allphysicalinfo import getall 
from etcdgetpy import etcdget as get
from etcdput import etcdput as put 
from etcddel import etcddel as dels 
from pumpkeys import pumpkeys, initpumpkeys
from time import sleep


allinfo = {}
phrase = ''
myclusterip = ''
pport = ''
nodeloc = ''
replitype = 'Receiver'
isitopen = 'closed'
def checkpartner(nodeloccmd):
 global allinfo, phrase, myclusterip, pport, nodeloc, replitype, leaderip, etcdip, isitopen
 isitopen == 'closed'
 count = 0
 print('sending to the cluster', nodeloccmd)
 try:
    result=subprocess.run(nodeloccmd.split(),stdout=subprocess.PIPE)
    if result.returncode == 0: 
        isitopen = 'open'
        resultdecod = result.stdout.decode()
 except:
    resultdecod = 0
 return isitopen , resultdecod

def createnodeloc(receiver, cmd):
 global allinfo, phrase, myclusterip, pport, nodeloc, replitype, leaderip, etcdip
 partnerinfo = get(etcdip, 'Partner/'+receiver)[0].split('/')
 remoteCluster = partnerinfo[0]
 replitype = partnerinfo[1]
 pport = partnerinfo[2]
 phrase = partnerinfo[-1]
 print(partnerinfo)
 print(replitype, pport, phrase, leaderip )
 nodesinfo = get(etcdip, 'repliPartner/'+receiver,'--prefix')
 isopen = 'closed'
 print('hi',nodesinfo)
 nodesinfo.append(('hi/hi/'+partnerinfo[0],'hi')) 
 isopen = 'close'
 for node in nodesinfo:
  print(node)
  nodeip = node[0].split('/')[2]
  if nodeip == remoteCluster :
    pumpkeys(nodeip, replitype, pport, phrase)
  nodeloc = 'ssh -oBatchmode=yes -i /TopStordata/'+nodeip+'_keys/'+nodeip+' -p '+pport+' -oStrictHostKeyChecking=no ' + nodeip 
  nodeloccmd = nodeloc+' '+ cmd
  print('################################################333')
  print(nodeip)
  print(nodeloc)
  print('################################################333')
  isopen, response = checkpartner(nodeloccmd)
  if isopen == 'open':
    break
 if isopen != 'open':
    print('result_failresult_ connection to all the nodes  cluster '+nodeip)
  
 if nodeip == remoteCluster and isopen == 'open' :
    nodeloccmd = nodeloc +' '+ '/TopStor/nodeinfo.sh' 
    print('################################################333')
    print(nodeip)
    print(nodeloccmd)
    print('################################################333')
    isopen, response = checkpartner(nodeloccmd)
    print('response',response)
    if isopen != 'open':
        print('result_failresult_ connection to remote node '+nodeip)
    else:
        print('################################################333')
        print(response)
        print('################################################333')
        partnerinfo = response.split('_')
        pumpkeys(nodeip, replitype, pport, phrase)
        put(etcdip,'repliPartner/'+receiver+'/'+partnerinfo[3], partnerinfo[2])

 if nodeip == remoteCluster and isopen != 'open' :
   print('result_failresult_ connection to all the nodes in the remote cluster '+nodeip)
    
 exit()
 return nodeip, nodeloc

def replitargetget(receiver, volume, volused, snapshot):
 global allinfo, phrase, myclusterip, pport, nodeloc, replitype, leaderip, etcdip
 partnerinfo = get(etcdip, 'Partner/'+receiver)[0].split('/')
 replitype = partnerinfo[1]
 pport = partnerinfo[2]
 phrase = partnerinfo[-1]
 print(replitype, pport, phrase, leaderip )
 nodesinfo = get(etcdip, 'cPartnernode/'+receiver,'--prefix')
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
  try:
   isopen, response = checkpartner(receiver, nodeip, repliselection.split(), 'old')
  except:
   print('result_failresult_ connection to the remote parnter')
   exit()
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
 volgrps = volumeinfo[4]
 voltype = volumeline[0].split('/')[1]
 if voltype in 'NFS':
    cmd = '/usr/sbin/zfs get quota '+myvol+' -H'
    volip = volumeinfo[9]
    volsubnet = volumeinfo[10]
    volgrps = volumeinfo[8]
    extras = ''
 elif voltype in 'ISCSI':
    cmd = '/usr/sbin/zfs get volsize '+myvol+' -H'
    volip = volumeinfo[2]
    volsubnet = volumeinfo[3]
    extras = volumeinfo[5]
 else:
    cmd = '/usr/sbin/zfs get quota '+myvol+' -H'
    volip = volumeinfo[7]
    volsubnet = volumeinfo[8]
    extras = ''

 quota=subprocess.run(cmd.split(' '),stdout=subprocess.PIPE).stdout.decode().split('\t')[2]
 oldsnap = 'noold'
 cmd = nodeloc + ' /TopStor/getlatestsnap.sh '+volume
 try:
  isopen, result = checkpartner(receiver, nodeip, cmd.split(), 'old')
 except:
   print('result_failresult_ connection to the remote parnter')
   exit()

 remotesnap = result.split('result_')
 if remotesnap != 'noold':
  cmd = 'zfs list -t snapshot'
  mysnaps = subprocess.run(cmd.split(' '),stdout=subprocess.PIPE).stdout.decode()
  if remotesnap[1] in mysnaps:
   oldsnap = remotesnap[2] 
 cmd = nodeloc + ' /TopStor/targetcreatevol.sh '+poolvol+' '+volip+' '+volsubnet+' '+quota+' '+voltype+' '+' '+oldsnap+' '+volgrps+' '+extras
 try:
  isopen, result = checkpartner(receiver, nodeip, cmd.split(), 'old')
 except:
   print('result_failresult_ connection to the remote parnter')
   exit()

 response = result.split('result_')
 print('the response of create:',response)
 if oldsnap == 'noold':
  response[1] = 'newvol/@new'
 if 'problem/@problem' in response[1]:
  print(' a problem creating/using the volume in the remote cluster')
  return
 elif 'newvol/@new' in response[1]:
  remvol = result.split('volume_')[1]
  print('/TopStor/sendzfs.sh new '+ myvol+'@'+snapshot +' '+ remvol +' '+ nodeloc.replace(' ','%%'))
  cmd = '/TopStor/sendzfs.sh new '+ myvol+'@'+snapshot +' '+ remvol +' '+ nodeloc.replace(' ','%%')
 else:
  #cmd = './sendzfs.sh old '+myvol+'@'+lastsnap+' '+myvol+'@'+snapshot+' '+poolvol+' '+nodeloc
  remvol = result.split('volume_')[1]
  myoldsnap = oldsnap.split('@')[1]
  cmd = '/TopStor/sendzfs.sh old '+myvol+'@'+myoldsnap+' '+myvol+'@'+snapshot+' '+remvol +' '+nodeloc.replace(' ','%%')
  print('/TopStor/sendzfs.sh old '+myvol+'@'+myoldsnap+' '+myvol+'@'+snapshot+' '+remvol +' '+nodeloc.replace(' ','%%'))
 put(leaderip,'running/'+receiver, 'running')
 stream = subprocess.run(cmd.split(' '),stdout=subprocess.PIPE).stdout.decode()
 dels(leaderip,'running/'+receiver)
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
  try:
   checkpartner(receiver, nodeip, cmd.split(), 'old')
  except:
   print('result_failresult_ connection to the remote parnter')
   exit()

 
 cmd = '/usr/sbin/zfs list -t snapshot -o name'
 _ , snaps = checkpartner(receiver, nodeip, cmd.split(), 'old')
 print('end checking csnaps')
 if snapshot in str(snaps):
    print('success')
    return 'success' 
 else:
    print('fail')
    return 'fail'
 return stream

def repliparam(snapshot, receiver, userreq='system'):
 global allinfo, phrase, myclusterip, pport, nodeloc, replitype, leaderip, etcdip
 if snapshot == 'sync':
  syncpush(receiver, userreq)
  return
 alldsks = get(leaderip, 'host','current')
 allinfo = getall(leaderip, alldsks)
 volume = snapshot.split('/')[1].split('@')[0]
 pool = snapshot.split('/')[0]
 snapshot = snapshot.split('@')[1].replace(' ','')
 volused = str(allinfo['volumes'][volume]['referenced'])
 snapused = '0' 
 nodeip, selection = replitargetget(receiver, volume, volused, snapshot)
 if selection == 'closed':
  print('(fail) no node is open for replication in the '+receiver)
  return 'closed'
 if 'No_vol_space' in str(selection):
  print('(fail) No space in the receiver: '+receiver)
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
  print('fail')
  cmd = '/usr/sbin/zfs destroy -r '+' '+pool+'/'+volume+'@'+snapshot 
 else:
  print('success ',result)
  cmd = nodeloc+'  /TopStor/setsnapsender.py '+snapshot+' '+leaderip
  subprocess.run(cmd.split(' '),stdout=subprocess.PIPE).stdout.decode()
  cmd = '/usr/sbin/zfs set partner:receiver='+receiver.split('_')[0]+' '+pool+'/'+volume+'@'+snapshot
 subprocess.run(cmd.split(' '),stdout=subprocess.PIPE).stdout.decode()
 #return _'+volume, volused, snapshot+'result_'
 return result
def getusershash():
 global allinfo, phrase, myclusterip, pport, nodeloc, replitype, leaderip, etcdip
 usershash = get(leaderip, 'usershash','--prefix')
 usershash = [ x for x in usershash if 'admin' not in x[0] ]
 return usershash

def getusersinfo():
 global allinfo, phrase, myclusterip, pport, nodeloc, replitype, leaderip, etcdip
 usersinfo = get(leaderip, 'usersinfo','--prefix')
 usersinfo = [ x for x in usersinfo if 'admin' not in x[0] ]
 return usersinfo

def getgroups():
 global allinfo, phrase, myclusterip, pport, nodeloc, replitype, leaderip, etcdip
 groups = get(leaderip, 'usersigroup','--prefix')
 groups = [ x for x in groups if 'admin' not in x[0] ]
 return groups 

def packagekeys(key,exception):
 global allinfo, phrase, myclusterip, pport, nodeloc, replitype, leaderip, etcdip
 keylist = get(leaderip, key, '--prefix')
 keylist = [ x for x in keylist if  exception not in x[0] ]
 print(keylist)
 stringlist = []
 for key in keylist:
  stringlist.append('tuple%'.join(key))
 print('stringlist', stringlist)
 keystring = 'list%'.join(stringlist)
 print(keystring)
 return keystring 

def syncpush(receiver, userreq):
 global allinfo, phrase, myclusterip, pport, nodeloc, replitype, leaderip, etcdip
 logmsg.sendlog('Partnerst01','info',userreq, receiver.split('_')[0])
 usershash = getusershash()
 usersinfo = getusersinfo()
 groups = getgroups()
 usershash = packagekeys('usershash','admin')
 usersinfo = packagekeys('usersinfo','admin')
 groups = packagekeys('usersigroup','admin')
 cmd = nodeloc + ' /TopStor/replisyncpull.py '+usershash+' '+usersinfo+' '+groups
 cmd = '/TopStor/replisyncpull.py '+usershash+' '+usersinfo+' '+groups
 nodeip, nodeloc, response = createnodeloc(receiver, cmd)
 print('nodeloc',nodeloc)
 try:
   isopen, response = checkpartner(receiver, nodeip, cmd.split(), 'old')
   print(response)
 except:
   print('result_failresult_ connection to the remote parnter')
   logmsg.sendlog('Partnerfa01','error',userreq, receiver.split('_')[0])
   exit()
 if 'Successfull_sync' in response:
    logmsg.sendlog('Partnersu01','info',userreq, receiver.split('_')[0])
 else:
    logmsg.sendlog('Partnerfa01','error',userreq, receiver.split('_')[0])


def repliinit(ldrip,etip):
 global leaderip, etcdip
 leaderip = ldrip
 etcdip = etip

if __name__=='__main__':
 leaderip =  sys.argv[1]
 etcdip =  sys.argv[2]
 initpumpkeys('init')
 cmdline='docker exec etcdclient /TopStor/etcdgetlocal.py clusternode'
 myhost=subprocess.run(cmdline.split(),stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n','').replace(' ','')
 logmsg.initlog(leaderip, myhost)
 with open('/root/replicatenowpy','w') as f:
    f.write(' '.join(sys.argv[1:]))
 repliparam(*sys.argv[3:])
