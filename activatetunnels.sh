#!/bin/bash
#!/bin/bash

# Get the current directory
current_dir='/TopStordata'

# List the files in the directory
files=$(ls $current_dir | egrep 'Lremote|Rremote')
tasks=`ps -ef | egrep 'Lremote|Rremote'`
# Loop through the files
for file in $files; do
	echo file=$file
	echo tasks$tasks | grep $file  >/dev/null
	if [ $? -ne 0 ];
	then
		echo running $file
		$current_dir/$file & disown
		if [ $? -ne 0 ];
		then
			echo Somthing went wrong, removing active links to this remote node
			node=` echo $file | awk -F'_' '{print $2}'`
			ttype=`echo $file | awk -F'/' '{print $NF}' | awk -F'_' '{print $1}'`
			kill -9 `pgrep $ttype -a | grep $node | awk '{print $1}'`
		fi
	fi

done

