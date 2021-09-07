#! /bin/bash

set -e

YESTERDAY=$(date -d yesterday '+%F')
DAY=${2:-$YESTERDAY}
BUCKET=${1}
DIR=/var/lib/docker/proxy/www/logs

if [ -z "$BUCKET" ]
then
  echo 'Usage: $0 <s3 bucket> [date (default yesterday)]'
  exit 1
fi

TODAY=$(date '+%F')

S3=s3://$BUCKET
#echo DAY=$DAY
#echo S3=$S3

lstdir () {
  aws s3 ls $1 | cut -b32-
}

stream () {
        for host in $(lstdir ${S3}/logs/)
        do
          for log in $(lstdir ${S3}/logs/$host$DAY/)
          do
            [[ $log =~ apache.info.proxy-[0-9]{2}-[0-9]{6}.gz ]] && aws s3 cp ${S3}/logs/$host$DAY/$log - | gzip -dc | grep -v '/server-status' | /usr/local/bin/json2combined.py
          done
        done
}

mkdir -p ${DIR}
stream | goaccess --no-progress --log-format=VCOMBINED - > ${DIR}/${DAY}.html
[ "$DAY" == "$TODAY" ] && cp ${DIR}/${DAY}.html ${DIR}/today.html
exit 0
