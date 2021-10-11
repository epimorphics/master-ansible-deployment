#! /bin/bash

set -e

BUCKET=${1}
DAYS=${2:-7}

if [ -z "$BUCKET" ]
then
  echo 'Usage: $0 <s3 bucket> [days (default 7)]'
  exit 1
fi

S3=s3://$BUCKET
#echo S3=$S3 >&2

lstdir () {
  aws s3 ls $1 | cut -b32-
}

stream () {
  DAY=$1
# echo DAY:$DAY >&2
  for host in $(lstdir ${S3}/logs/)
  do
#   echo host:$host >&2
    for log in $(lstdir ${S3}/logs/$host$DAY/)
    do
      if [[ $log =~ apache.info.proxy-[0-9]{2}-[0-9]{6}.gz ]]
      then
#       echo log:$log >&2
        aws s3 cp ${S3}/logs/$host$DAY/$log - | gzip -dc | grep -v '/server-status' | /usr/local/bin/json2combined.py
#     else
#       echo skip:$log >&2
      fi
    done
  done
}

mkdir -p /var/lib/docker/proxy/www/logs
for i in `seq 1 $DAYS` 
do
  DAY=$(date -d "-$i day" '+%F')
  stream $DAY
done | goaccess -e 10.0.0.0-10.255.255.255 --no-progress --log-format=VCOMBINED - > /var/lib/docker/proxy/www/logs/index.html

exit 0
