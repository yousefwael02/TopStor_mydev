#!/bin/bash

declare -a actives=`/TopStor/etcdget.py $@ Active --prefix | awk '{print $2}' | awk -F"'" '{print $2}'`

echo $actives
# Loop over the array of lines
rm -rf /TopStordata/promgraf/prom.yml
for line in "${actives[@]}"; do
  # Process each line in the loop
  echo "$line"
  sed "s/MYNODEIP/$line/g" /TopStor/prom.yml > /TopStordata/promyaml
  cat /TopStordata/promyaml >> /TopStordata/promgraf/prom.yml
  rm -rf /TopStordata/promyaml
done

