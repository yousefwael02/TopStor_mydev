#!/usr/bin/sh
fnupdate () {
	origin='http://10.11.11.252/git/'$1'.git'
	remote='http://github.com/'$2'/'$1'_mydev.git'
	git init
	git remote add origin $origin
	git remote add remote $remote 
	git fetch $remote 
	if [ $? -ne 0 ];
	then
		echo something went wrong while fetching for the first time  from remote $remote.. consult the devleloper
		echo However, will continue creating the repos
	fi
	sync
	sync
	sync
}
echo nameserver 8.8.8.8 > /etc/resolv.conf
cjobs=(`echo TopStor pace topstorweb`)
developer=$1
branchc=`echo $developer | wc -c`
if [ $branchc -le 3 ];
then
	echo no valid developer name is supplied .... exiting
	exit
fi 
flag=1
while [ $flag -ne 0 ];
do
	rjobs=(`echo "${cjobs[@]}"`)
	echo rjobs=${rjobs[@]}
	for job in "${rjobs[@]}";
	do
		echo '###########################################'
 		echo ${job}_${developer}
		echo xx$2 | grep init
		if [ $? -eq 0 ];
		then
			echo re-creating the complete ${job}_${developer} repo
			rm -rf /${job}_${developer}
		fi
		mkdir /${job}_${developer}
		cd /${job}_${developer}
		if [ $? -ne 0 ];
		then
				echo the directory $job is not found... exiting
				exit
		fi
		fnupdate $job $developer 
		cjobs=(`echo "${cjobs[@]}" | sed "s/$job//g" `)
  	done
	lencjobs=`echo $cjobs | wc -c`
	if [ $lencjobs -le 3 ];
	then
		flag=0
	fi
done
cd /TopStor
echo finished
