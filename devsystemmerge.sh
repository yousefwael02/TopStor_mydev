#!/usr/bin/sh
fnupdate () {
	echo '###########################################' $1
	git branch -D $1
	git checkout -b $1
	#git reset --hard
	git clean -f
	git config --replace-all pull.rebase false
	git checkout -- *
	git rm -rf __py*
	rm -rf __py*
        git remote add $2 $3
	#git add --all
	#git commit -am 'fixing' 
	git pull $2 $1
	if [ $? -ne 0 ];
	then
		echo something went wrong while updating branch:$1 for repo $3 
		exit
	fi
	sync
	sync
	sync
}
cjobs=(`echo TopStor/TopStordev.git pace/HC.git topstorweb/TopStorweb.git`)
developer=$1
branch=$2
loc='http://10.11.11.252/git/'${developer}'_'
branchc=`echo y$branch | wc -c`
if [ $branchc -lt 4 ];
then
	echo no valid branch is supplied .... exiting
	exit
fi 
developerc=`echo y$developer | wc -c`
if [ $developerc -lt 3 ];
then
	echo no valid developer is supplied .... exiting
	exit
fi 
echo $branch | grep samebranch
if [ $? -eq 0 ];
then
	branch=`git branch | grep '*' | awk '{print $2}'`
fi
flag=1
while [ $flag -ne 0 ];
do
	rjobs=(`echo "${cjobs[@]}"`)
	echo rjobs=${rjobs[@]}
	for jobc in "${rjobs[@]}";
	do
		job=`echo $jobc | awk -F'/' '{print $1}'`
		devrepo=$loc`echo $jobc | awk -F'/' '{print $2}'`
 		echo $job
		cd /$job
		if [ $? -ne 0 ];
		then
			echo the directory $job is not found...exiting 
			exit
		fi
		fnupdate $branch $developer $devrepo
		cjobs=(`echo "${cjobs[@]}" | sed -e "s/$jobc//g" `)
  	done
	lencjobs=`echo $cjobs | wc -c`
	if [ $lencjobs -le 3 ];
	then
		flag=0
	fi
done
cd /TopStor
git show | grep commit
echo finished
