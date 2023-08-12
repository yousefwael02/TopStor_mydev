#!/bin/bash
ssh -p secureport -i /TopStordata/remotenode_keys/remotenode -N -R newport:mycluster:2379 remotenode
