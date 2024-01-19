#!/bin/sh
partner=`echo $@ | awk '{print $1}'`
partnerip=`echo $@ | awk '{print $2}'`
cd /TopStordata/
cd ${partner}_keys 
rm -rf ${partnerip}.pub
rm -rf ${partnerip}
