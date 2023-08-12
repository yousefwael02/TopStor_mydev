#!/bin/sh
receiver=`echo $@ | awk '{print $1}'`
remotecluster=`echo $@ | awk '{print $2}'`
leaderip=`echo $@ | awk '{print $3}'`
remotenode=`echo $@ | awk '{print $4}'`
remoteport=`echo $@ | awk '{print $5}'`
rm -rf /TopStordata/Lremote_${receiver}${remotenode}*  
cp /TopStor/LREMOTE.sh /TopStordata/Lremote_${receiver}${remotenode}
rem='/TopStordata/Lremote_'${receiver}$remotenode
sed -i "s/secureport/$remoteport/g" ${rem}
sed -i "s/remotenode/$remotenode/g" ${rem}
sed -i "s/newport/2381/g" ${rem}
sed -i "s/remotecluster/$remotecluster/g" ${rem}
mv $rem ${rem}.sh
chmod +x ${rem}.sh 
pgrep Lremote_ -a | grep $rem | awk '{print $1}'
kill -9 `pgrep Lremote_ -a | grep $rem | awk '{print $1}'`

rm -rf /TopStordata/Rremote_${receiver}${remotenode}*  
cp /TopStor/RREMOTE.sh /TopStordata/Rremote_${receiver}${remotenode}
rem='/TopStordata/Rremote_'${receiver}$remotenode
sed -i "s/secureport/$remoteport/g" ${rem}
sed -i "s/remotenode/$remotenode/g" ${rem}
sed -i "s/newport/2381/g" ${rem}
sed -i "s/mycluster/$leaderip/g" ${rem}
mv $rem ${rem}.sh
chmod +x ${rem}.sh 
kill -9 `pgrep Rremote_  -a| grep $rem | awk '{print $1}'`
