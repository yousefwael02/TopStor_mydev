#!/bin/bash
ssh -p secureport -i /TopStordata/remotenode_keys/remotenode  -o ListenAddress=0.0.0.0 -N -R remotecluster:tunnelport:mycluster:2379 remotenode Rremote receiver
if [ $? -ne 0 ];
then
	echo Somthing went wrong, removing active links to this remote node
	kill -9 `pgrep Rremote  -a | grep remotenode | awk '{print $1}'`
fi
