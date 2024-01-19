#!/usr/bin/python3
import sys
from sendhost import sendhost

ownerip = sys.argv[1]
myhost = sys.argv[2]
myhostip = sys.argv[3]
nodeip = sys.argv[4]
repliport = sys.argv[5]
phrase = sys.argv[6]
result = sys.argv[7]
z=['/TopStor/receivekeys.sh',myhost,myhostip,nodeip, repliport, phrase, result]
with open('/root/sendrectmp','w') as f:
    f.write(' '.join(z)+'\n')
    f.write(ownerip)
msg={'req': 'Exchange', 'reply':z}
sendhost(ownerip, str(msg),'recvreply',myhost)
