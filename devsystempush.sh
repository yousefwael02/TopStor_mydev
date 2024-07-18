#!/usr/bin/sh

branch=`echo $@ | awk '{print $1}'`
hostname=`hostname`
/TopStor/systempush.sh ${branch}_$hostname
