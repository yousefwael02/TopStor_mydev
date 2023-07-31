import os
import subprocess

def convertToDicts(data):
    keys = data[0].split()
    interfaces = []
    for values in data[1:]:
        if (values.replace(" ","") != ""):
            interface = dict(zip(keys,values.split()))
            interfaces.append(interface)
    return interfaces
def getInterfaces():
    cmdline = ['nmcli', 'device', 'status']
    result = subprocess.run(cmdline, stdout=subprocess.PIPE)
    availableInterfaces = str(result.stdout.decode()).replace('\n\n','n').split('\n')
    ethernetInterfaces = []
    for interface in convertToDicts(availableInterfaces):
        if (interface["TYPE"] == "ethernet" and not interface["DEVICE"].startswith('veth')):
            ethernetInterfaces.append(interface["DEVICE"])
    with open("/TopStor/hi.txt",'w') as f:
        for interface in ethernetInterfaces:
            f.write(interface)
            f.write(" HEHE")
    print(ethernetInterfaces)
if __name__=='__main__':
    getInterfaces()
