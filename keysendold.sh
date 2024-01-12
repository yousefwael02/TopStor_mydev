#!/bin/sh
export PATH=/bin:/usr/bin:/sbin:/usr/sbin:/root
declare -a targets=(`cat /pacedata/iscsitargets | awk '{print $2}'`);
myhost=`hostname -s`
myaddCC=`echo $@ | awk '{print $1}'`
myhostCC=`cat /TopStordata/hostname`
 echo 127.0.0.1 localhost > /etc/hosts
 echo $myaddCC $myhostCC >> /etc/hosts
 echo $myaddCC $myhost >> /etc/hosts
 echo 127.0.0.1 $myhost >> /etc/hosts
if [[ ! -f /root/.ssh/id_rsa ]] ;then 
 ssh-keygen -t rsa -f /root/.ssh/id_rsa -q -P "";
fi
securessh=$(expect -c "
 set timeout 10
 spawn ssh-copy-id -i /root/.ssh/id_rsa.pub root@$myhostCC 
 expect \"*\?\"
 send \"yes\r\"
 expect \"*assword:\"
 send \"Abdoadmin\r\"
 expect eof
 ")
securessh=$(expect -c "
 set timeout 10
 spawn ssh-copy-id -i /root/.ssh/id_rsa.pub root@$myhost 
 expect \"*\?\"
 send \"yes\r\"
 expect \"*assword:\"
 send \"Abdoadmin\r\"
 expect eof
 ")
