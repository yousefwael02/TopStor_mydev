#!/bin/sh

# Identify local node and leader
myhost=$(docker exec etcdclient /TopStor/etcdgetlocal.py clusternode)
leader=$(docker exec etcdclient /TopStor/etcdgetlocal.py leader)

# Only execute snapshots if this node is the leader
echo "$leader" | grep -q "$myhost" || exit 0

# Capture the command and its first argument
cmd="$1"
target="$2"
shift 2

# Resolve leader IP dynamically if "LEADER" token is used
if [ "$target" = "LEADER" ]; then
    target=$(docker exec etcdclient /TopStor/etcdgetlocal.py leaderip 2>/dev/null)
fi

# Fail if leader IP cannot be resolved
if [ -z "$target" ]; then
    echo "$(date) ERROR: Unable to resolve leader IP" >> /var/log/snapshot.log
    exit 1
fi

# Execute the original command with resolved IP
exec "$cmd" "$target" "$@"

