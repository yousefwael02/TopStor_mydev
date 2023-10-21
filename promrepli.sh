#!/bin/sh
cd /TopStor/
leaderip=`echo $@ | awk '{print $1}'`
myhostip=`echo $@ | awk '{print $2}'`
rm -rf /prom/prom.yml
cp /TopStor/promrepli.yml  /prom/promyaml
sed -i "s/LEADERIP/$leaderip/g" /prom/promyaml
cat /prom/promyaml >> /prom/prom.yml
rm -rf /prom/promyaml
docker rm -f promserver
docker rm -f promgraf
	docker run -d -p $myhostip:9090:9090 -v /prom/prom.yml:/etc/prometheus/prometheus.yml -v /prom/:/prometheus -v /etc/passwd:/etc/passwd -v /etc/group:/etc/group --name promserver prom/prometheus
 	rm -rf /promgraf/hosts
 	cp /TopStor/promgrafhosts /promgraf/hosts
 	sed -i "s/MYCLUSTER/$myhostip/g" /promgraf/hosts 
 	docker run -d -p $myhostip:4000:3000 -v /promgraf/grafana.ini:/etc/grafana/grafana.ini -v /promgraf:/var/lib/grafana -v /promgraf/hosts:/etc/hosts --name promgraf grafana/grafana
