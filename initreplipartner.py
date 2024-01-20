#!/usr/bin/python3
import sys, os, subprocess, logmsg
from allphysicalinfo import getall 
from etcdgetpy import etcdget as get
from etcdgetnoport import etcdget as getnoport
from etcdputnoport import etcdput as putnoport 
from etcdput import etcdput as put 
from etcddel import etcddel as dels 
from pumpkeys import pumpkeys, initpumpkeys
from time import sleep
from time import time as stamp
from sendhost import sendhost
from ast import literal_eval as mtuple


def submitkeys(partner, partnerip, isleader, myhost, myhostip, leaderip, repliport, phrase):
    cmdline = '/TopStor/preparekeys.sh '+partner+' '+partnerip
    result = subprocess.run(cmdline.split(),stdout=subprocess.PIPE).stdout.decode('utf-8').split('\n')[0].replace(' ','_spc_')
    if 'yes' in isleader:
        z=['/TopStor/receivekeys.sh',myhost,myhostip,leaderip, repliport, phrase, result]
    else:
        z=['/TopStor/sendreceivekeys.py',partnerip, myhost,myhostip,leaderip, repliport, phrase, result]
    msg={'req': 'Exchange', 'reply':z}
    try:
        sendhost(partnerip, str(msg),'recvreply',myhost)
    except:
        print('the cluster is down')
        exit()
    sleep(3)
    nodeloc = 'ssh -oBatchmode=yes -i /TopStordata/'+partner+'/'+partnerip+' -p '+repliport+' -oStrictHostKeyChecking=no '+partnerip
    print('ssh -oBatchmode=yes -i /TopStordata/'+partner+'/'+partnerip+' -p '+repliport+' -oStrictHostKeyChecking=no '+partnerip)
    count = 0 
    result=subprocess.run(nodeloc.split()+['ls'],stdout=subprocess.PIPE)
    while count < 10:
        if result.returncode == 0:
            isitopen = 'open'
            print('it is open now')
            break
        count += 1
        print('still closed')
        sleep(1) 
        result=subprocess.run(nodeloc.split()+['ls'],stdout=subprocess.PIPE)
    return nodeloc,result.returncode

def pumpcluster(*bargs):
 leaderip = bargs[0]
 myhostip = bargs[1]
 myhost = bargs[2]
 partner = bargs[3]
 partnerip = bargs[4]
 repliport = bargs[5]
 phrase = bargs[6]
 leadernodeloc, returncode = submitkeys(partner, partnerip, 'yes', myhost, myhostip, leaderip, repliport, phrase)
 if returncode != 0:
    return
 initPartnerReadies(leadernodeloc, partner, partnerip, myhost, myhostip, leaderip, repliport, phrase)

