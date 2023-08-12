#!/bin/bash
ssh -p secureport -i /TopStordata/remotenode_keys/remotenode -N -L tunnelport:remotecluster:2379 remotenode Lremote receiver
if [ $? -ne 0 ];
then
	echo Somthing went wrong, removing active links to this remote node
	kill -9 `pgrep Lremote  -a | grep remotenode | awk '{print $1}'`
fi
