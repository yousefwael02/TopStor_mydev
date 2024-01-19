#!/bin/sh
echo $@ > /root/preptmp
partner=`echo $@ | awk '{print $1}'`
partnerip=`echo $@ | awk '{print $2}'`
cd /TopStordata/
mkdir ${partner} 2>/dev/null
cd ${partner} 
rm -rf ${partnerip} 2>/dev/null
rm -rf ${partnerip}.pub 2>/dev/null
ssh-keygen -f $partnerip -N "" 1>/dev/null
cat ${partnerip}.pub

