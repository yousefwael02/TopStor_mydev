#!/usr/bin/python3
import subprocess
from allphysicalinfo import getall 
from etcdget import etcdget as get
from levelthis import levelthis
from copy import deepcopy 

def selectnewmirror(fdisk, diskdict, fmirror):
 global leader, leaderip, clusterip, myhost, myhostip
 single = newraids(diskdict)['single']
 fmdisks = [x for x in fmirror['disks'] if x != fdisk]
 size = float('inf')
 fmhosts = set()
 for disk in fmdisks:
  size = min(diskdict[disk]['size'],size)
  fmhosts.add(diskdict[disk]['host'])
 group = len(fmdisks) + 1
 mirror = dict() 
 possizes = [x for x in single if float(x) >= float(size)]
 possizes.sort(reverse=True)
 hostdisks = dict()
 hosts = set()
 for syz in possizes:
  for dsk in single[syz]:
   if dsk == fdisk or dsk in fmdisks:
    continue
   if diskdict[dsk]['host'] not in hostdisks:
    hostdisks[diskdict[dsk]['host']] = []
   hostdisks[diskdict[dsk]['host']].append(dsk)
   hosts.add(diskdict[dsk]['host'])
 pool = fmirror['pool']
 balance = get(leaderip, 'balance', pool)[0][1]
 hostdiskcopy = deepcopy(hostdisks)
 hosts = list(hosts)
 finishedhosts = set() 
 posdisks = []
 if 'Availability' in balance:
  notdone = 1 
  hostcount = len(hosts)
  while notdone:
   chost = hosts[(notdone-1) % hostcount] 
   if len(hostdiskcopy[chost]):
    cdisk = hostdiskcopy[chost].pop(); 
    notdone += 1
    if chost not in fmhosts:
     posdisks.append[cdisk]
   else:
    finishedhosts.add(chost)
   if len(finishedhosts) == hostcount: 
    notdone = 0
 if not len(posdisks) or 'Availability' not in balance:
  hostdiskcopy = deepcopy(hostdisks)
  notdone = 1 
  while notdone:
   chost = hosts[(notdone-1) % hostcount] 
   if len(hostdiskcopy[chost]):
    cdisk = hostdiskcopy[chost].pop(); 
    notdone += 1
    posdisks.append(cdisk)
   else:
    finishedhosts.add(chost)
   if len(finishedhosts) == hostcount: 
    notdone = 0

 if not len(posdisks):
  posdisks = 'Nodisk'
 return posdisks 


def getmirror(single,group,diskdict):
 global leader, leaderip, clusterip, myhost, myhostip
 mirror = dict() 
 for size in single:
  otherslist = [] 
  hosts = set()
  othershosts = set()
  posdiskc = 0
  for others in single:
   if others > size:
    posdiskc += len(single[others])
    otherslist.append(others)
    for dsk in single[others]:
     othershosts.add(diskdict[dsk]['host'])
  sizec = len(single[size])
  for dsk in single[size]:
   hosts.add(diskdict[dsk]['host'])
  if sizec > 0 and (posdiskc+sizec) >= group:
   mirror[size] = {'disk':size, 'diskcount':group, 'others':otherslist, 'hosts': list(hosts), 'othershosts': list(othershosts)} 
 return mirror

def getraid(single,group,parity,diskdict):
 global leader, leaderip, clusterip, myhost, myhostip
 theraid = dict()
 for size in single:
  otherslist = [] 
  hosts = set()
  othershosts = set()
  posdiskc = 0
  for others in single:
   if others > size:
    posdiskc += len(single[others])
    otherslist.append(others)
    for dsk in single[others]:
     othershosts.add(diskdict[dsk]['host'])
  dif = posdiskc + len(single[size]) - group
  for dsk in single[size]:
   hosts.add(diskdict[dsk]['host'])
  base = round(size*(group - parity ),2)
  count = 0 
  while dif >= 0:
   theraid[base] = {'disk':size, 'diskcount':group+count, 'others':otherslist, 'hosts': list(hosts), 'othershosts': list(othershosts)} 
   base += size
   dif -= 1 
   count += 1
 return theraid

allraids ={'raid5':{'parity':1, 'group':3 } , 'raid6':{ 'parity':2, 'group':4}, 'volset':{ 'parity':0, 'group':1},
           'raid6plus':{'parity':3, 'group':5} }

def newraids(diskdict):
 global leader, leaderip, clusterip, myhost, myhostip
 allsizes = dict() 
 single = dict() 
 #allsizes['single'] = single
 for disk in diskdict:
  if 'free' in diskdict[disk]['raid']:
   if diskdict[disk]['size'] not in single:
    single[diskdict[disk]['size']] = []
   single[diskdict[disk]['size']].append(disk)
 for raid in allraids:
  theraid = getraid(single,allraids[raid]['group'],allraids[raid]['parity'],diskdict) 
  if len(theraid) > 0:
   allsizes[raid] = theraid.copy()
 theraid = getmirror(single,2,diskdict)
 if len(theraid) > 0:
  allsizes['mirror'] = theraid
 if len(single) > 0:
  allsizes['single'] = single
 return allsizes

