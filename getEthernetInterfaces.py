import os
import subprocess
from etcdput import etcdput as put
def convertToDicts(data):
    keys = data[0].split()
    interfaces = []
    for values in data[1:]:
        if (values.replace(" ","") != ""):
            interface = dict(zip(keys,values.split()))
            interfaces.append(interface)
    return interfaces
def setInterfaces():
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
        put(argv[0], 'port/' + argv[1] + '/' + interface, 'eth' + str(counter))
        counter += 1
if __name__=='__main__':
    setInterfaces(*sys.argv[1:])
