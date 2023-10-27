#!/bin/python
import sys, subprocess, re, zlib, json, base64
from etcdgetpy import etcdget as get 
from etcdput import etcdput as put
from etcddel import etcddel as dels 
from time import time , sleep
from collectconfig import collectConfig


readies = 0 

def postchange(ready,myhost):
 global leaderip
 cmndstring = '/TopStor/collectconfig.py '+leaderip+' '+ready 
 z= cmndstring.split(' ')
 msg={'req': 'Pumpthis', 'reply':z}
 sendhost(ready, str(msg),'recvreply',myhost)


def json_zip(j):
    j = base64.b64encode(
            zlib.compress(
                json.dumps(j).encode('utf-8')
            )
        ).decode('ascii')
    
    return j

def json_unzip(j, insist=True):
    try:
        j = zlib.decompress(base64.b64decode(j))
    except:
        raise RuntimeError("Could not decode/unzip the contents of "+j)

    try:
        j = json.loads(j)
    except:
        raise RuntimeError("Could interpret the unzipped contents of "+j)

    return j

def updateConfig(leaderip, nodeName):
    cmdline = '/TopStor/collectconfig.sh'.split()
    content = subprocess.run(cmdline,stdout=subprocess.PIPE, text=True).stdout
    print(content)
    zipped = json_zip(content)
    put(leaderip, 'getconfig/'+nodeName, zipped)

def getConfig(ldrip, nodeName):
    global leaderip,readies
    leaderip = ldrip
    with open('/root/collectconfig','w') as f:
        f.write(leaderip+' '+nodeName)
    stamp=str(time())
    dels(leaderip,'getconfig/dhcp','--prefix')
    if readies == 0:
     readies=get(leaderip,'ready','--prefix')
    for ready in readies:
        thishost=ready[0].split('/')[1]
        postchange(ready,nodeName)
    #put(leaderip,'sycgetconfig/__/request','getconfig_'+stamp)
    counter = 0
    while counter < 60:
        counter += 1
        sleep(1)
        if len(get(leaderip,'getconfig','--prefix')) == len(readies):
            counter = 100
    
def downloadConfig(ldrip,nodeName):
    global leaderip, readies
    leaderip = ldrip
    if readies == 0:
     readies=get(leaderip,'ready','--prefix')
    cmdline = 'rm -rf /TopStordata/config*'.split()
    content = subprocess.run(cmdline,stdout=subprocess.PIPE, text=True).stdout
    for ready in readies:
        noden = ready[0].split('/')[1]
        zipped = get(leaderip, 'getconfig/'+noden )[0]
        unzipped = json_unzip(zipped)
        with open("/TopStordata/" + 'config_'+ noden + ".txt", "w") as file:
            file.write(unzipped)
    return unzipped

if __name__=='__main__':
    leaderip = sys.argv[1]
    nodeName = sys.argv[2]
    with open('/root/collectconfig','w') as f:
        f.write(leaderip+' '+nodeName)
    getConfig(leaderip, nodeName)
    downloadConfig(leaderip, nodeName)
