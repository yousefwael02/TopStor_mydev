#!/bin/bash
ssh -p secureport -i /TopStordata/remotenode_keys/remotenode -N -R newport:mycluster:2379 remotenode Rremote receiver
if [ $? -ne 0 ];
then
	echo Somthing went wrong, removing active links to this remote node
	kill -9 `pgrep Rremote  -a | grep remotenode | awk '{print $1}'`
fi
