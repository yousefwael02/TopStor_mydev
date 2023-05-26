#!/bin/sh
echo $@ > /root/receivekeys
partner=`echo $@ | awk '{print $1}'`
partnerip=`echo $@ | awk '{print $2}'`
clusterip=`echo $@ | awk '{print $3}'`
ptype=`echo $@ | awk '{print $4}'`
port=`echo $@ | awk '{print $5}'`
ppass=`echo $@ | awk '{print $6}'`
keys=`echo $@ | awk '{print $7}'`

leader=`docker exec etcdclient /TopStor/etcdgetlocal.py leader `
leaderip=`docker exec etcdclient /TopStor/etcdgetlocal.py leaderip `
myhost=`docker exec etcdclient /TopStor/etcdgetlocal.py clusternode `
myhostip=`docker exec etcdclient /TopStor/etcdgetlocal.py clusternodeip `
/TopStor/etcdget.py $leaderip Partner $clusterip | grep $ppass | grep $port 
if [ $? -eq 0 ];
then
 echo it is okok >> /root/receivekeys
 /TopStor/etcdput.py $leaderip nodesender/${clusterip}/$partnerip/$myhostip $partner
 echo $myhost | $leader
 if [ $? -ne 0 ];
 then
 	/TopStor/etcdput.py $myhostip nodesender/${clusterip}/$partnerip $partner   2>/dev/null
 fi
 authkeys=`cat /root/.ssh/authorized_keys | grep -v $partner`
 echo $authkeys > /root/.ssh/authorized_keys
 echo $keys | sed 's/\_spc\_/ /g' >> /root/.ssh/authorized_keys
 sshd=`cat /etc/ssh/sshd_config | grep -v "Port 22" | grep -v $port`
 echo -e "$sshd" > /etc/ssh/sshd_config
 echo -e "Port $port \r"  >> /etc/ssh/sshd_config
 echo -e "Port 22 \r" >> /etc/ssh/sshd_config
 firewall-cmd --permanent --add-port=$port/udp
 firewall-cmd --permanent --add-port=$port/tcp
 firewall-cmd --reload
 systemctl restart sshd
 chmod 004 /root/.ssh/authorized_keys
fi
