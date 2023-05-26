#!/usr/bin/python3
import sys, subprocess
from etcdget import etcdget as get

def setsnapshotsender(snapshot,cip):
    cmd = 'zfs list -t snapshot'    
    result = subprocess.run(cmd.split(),stdout=subprocess.PIPE).stdout.decode().split()
    print(result)
    fullname = [ x.split('\t')[0] for x in result if snapshot in x ][0]
    print('fullname',fullname)
    cmdline='docker exec etcdclient /TopStor/etcdgetlocal.py leaderip'
    leaderip=subprocess.run(cmdline.split(),stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n','').replace(' ','')
    sender = get(leaderip,'Partner', cip)[0][0].split('/')[1].split('_')[0]
    cmd = 'zfs set partner:sender='+sender+' '+fullname    
    result = subprocess.run(cmd.split(),stdout=subprocess.PIPE).stdout.decode().split()
    print('sender', sender)
    

if __name__=='__main__':
    with open('/root/setsnapsender','w') as f:
        f.write(' '.join(sys.argv[1:])+'\n')
    snapshot =  sys.argv[1]
    senderclusterip =  sys.argv[2]
    setsnapshotsender(snapshot, senderclusterip)
