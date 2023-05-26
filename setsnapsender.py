#!/usr/bin/python3
import sys, subprocess

leaderip = '0'
def setsnapshotsender(snapshot,cip):
    cmd = 'zfs list -t snapshot'    
    result = subprocess.run(cmdline.split(),stdout=subprocess.PIPE).stdout.decode() 
    fullname = [ x.split('\t')[0] for x in result if snapshot in x ][0]
    print('fullname',fullname)
    cmdline='docker exec etcdclient /TopStor/etcdgetlocal.py leaderip'
    leaderip=subprocess.run(cmdline.split(),stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n','').replace(' ','')
    sender = get(leaderip,'Partner', cip)[0][0].split('/')[1].split('_')[0]
    print('sender', sender)
    

if __name__=='__main__':
    snapshot =  sys.argv[1]
    senderclusterip =  sys.argv[2]
    setsnapshotsender(snapshot, senderclusterip)