def initPartnerReadies(leadernodeloc,  partner, partnerip, myhost, myhostip, leaderip, repliport, phrase,tunnelport=''): 
 if 'readyonly' in leadernodeloc:
    partnerreadies = getnoport(leaderip, str(tunnelport),'ready','--prefix')
    print(leadernodeloc, partner, partnerip, myhost)
    knownreadies = os.listdir('/TopStordata/'+partner)
    partnerleader = getnoport(leaderip, str(tunnelport),'leader')[0]
    print('partnerleader',partnerleader)
 else:
    cmd = leadernodeloc + ' /TopStor/etcdget.py '+partnerip+' leader'
    partnerleader =subprocess.run(cmd.split(),stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n','')
    cmd = leadernodeloc + ' /TopStor/etcdget.py '+partnerip+' ready --prefix'
    partnerreadies =subprocess.run(cmd.split(),stdout=subprocess.PIPE).stdout.decode('utf-8')[:-1].split("\n")
 cmd=' /TopStor/etcdget.py '+leaderip+' replinextport' 
 port2 =subprocess.run(cmd.split(),stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n','')
 for tup in partnerreadies:
    if 'readyonly' in leadernodeloc:
        ready = tup
        if ready[1] in str(knownreadies):
            continue 
    else:
        ready = mtuple(tup)
    if partnerleader in ready[0]:
        isleader = 'yes'
        cmd = ' /TopStor/rmkeys.sh '+partner+' '+partnerip
        subprocess.run(cmd.split(),stdout=subprocess.PIPE).stdout.decode('utf-8')
    else:
        isleader = 'no'
    nodeloc, _ = submitkeys(partner, ready[1], isleader,  myhost, myhostip, leaderip, repliport, phrase)
    if partnerleader in ready[0]:
        leadernodeloc = nodeloc
        portcmd=' /TopStor/etcdget.py '+partnerip+' replinextport' 
    else:
        portcmd=' /TopStor/etcdget.py '+ready[1]+' replinextport' 
    cmd = leadernodeloc + portcmd
    port1 =subprocess.run(cmd.split(),stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n','')
    if int(port1) > int(port2):
        selectedport = int(port1) 
    else:
        selectedport = int(port2) 
    print('selectedport',port1, port2, selectedport)
    cmdline = '/TopStor/remotetunneladd.sh '+partner+' '+partnerip+' '+leaderip+' '+ready[1]+' '+repliport+' '+str(selectedport)
    print('/TopStor/remotetunneladd.sh '+partner+' '+partnerip+' '+leaderip+' '+ready[1]+' '+repliport+' '+str(selectedport))
    subprocess.run(cmdline.split(),stdout=subprocess.PIPE).stdout.decode('utf-8')
    if partnerleader in ready[0]:
        cmdline = nodeloc + ' /TopStor/etcdput.py '+partnerip+' replinextport '+str(selectedport+1)
    else:
        cmdline = nodeloc + ' /TopStor/etcdput.py '+ready[1]+' replinextport '+str(selectedport+1)
    subprocess.run(cmdline.split(),stdout=subprocess.PIPE).stdout.decode('utf-8')
    leader=get(leaderip,'leader')[0]
    if leader in myhost:
        cmdline = '/TopStor/etcdput.py '+leaderip+' replinextport '+str(selectedport+1)
    else:
        cmdline = '/TopStor/etcdput.py '+myhostip+' replinextport '+str(selectedport+1)
    subprocess.run(cmdline.split(),stdout=subprocess.PIPE).stdout.decode('utf-8')
    port2 = str(selectedport+1)
    
 
def checkpartner(nodeloccmd):
 isitopen = 'closed'
 count = 0
 resultdecod = 0
 print('sending to the cluster', nodeloccmd)
 try:
    result=subprocess.run(nodeloccmd.split(),stdout=subprocess.PIPE)
    if result.returncode == 0:
        isitopen = 'open'
        resultdecod = result.stdout.decode()
 except:
    resultdecod = 0
 return isitopen , resultdecod

def createnodeloc(leaderip, etcdip, receiver,userreq):
 cmd = 'ls'
 partnerinfo = get(leaderip, 'Partner/'+receiver)[0].split('/')
 remoteCluster = partnerinfo[0]
 replitype = partnerinfo[1]
 pport = partnerinfo[2]
 phrase = partnerinfo[-1]
 print(partnerinfo)
 print(replitype, pport, phrase, leaderip )
 nodesinfo = get(etcdip, 'repliPartner/'+receiver,'--prefix')
 isopen = 'closed'
 print('hi',nodesinfo)
 #nodesinfo.append(('hi/hi/'+partnerinfo[0],'hi')) 
 isopen = 'close'
 print(nodesinfo)
 for node in nodesinfo:
  print(node)
  nodeip = node[0].split('/')[2]
  nodeloc = 'ssh -oBatchmode=yes -i /TopStordata/'+partner+'/'+nodeip+' -p '+pport+' -oStrictHostKeyChecking=no ' + nodeip 
  nodeloccmd = nodeloc+' '+ cmd
  print('################################################333')
  print(nodeip)
  print(nodeloc)
  isopen, response = checkpartner(nodeloccmd)
  print('isopen',isopen)
  print('response', response)
  if isopen=='closed':
   return
  print(isopen)
  print(response)
  print('################################################333')
  if isopen == 'open':
    return nodeip, nodeloc, response
 nodeip = remoteCluster
 pumpkeys(nodeip, replitype, pport, phrase)
 nodeloc = 'ssh -oBatchmode=yes -i /TopStordata/'+nodeip+'/'+nodeip+' -p '+pport+' -oStrictHostKeyChecking=no ' + nodeip 
 nodeloccmd = nodeloc+' '+ cmd
 isopen, response = checkpartner(nodeloccmd)
 finalresponse = response
 if isopen != 'open':
    print('port is not open')
    finalresponse = 'result_failresult_ connection to all the nodes  cluster '+nodeip
 else:
    nodeloccmd = nodeloc +' '+ '/TopStor/nodeinfo.sh '+remoteCluster 
    print('################################################333')
    print(nodeip)
    print(nodeloccmd)
    print('################################################333')
    print('sending checkpartner')
    isopen, response = checkpartner(nodeloccmd)
    print('response',response)
    if isopen != 'open':
        finalresponse = 'result_failresult_ connection to remote node '+nodeip
    else:
        print('################################################333')
        print(response)
        print('################################################333')
        partnerinfo = response.split('_')
        try: 
            remotenextport = int(partnerinfo[4])
        except:
            remotenextport = 2380
        try:
            mynextport = int(get(etcdip,'replinextport')[0])
        except:
            mynextport = 2380
        replileader = partnerinfo[5]
        tunnelport = [ remotenextport ,mynextport ]
        print(tunnelport)
        tunnelport.sort()
        tunnelport = tunnelport[-1]+1 
        print(tunnelport)
        pumpkeys(partnerinfo[3], replitype, pport, phrase)
        put(etcdip,'repliPartner/'+receiver+'/'+partnerinfo[3], partnerinfo[2]+'/'+str(tunnelport))
        #if etcdip == leaderip:
        put(etcdip, 'replinextport',str(tunnelport))
        print('/TopStor/remotetunneladd.sh '+receiver+' '+remoteCluster+' '+leaderip+' '+partnerinfo[3]+' '+pport+' '+str(tunnelport))
        cmdline = '/TopStor/remotetunneladd.sh '+receiver+' '+remoteCluster+' '+leaderip+' '+partnerinfo[3]+' '+pport+' '+str(tunnelport)
        subprocess.run(cmdline.split(),stdout=subprocess.PIPE).stdout.decode('utf-8')
        cmdline='docker exec etcdclient /TopStor/etcdgetlocal.py clusternode'
        myhost=subprocess.run(cmdline.split(),stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n','').replace(' ','')
        cmdline='docker exec etcdclient /TopStor/etcdgetlocal.py clusternodeip'
        myip=subprocess.run(cmdline.split(),stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n','').replace(' ','')
        remotepartner = getnoport(leaderip, str(tunnelport),'Partner',leaderip)
        if leaderip not in remotepartner:
            #dels(leaderip,'Partner',receiver)
            logmsg.sendlog('Partnerfa01','info',userreq, receiver.split('_')[0])
        dels(leaderip,'sync','request/'+receiver)
        myalias = remotepartner[0][0].split('/')[1]
        putnoport(leaderip, str(tunnelport),'replireverse/'+myalias+'/'+receiver+'/'+leaderip, str(tunnelport))
        checkifok = getnoport(leaderip, str(tunnelport),'replireverse/'+myalias+'/'+receiver+'/'+leaderip)[0]
        if str(tunnelport) in checkifok:
            putnoport(leaderip, str(tunnelport),'replinextport', str(tunnelport))
            logmsg.sendlog('Partnersu01','info',userreq, receiver.split('_')[0])
        else:
            #dels(leaderip,'Partner',receiver)
            logmsg.sendlog('Partnerfa01','error',userreq, receiver.split('_')[0])

 if nodeip == remoteCluster and isopen != 'open' :
   finalresponse = 'result_failresult_ connection to all the nodes in the remote cluster '+nodeip
    
 return nodeip, nodeloc, finalresponse
 

if __name__=='__main__':
 if 'readyonly' in sys.argv[1]:
    initPartnerReadies(*sys.argv[1:]) 
 else:
    pumpcluster(*sys.argv[2:])
