#!/bin/sh
echo $@ > /root/remotetunneladd
receiver=`echo $@ | awk '{print $1}'`
remotecluster=`echo $@ | awk '{print $2}'`
leaderip=`echo $@ | awk '{print $3}'`
remotenode=`echo $@ | awk '{print $4}'`
remoteport=`echo $@ | awk '{print $5}'`
tunnelport=`echo $@ | awk '{print $6}'`
rm -rf /TopStordata/${receiver}/Lremote_$receiver_${remotenode}*  
cp /TopStor/LREMOTE.sh /TopStordata/${receiver}/Lremote_${receiver}_${remotenode}_
rem='/TopStordata/'${receiver}'/Lremote_'${receiver}_${remotenode}_
sed -i "s/secureport/$remoteport/g" ${rem}
sed -i "s/receiver/$receiver/g" ${rem}
sed -i "s/remotenode/$remotenode/g" ${rem}
sed -i "s/mycluster/$leaderip/g" ${rem}
sed -i "s/remotecluster/$remotecluster/g" ${rem}
sed -i "s/tunnelport/$tunnelport/g" ${rem}
mv $rem ${rem}.sh
chmod +x ${rem}.sh 
pgrep Lremote_ -a | grep $rem | awk '{print $1}'
kill -9 `pgrep Lremote_ -a | grep $rem | awk '{print $1}'`

rm -rf /TopStordata/${receiver}/Rremote_${receiver}${remotenode}*  
cp /TopStor/RREMOTE.sh /TopStordata/${receiver}/Rremote_${receiver}_${remotenode}_
rem='/TopStordata/'${receiver}'/Rremote_'${receiver}_${remotenode}_
sed -i "s/secureport/$remoteport/g" ${rem}
sed -i "s/receiver/$receiver/g" ${rem}
sed -i "s/remotenode/$remotenode/g" ${rem}
sed -i "s/mycluster/$leaderip/g" ${rem}
sed -i "s/remotecluster/$remotecluster/g" ${rem}
sed -i "s/tunnelport/$tunnelport/g" ${rem}
mv $rem ${rem}.sh
chmod +x ${rem}.sh 
kill -9 `pgrep Rremote_  -a| grep $rem | awk '{print $1}'`
#/TopStor/activatetunnels.sh
echo hihihihihihi
tun=3
#while [ $tun -ne $tunnelport ];
#do
#	sleep 1 
#	/TopStor/etcdputnoport.py $leaderip $tunnelport replinextport $tunnelport
#	sleep 1 
#	tun=`/TopStor/etcdgetnoport.py $leaderip $tunnelport replinextport`
#	echo $tun, $tunnelport
#done
