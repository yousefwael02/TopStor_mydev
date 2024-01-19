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
msg={'req': 'Exchange', 'reply':z}
endhost(ownerip, str(msg),'recvreply',myhost)
