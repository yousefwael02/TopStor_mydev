#!/bin/bash
ssh -p secureport -i /TopStordata/remotenode_keys/remotenode -N -L newport:remotecluster:2379 remotenode