def selectdisks(disks,singles, disksinfo):
 global leader, leaderip, clusterip, myhost, myhostip
 #print('#########disks',disks)
 #print('#########singles',singles)
 with open('/TopStordata/selecteddisks','w') as f:
    f.write(str(disks)+'\n')
    f.write(str(singles)+'\n')
    f.write(str(disksinfo)+'\n')
 thedisks = []
 others = disks['others']
 others.sort(reverse=True)
 diskgroups = others 
 diskgroups.append(disks['disk'] )
 diskcount = disks['diskcount']
 #print('---------diskcount',diskcount)
 while diskcount > 0:
  nextgroup = diskgroups.pop()
  hostdisks = dict()
  hosts = set()
  disks = singles[nextgroup] 
  #print('------------diskcount2,',diskcount)
  for dsk in disks:
   hosts.add(disksinfo[dsk]['host'])
   if disksinfo[dsk]['host'] not in hostdisks:
    hostdisks[disksinfo[dsk]['host']] = []
   hostdisks[disksinfo[dsk]['host']].append(dsk)
  #print('-----------hostdisks',hostdisks)
  diskc = min(diskcount, len(disks))
  hosts = list(hosts)
  hostcount = len(hosts)
  while diskc > 0:
   host = hosts[ diskc % hostcount ] 
   if len(hostdisks[host]) > 0:
    thedisks.append(hostdisks[host].pop()) 
    diskc -= 1
   else:
    hostcount -= 1
  diskcount -= len(disks)
 print('thedisks\n',thedisks)
 return thedisks

def initgetraids(*args):
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

if __name__=='__main__':
 initgetraids('init') 
 alldsks = get(leaderip, 'host','current')
 allinfo = getall(leaderip, alldsks)
 disks = allinfo['disks']
 raids = newraids(disks)
 disks= {'disk': 10.7, 'diskcount': 2, 'others': [64.4], 'hosts': ['dhcp876810'], 'othershosts': ['dhcp876810']}
 singles= {10.7: ['scsi-360014056e9df2c855f747d88a417d92a', 'scsi-360014054a72da87a9a3458e8d0cf54e0'], 64.4: ['scsi-36001405c2feda3f507e4daca90a34057', 'scsi-36001405f69f9b869aab47579f0044b23']}
 disksinfo={'scsi-3600140514d327de4f834e60bf133d261': {'name': 'scsi-3600140514d327de4f834e60bf133d261', 'actualdisk': 'sde', 'changeop': 'ONLINE', 'pool': 'pdhcp728726367', 'raid': 'mirror-0_pdhcp728726367', 'status': 'ONLINE', 'id': '0', 'host': 'dhcp273302', 'size': 64.4, 'devname': 'sde', 'silvering': 'no'}, 'scsi-36001405adfe5f94e2064dbf8bcc8bc9b': {'name': 'scsi-36001405adfe5f94e2064dbf8bcc8bc9b', 'actualdisk': 'sdd', 'changeop': 'ONLINE', 'pool': 'pdhcp728726367', 'raid': 'mirror-0_pdhcp728726367', 'status': 'ONLINE', 'id': '0', 'host': 'dhcp273302', 'size': 64.4, 'devname': 'sdd', 'silvering': 'no'}, 'scsi-360014056e9df2c855f747d88a417d92a': {'name': 'scsi-360014056e9df2c855f747d88a417d92a', 'actualdisk': 'scsi-360014056e9df2c855f747d88a417d92a', 'changeop': 'free', 'status': 'free', 'raid': 'free', 'pool': 'pree', 'id': '2', 'host': 'dhcp876810', 'size': 10.7, 'devname': 'sdh', 'silvering': 'no'}, 'scsi-360014054a72da87a9a3458e8d0cf54e0': {'name': 'scsi-360014054a72da87a9a3458e8d0cf54e0', 'actualdisk': 'scsi-360014054a72da87a9a3458e8d0cf54e0', 'changeop': 'free', 'status': 'free', 'raid': 'free', 'pool': 'pree', 'id': '3', 'host': 'dhcp876810', 'size': 10.7, 'devname': 'sdi', 'silvering': 'no'}, 'scsi-36001405c2feda3f507e4daca90a34057': {'name': 'scsi-36001405c2feda3f507e4daca90a34057', 'actualdisk': 'scsi-36001405c2feda3f507e4daca90a34057', 'changeop': 'free', 'status': 'free', 'raid': 'free', 'pool': 'pree', 'id': '4', 'host': 'dhcp876810', 'size': 64.4, 'devname': 'sdj', 'silvering': 'no'}, 'scsi-36001405f69f9b869aab47579f0044b23': {'name': 'scsi-36001405f69f9b869aab47579f0044b23', 'actualdisk': 'scsi-36001405f69f9b869aab47579f0044b23', 'changeop': 'free', 'status': 'free', 'raid': 'free', 'pool': 'pree', 'id': '5', 'host': 'dhcp876810', 'size': 64.4, 'devname': 'sdk', 'silvering': 'no'}}
 selectdisks(disks,singles, disksinfo)
