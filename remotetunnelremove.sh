#!/bin/sh
echo $@ > /root/remtunnremove
receiver=`echo $@ | awk '{print $1}'`
rm -rf /TopStordata/$receiver  
kill -9 `pgrep Lremote_ -a | grep $receiver | awk '{print $1}'`
kill -9 `pgrep ssh -a | grep ssh$receiver | awk '{print $1}'`
