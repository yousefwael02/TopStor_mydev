#!/usr/bin/python3
import sys
from etcdgetpy import etcdget as get
from etcdgetlocalpy import etcdget as getlocal
from etcdput import etcdput as put
from broadcasttolocal import broadcasttolocal
from time import time as stamp
from socket import gethostname as hostname
from levelthis import levelthis
leaderip = getlocal('leaderip')[0]
myhost = getlocal('clusternode')[0]
def addtrend(vol,size,stamp):
 normsize = str(levelthis(size))
 csizes = get(leaderip, 'sizevol/'+vol)[0]
 csizes += '/'+stamp+'-'+normsize
 put(leaderip, 'sizevol/'+vol,csizes)
 put(leaderip, 'sync/sizevol/Add_'+'sizevol::'+vol+'_'+csizes.replace('/','::')+'/request/'+myhost, 'sizevol'_stamp)
 put(leaderip, 'sync/sizevol/Add_'+'sizevol::'+vol+'_'+csizes.replace('/','::')+'/request/', 'sizevol'_stamp)
# broadcasttolocal('sizevol/'+vol,csizes)
 
if __name__=='__main__':
 addtrend(*sys.argv[1:])
