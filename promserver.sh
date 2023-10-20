#!/bin/sh
cd /TopStor/
leaderip=`echo $@ | awk '{print $1}'`
echo $@  > /root/promserver
declare -a actives=(`/TopStor/etcdget.py $1 Active --prefix | awk '{print $2}' | awk -F"'" '{print $2}'`)
declare -a ports=(`echo -e ":9100\n:9101\n:19916"`)
rm -rf /prom/prom.yml
cp /TopStor/prom.yml  /prom/promyaml
counter=1
for port in "${ports[@]}"; do
	portstr=''
	for line in "${actives[@]}"; do
  	# Process each line in the loop
		portstr=${portstr}${line}${port}','
	done
	echo portstr="$portstr"
  	sed -i "s/PORTSTR${counter}/$portstr/g" /prom/promyaml
	counter=$((counter+1))
done
cat /prom/promyaml >> /prom/prom.yml
rm -rf /prom/promyaml
docker ps | grep  promserver
if [ $? -eq 0 ];
then
 docker restart promserver
 docker restart promgraf
fi
