#!/usr/bin/python3
import sys
from sendhost import sendhost

myhost = sys.argv[1]
myhostip = sys.argv[2]
nodeip = sys.argv[3]
repliport = sys.argv[4]
phrase = sys.argv[5]
result = sys.argv[6]
z=['/TopStor/sendreceivekeys.sh',myhost,myhostip,leaderip, repliport, phrase, result]
msg={'req': 'Exchange', 'reply':z}
endhost(partnerip, str(msg),'recvreply',myhost)
