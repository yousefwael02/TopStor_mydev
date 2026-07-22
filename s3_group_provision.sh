#!/bin/sh
set -eu

leaderip="$1"
bucket="$2"
ipaddr="$3"
apiport="$4"
root_access="$5"
root_secret="$6"
groups_csv="$7"
mc_image="${MINIO_MC_IMAGE:-minio/mc:latest}"
mc_archive="${MINIO_MC_ARCHIVE:-/TopStor/minio-mc.tar.gz}"

if [ -z "$groups_csv" ] || [ "$groups_csv" = "NoGroup" ]; then
 exit 0
fi

mc_host_url="http://${root_access}:${root_secret}@${ipaddr}:${apiport}"

mc_cmd() {
 if command -v mc >/dev/null 2>&1; then
  MC_HOST_s3="$mc_host_url" mc "$@"
 else
  if ! docker image inspect "$mc_image" >/dev/null 2>&1; then
   if [ -f "$mc_archive" ]; then
    docker load -i "$mc_archive" >/dev/null 2>&1 || return 1
   fi
  fi
  docker image inspect "$mc_image" >/dev/null 2>&1 || return 1
  docker run --rm --network host -v /tmp:/tmp -e MC_HOST_s3="$mc_host_url" "$mc_image" "$@"
 fi
}

trim() {
 echo "$1" | sed 's/^ *//;s/ *$//'
}

sanitize_name() {
 printf '%s' "$1" | tr -c '[:alnum:]_.-' '_' | tr '[:upper:]' '[:lower:]'
}

make_secret() {
 seed="$1"
 if command -v sha256sum >/dev/null 2>&1; then
  printf '%s' "$seed" | sha256sum | awk '{print $1}' | cut -c1-32
 elif command -v openssl >/dev/null 2>&1; then
  printf '%s' "$seed" | openssl dgst -sha256 | awk '{print $2}' | cut -c1-32
 else
  printf '%s' "$seed" | tr -c '[:alnum:]' 'a' | cut -c1-32
 fi
}

policy_file="/tmp/minio_policy_$$.json"
cleanup() {
 rm -f "$policy_file"
}
trap cleanup EXIT INT TERM

cat > "$policy_file" <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetBucketLocation", "s3:ListBucket"],
      "Resource": ["arn:aws:s3:::$bucket"]
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:AbortMultipartUpload",
        "s3:ListMultipartUploadParts"
      ],
      "Resource": ["arn:aws:s3:::$bucket/*"]
    }
  ]
}
POLICY

policy_name="s3_$(sanitize_name "$bucket")_rw"

if ! mc_cmd admin policy create s3 "$policy_name" "$policy_file" >/dev/null 2>&1; then
 if ! mc_cmd admin policy add s3 "$policy_name" "$policy_file" >/dev/null 2>&1; then
  mc_cmd admin policy remove s3 "$policy_name" >/dev/null 2>&1 || true
  mc_cmd admin policy create s3 "$policy_name" "$policy_file" >/dev/null 2>&1 || mc_cmd admin policy add s3 "$policy_name" "$policy_file" >/dev/null 2>&1
 fi
fi

old_ifs="$IFS"
IFS=','
for raw_group in $groups_csv; do
 group_name="$(trim "$raw_group")"
 if [ -z "$group_name" ] || [ "$group_name" = "NoGroup" ]; then
  continue
 fi

 group_record="$(docker exec etcdclient /TopStor/etcdgetlocal.py "usersigroup/$group_name" 2>/dev/null | tr -d '\r')"
 if [ -z "$group_record" ] || echo "$group_record" | grep -q "_1"; then
  continue
 fi

 users_csv="$(echo "$group_record" | awk -F'/' '{print $3}')"
 if [ -z "$users_csv" ] || [ "$users_csv" = "NoUser" ]; then
  continue
 fi

 minio_group="sysgrp_$(sanitize_name "$group_name")"
 set --

 user_ifs="$IFS"
 IFS=','
 for raw_user in $users_csv; do
  sys_user="$(trim "$raw_user")"
  [ -z "$sys_user" ] && continue

  minio_user="$(sanitize_name "$sys_user")"
  [ -z "$minio_user" ] && continue

  user_secret="$(make_secret "${bucket}:${minio_user}")"

  if ! mc_cmd admin user info s3 "$minio_user" >/dev/null 2>&1; then
   mc_cmd admin user add s3 "$minio_user" "$user_secret" >/dev/null 2>&1 || true
  fi

  ETCDCTL_API=3 /pace/etcdput.py "$leaderip" "s3users/$bucket/$minio_user" "${minio_user}/${user_secret}" >/dev/null 2>&1 || true
  set -- "$@" "$minio_user"
 done
 IFS="$user_ifs"

 if [ "$#" -gt 0 ]; then
  mc_cmd admin group add s3 "$minio_group" "$@" >/dev/null 2>&1 || true
  mc_cmd admin policy attach s3 "$policy_name" --group "$minio_group" >/dev/null 2>&1 || mc_cmd admin policy set s3 "$policy_name" "group=$minio_group" >/dev/null 2>&1 || true
 fi
done
IFS="$old_ifs"

exit 0
