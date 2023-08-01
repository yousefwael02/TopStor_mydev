#!/bin/python
import os,sys
import subprocess
from time import time as stamp
from etcdput import etcdput as put

def dosync(sync,  *args):
  global leaderip, leader
  dels(leaderip, 'sync',sync)
  put(leaderip, *args)
  put(leaderip, args[0]+'/'+leader,args[1])
  return

def convertToDicts(data):
    keys = data[0].split()
    interfaces = []
    for values in data[1:]:
        if (values.replace(" ","") != ""):
            interface = dict(zip(keys,values.split()))
            interfaces.append(interface)
    return interfaces
def setInterfaces(*argv):
    cmdline = ['nmcli', 'device', 'status']
    result = subprocess.run(cmdline, stdout=subprocess.PIPE)
    availableInterfaces = str(result.stdout.decode()).replace('\n\n','n').split('\n')
    ethernetInterfaces = []
    for interface in convertToDicts(availableInterfaces):
        #if (interface["TYPE"] == "ethernet" and not interface["DEVICE"].startswith('veth')):
        if (interface["TYPE"] == "ethernet"):
            ethernetInterfaces.append(interface["DEVICE"])
    counter = 0
    for interface in ethernetInterfaces:
        put(argv[0], 'ports/' + argv[1] + '/' + interface, 'eth' + str(counter))
        counter += 1
    stampit = str(stamp())
    dosync('ports_', 'sync/ports/add/request','ports_'+stampit)
if __name__=='__main__':
    with open("/TopStor/a.txt",'w') as f:
        f.write(sys.argv[1])
        f.write(" " + sys.argv[2])
        
    setInterfaces(*sys.argv[1:])
