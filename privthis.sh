#!/bin/sh
export ETCDCTL_API=3
cd /TopStor || exit 1

userreq="$(echo "$@" | awk '{print $2}')"
modpriv="$(echo "$@" | awk '{print $1}')"
superuser='admin'
sysuser='system'

if [ "$sysuser" = "$userreq" ] || [ "$superuser" = "$userreq" ]; then
 echo true
 exit 0
fi

if command -v docker >/dev/null 2>&1; then
 userraw="$(docker exec etcdclient /TopStor/etcdgetlocal.py "usersinfo/$userreq" 2>/dev/null)"
else
 userraw="$(/TopStor/etcdgetlocal.py "usersinfo/$userreq" 2>/dev/null)"
fi

userinfo="$(echo "$userraw" | awk -F"$modpriv" '{print $2}')"
priv="$(echo "$userinfo" | cut -c 2- | awk -F'/' '{print $1}')"

if echo "$priv" | grep -q 'true'; then
 echo "$priv"
else
 echo 'false'
fi
