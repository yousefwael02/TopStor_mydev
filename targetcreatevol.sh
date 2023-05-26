#!/bin/sh
echo $@ > /root/targetcreatevol
cd /TopStor

pool=`echo $@ | awk '{print $1}' | awk -F'/' '{print $1}'`
name=`echo $@ | awk '{print $1}' | awk -F'/' '{print $2}'`
ipaddress=`echo $@ | awk '{print $2}'`
Subnet=`echo $@ | awk '{print $3}'`
size=`echo $@ | awk '{print $4}'`
typep=`echo $@ | awk '{print $5}'`
groups=`echo $@ | awk '{print $6}'`
oldsnap=`echo $@ | awk '{print $7}'`
myhost=`docker exec etcdclient /TopStor/etcdgetlocal.py clusternode`
myhostip=`docker exec etcdclient /TopStor/etcdgetlocal.py clusternodeip`
leader=`docker exec etcdclient /TopStor/etcdgetlocal.py leader`
leaderip=`docker exec etcdclient /TopStor/etcdgetlocal.py leaderip`
echo $leader | grep $myhost
if [ $? -ne 0 ];
then
	etcd=$myhostip
else
        etcd=$leaderip
fi

newvol=`/TopStor/etcdget.py $leaderip vol $name | grep $pool | awk -F'/' '{print $6}'`
echo $newvol | grep $name 
if [ $? -eq 0 ];
then
 volinfo=`/TopStor/etcdget.py $leaderip vol $newvol`
 zfs unmount -f $pool/${newvol}
 #latestsnap=`/TopStor/getlatestsnap.py $newvol | awk -F'result_' '{print $2}'`
 echo zfs rollback $pool/$newvol@$oldsnap
 echo 'noold' | grep $oldsnap
 if [ $? -eq 0 ];
 then
  zfs list -t snapshot -o name | grep ^${pool}/${newvol}@  | tac | xargs -n 1 zfs destroy -r 
 else
  zfs rollback -r $pool/$newvol@$oldsnap
 fi
 oldnew='old'
else 
 echo ./createmyvol.py $myhost $myhostip $pool $name $ipaddress $Subnet $size $typep $groups > /root/targetcreatevol
 ./createmyvol.py $myhost $myhostip $pool $name $ipaddress $Subnet $size $typep $groups
 oldnew='new'
 latestsnap=''
 zfs destroy -f $pool/${newvol}
fi
newvol=`/TopStor/etcdget.py $leaderip vol $name | grep $pool | awk -F'/' '{print $6}'`
echo $newvol | grep $name 
if [ $? -eq 0 ];
then
 volinfo=`/TopStor/etcdget.py $leaderip vol $newvol`
 volleft=` echo $volinfo | awk -F"'," '{print $1}' | awk -F"'" '{print $2}'`
 volright=` echo $volinfo | awk -F"'," '{print $2}' | awk -F"'" '{print $2}'`
 volleft=`echo $volleft | sed 's/active/replica/g'`
 zfs set status:mount=disabled $pool/$newvol 
 echo /TopStor/etcdput.py $leaderip $volleft $volright
 /TopStor/etcdput.py $leaderip $volleft $volright
 stamp=`date +%s`
 ETCDCTL_API=3 /pace/etcdput.py $leaderip sync/volumes/${pool}_$newvol/request volumes_$stamp
 ETCDCTL_API=3 /pace/etcdput.py $leaderip sync/volumes/${pool}_$newvol/request/$leader volumes_$stamp
 docker rm -f `docker ps | grep $ipaddress | awk '{print $1}'` 2>/dev/null
 echo result_${oldnew}vol/@${oldnew}result_$pool/${newvol}result_${latestsnap}result_
else
 echo result_problem/@newresult_
fi 
