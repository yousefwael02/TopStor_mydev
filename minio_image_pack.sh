#!/bin/sh
set -eu

server_image="${MINIO_SERVER_IMAGE:-quay.io/minio/minio:latest}"
mc_image="${MINIO_MC_IMAGE:-minio/mc:latest}"
server_archive="${MINIO_SERVER_ARCHIVE:-/TopStor/minio-server.tar.gz}"
mc_archive="${MINIO_MC_ARCHIVE:-/TopStor/minio-mc.tar.gz}"

mkdir -p /TopStor

docker pull "$server_image"
docker pull "$mc_image"

docker save "$server_image" | gzip -c > "$server_archive"
docker save "$mc_image" | gzip -c > "$mc_archive"

echo "Packed $server_image into $server_archive"
echo "Packed $mc_image into $mc_archive"
