#!/usr/bin/python3
import sys, subprocess
from etcdgetpy import etcdget as get
from etcdput import etcdput as put 


leaderip = ''
def inflatekeys(*keys):
 global leaderip
 for keystring in keys:
    stringlist = keystring.replace('list%',' ').split(' ')
    for keytuple in stringlist:
        key = keytuple.replace('tuple%',' ').split(' ')
        print(key)
        put(leaderip,'pullsync/'+key[0],key[1])
 
 print('Successfull_sync')
if __name__=='__main__':
 cmdline='docker exec etcdclient /TopStor/etcdgetlocal.py leaderip'
 leaderip=subprocess.run(cmdline.split(),stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n','').replace(' ','')
 inflatekeys(*sys.argv[1:])
