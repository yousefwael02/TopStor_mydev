#!/usr/bin/python3
import sys, subprocess
from sendhost import sendhost
def initpumpkeys(*args):
    global leader, leaderip, myhost, myhostip
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

    
def pumpkeys(*bargs):
 global leader, leaderip, myhost, myhostip
 print(str(bargs))
 partnerip = bargs[0]
 replitype = bargs[1]
 repliport = bargs[2]
 phrase = bargs[3]
 cmdline = '/TopStor/preparekeys.sh '+partnerip
 result = subprocess.run(cmdline.split(),stdout=subprocess.PIPE).stdout.decode('utf-8').split('\n')[0].replace(' ','_spc_')
 z=['/TopStor/receivekeys.sh',myhost,myhostip,leaderip, replitype, repliport, phrase, result]
 msg={'req': 'Exchange', 'reply':z}
 print(msg)
 sendhost(partnerip, str(msg),'recvreply',myhost)
 

if __name__=='__main__':
 initpumpkeys('init')
 pumpkeys(*sys.argv[1:])
