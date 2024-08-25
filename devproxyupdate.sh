#!/usr/bin/sh
fnupdate () {
	git branch -D $1
	origin=`git remote -v | grep 252 | head -1 | awk '{print $1}'`
	remote=`git remote -v | grep github | head -1 | awk '{print $1}'`
	git fetch $remote 
	if [ $? -ne 0 ];
	then
		echo something went wrong while pulling from remote $remote, branch: $1, dir:`pwd` .... consult the devleloper
		exit
	fi
	git checkout -b $1  $remote/$1
	if [ $? -ne 0 ];
	then
		echo something went wrong while pulling from remote $remote, branch: $1, dir:`pwd` .... consult the devleloper
		exit
	fi
	git reset --hard $remote/$1
	git clean -f
	git config --replace-all pull.rebase false
	git checkout -- *
	git rm -rf __py*
	git push $origin $1
	if [ $? -ne 0 ];
	then
		echo something went wrong while pushing to origin: $origin, branch: $1, dir:`pwd` .... consult the devleloper
		exit
	fi
	sync
	sync
	sync
}
echo nameserver 8.8.8.8 > /etc/resolv.conf
cjobs=(`echo TopStor pace topstorweb`)
branch=$1
developer=`pwd | awk -F'_' '{print $2}'`
branchc=`echo $branch | wc -c`
if [ $branchc -le 3 ];
then
	echo no valid branch is supplied .... exiting
	exit
fi 
developer=`pwd | awk -F'_' '{print $2}'`
dev=$2
devc=`echo $dev | wc -c`
if [ $devc -le 3 ];
then
	echo no valid developer name is supplied .... exiting
	exit
fi 
ondevtopstor=`ls / | grep $dev | grep TopStor`
devl=`echo x$ondevtopstor | wc -l` 
if [ $devl -ge 1 ];
then
	echo choose between:
	echo $ondevtopstor | awk -F'_' '{$NF}' 
	exit
fi

if [ $devl -eq 0 ];
then
	echo No such developer $dev 
	exit
fi
developer=$dev
flag=1
while [ $flag -ne 0 ];
do
	rjobs=(`echo "${cjobs[@]}"`)
	echo rjobs=${rjobs[@]}
	for job in "${rjobs[@]}";
	do
		echo '###########################################'
 		echo ${job}_${developer}
		isexit=1
		cd /${job}_${developer}
		if [ $? -ne 0 ];
		then
				echo the directory $job is not found... exiting
				exit
		fi
		fnupdate $branch $developer 
		cjobs=(`echo "${cjobs[@]}" | sed "s/$job//g" `)
  	done
	lencjobs=`echo $cjobs | wc -c`
	if [ $lencjobs -le 3 ];
	then
		flag=0
	fi
done
cd /TopStor_$developer
echo the latest commit in the $developer repo:
git show | grep commit
cd /TopStor
echo finished
