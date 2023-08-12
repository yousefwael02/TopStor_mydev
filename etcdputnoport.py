#!/usr/bin/python3
import subprocess,sys, os
import json
from time import sleep

def etcdctl(pport, key,prefix):
 cmdline=['/usr/local/bin/etcdctl','--user=root:YN-Password_123','--endpoints=http://127.0.0.1:'+pport,'put',key,prefix]
 cmdline=['/usr/local/bin/etcdctl','--endpoints=http://127.0.0.1:'+pport,'put',key,prefix]
 try:
    result=subprocess.run(cmdline,stdout=subprocess.PIPE, timeout=2)
    return result 
 except:
    print('not reachable')
    return




def etcdput(pport, key,val):
 os.environ['ETCDCTL_API']= '3'
 etcdctl(pport, key,val)
 return 1 


if __name__=='__main__':
 etcdput(*sys.argv[1:])
