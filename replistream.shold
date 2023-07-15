#!/bin/sh
echo $@ > /root/replistream
partner=`echo $@ | awk '{print $1}'`
snapshot=`echo $@ | awk '{print $2}'`
nodeip=`echo $@ | awk '{print $3}'`
poolvol=`echo $@ | awk '{print $4}'`
partnerinfo=`./etcdgetlocal.py Partner/$partner`
pport=`echo $partnerinfo | awk -F'/' '{print $3}'`
phrase=`echo $partnerinfo | awk -F'/' '{print $NF}'`
clusterip=`./etcdgetlocal.py lederip`
strict='-oStrictHostKeyChecking=no' 
#isopen=`./checkpartner.sh $partner Receiver $nodeip $pport $clusterip $phrase old`
nodeloc='ssh -oBatchmode=yes -i /TopStordata/'${nodeip}'_keys/'${nodeip}' -p '$pport' -oStrictHostKeyChecking=no '${nodeip}
myvol=`echo $snapshot | awk -F'@' '{print $1}'`
volinfo=` ./etcdgetlocal.py vol $myvol`
volip=`echo $volinfo | awk -F'/' '{print $12}'`
volsubnet=` echo $volinfo | awk -F'/' '{print $13}' | awk -F"'" '{print $1}'` 
voltype=`echo $volinfo | awk -F'/' '{print $2}'`
groups=`echo $volinfo | awk -F'/' '{print $9}'`
quota=`zfs get quota $myvol -H | awk '{print $3}'`
echo $nodeloc /TopStor/targetcreatevol.sh $poolvol $volip $volsubnet $quota $voltype $groups
result=`$nodeloc /TopStor/targetcreatevol.sh $poolvol $volip $volsubnet $quota $voltype $groups`>/root/targetcreat
echo result = $result
echo $result | grep 'problem/@problem'
if [ $? -eq 0 ];
then
 echo result_cannot create volume result_ 
 exit
fi
poolvol=`echo $result | awk -F'result_' '{print $3}'`
#snapshot=`echo $snapshot | awk -F'@' '{print $1}'`
echo $result | grep 'newvol/@new'
if [ $? -eq 0 ];
then
 echo $result
 echo send -DvPc -i $snapshot TO $nodeloc zfs recv -F $poolvol > /root/sendtmp
 zfs send -DvPc -i $snapshot | $nodeloc zfs recv -F $poolvol 
 result=$?
else
 echo $result
 lastsnap=`echo $result | awk -F'result_' '{print $4}' | sed 's/ //g'`
 echo send -DvPc -i $myvol@$lastsnap $snapshot TO $nodeloc zfs recv -F $poolvol > /root/sendtmp2
 zfs send -DvPc -i $myvol@$lastsnap $snapshot | $nodeloc zfs recv -F $poolvol 
 result=$?
 echo 'zfs send -DvPc -I '$myvol'@'$lastsnap $snapshot' | '$nodeloc' zfs recv -F '$poolvol 
fi
#zfs send -Lc $snapshot | $nodeloc zfs recv -F $poolvol 
if [ $result -eq 0 ];
then
 props=`zfs get all $snapshot | awk '{print $2"="$3}' | grep ':' | grep -v receiver | tr '\n' ','`
 echo $nodeloc /TopStor/targetsetprop.sh $poolvol $clusterip ${props:0:-1}
 $nodeloc /TopStor/targetsetprop.sh $poolvol $clusterip ${props:0:-1}
fi
echo result2_${result}result2__
