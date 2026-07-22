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
minio_image="${MINIO_SERVER_IMAGE:-quay.io/minio/minio:latest}"
minio_archive="${MINIO_SERVER_ARCHIVE:-/TopStor/minio-server.tar.gz}"

mkdir -p /$pool/$name/$bucket

if ! docker image inspect "$minio_image" >/dev/null 2>&1; then
 if [ -f "$minio_archive" ]; then
  docker load -i "$minio_archive" >/dev/null 2>&1 || exit 1
 fi
fi

if ! docker image inspect "$minio_image" >/dev/null 2>&1; then
 exit 1
fi

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
  "$minio_image" server /data --console-address ":9001"
