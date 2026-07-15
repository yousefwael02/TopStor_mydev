#!/bin/sh
cd /TopStor
export ETCDCTL_API=3
echo $@ > /root/s3shparam

pool=`echo $@ | awk '{print $1}'`
name=`echo $@ | awk '{print $2}'`
bucket=`echo $@ | awk '{print $3}'`
ipaddr=`echo $@ | awk '{print $4}'`
ipsubnet=`echo $@ | awk '{print $5}'`
accesskey=`echo $@ | awk '{print $6}'`
secretkey=`echo $@ | awk '{print $7}'`
apiport=`echo $@ | awk '{print $8}'`
consoleport=`echo $@ | awk '{print $9}'`
resname=S3-$ipaddr

mkdir -p /$pool/$name/$bucket
docker rm -f $resname
nmcli conn mod cmynode -ipv4.addresses ${ipaddr}/$ipsubnet
nmcli conn mod cmynode +ipv4.addresses ${ipaddr}/$ipsubnet
nmcli conn up cmynode

docker run -d --rm \
  -p $ipaddr:$apiport:9000 \
  -p $ipaddr:$consoleport:9001 \
  -e MINIO_ROOT_USER=$accesskey \
  -e MINIO_ROOT_PASSWORD=$secretkey \
  -v /$pool/$name:/data \
  --name $resname \
  quay.io/minio/minio server /data --console-address ":9001"