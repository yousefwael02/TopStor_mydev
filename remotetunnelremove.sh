#!/bin/sh
receiver=`echo $@ | awk '{print $1}'`
rm -rf /TopStordata/Lremote_${receiver}*  
rm -rf /TopStordata/Rremote_${receiver}*  
kill -9 `pgrep Lremote_ -a | grep $receiver | awk '{print $1}'`
kill -9 `pgrep ssh -a | grep ssh$receiver | awk '{print $1}'`

rm -rf /TopStordata/Rremote_${receiver}*  
kill -9 `pgrep Rremote_  -a| grep $receiver | awk '{print $1}'`
kill -9 `pgrep ssh  -a| grep ssh$receiver | awk '{print $1}'`
