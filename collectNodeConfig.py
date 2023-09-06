#!/bin/python
import sys, subprocess, re, zlib, json, base64
from etcdget import etcdget as get 
from etcdput import etcdput as put

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
        raise RuntimeError("Could not decode/unzip the contents")

    try:
        j = json.loads(j)
    except:
        raise RuntimeError("Could interpret the unzipped contents")

    return j

def updateConfig(leaderip, nodeName):
    cmdline = '/TopStor/collectconfig.sh'.split()
    content = subprocess.run(cmdline,stdout=subprocess.PIPE, text=True).stdout
    zipped = json_zip(content)
    put(leaderip, nodeName + "_config", zipped)

def getConfig(leaderip, nodeName):
    zipped = get(leaderip, nodeName + "_config")[0]
    unzipped = json_unzip(zipped)
    with open("/TopStordata/" + nodeName + "_config.txt", "w") as file:
        file.write(unzipped)
    return unzipped

if __name__=='__main__':
    leaderip = sys.argv[1]
    nodeName = sys.argv[2]
    updateConfig(leaderip, nodeName)
