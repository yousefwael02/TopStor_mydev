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

def updateConfig(leaderip, JSONCONFIG_KEY):
    cmdline = '/TopStor/collectconfig.sh'.split()
    content = subprocess.run(cmdline,stdout=subprocess.PIPE, text=True).stdout
    zipped = json_zip(content)
    put(leaderip, JSONCONFIG_KEY, zipped)

def getConfig(leaderip, JSONCONFIG_KEY):
    zipped = get(leaderip, JSONCONFIG_KEY)[0]
    unzipped = json_unzip(zipped)
    return unzipped

if __name__=='__main__':
    global leaderip, nodeName, JSONCONFIG_KEY
    leaderip = sys.argv[1]
    nodeName = sys.argv[2]
    JSONCONFIG_KEY = nodeName + "Config"
    updateConfig(leaderip, JSONCONFIG_KEY)
    print(getConfig(leaderip, JSONCONFIG_KEY))
