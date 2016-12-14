#!/bin/bash

## if use custom profile
#AWS_CONFIG_FILE=/root/.aws/config
#AWS_SHARED_CREDENTIALS_FILE=/root/.aws/credentials

target_dir=/var/www/{{ server_name }}
backup_dir=/root/backup
s3_dir={{ s3.dir }}
today=`date '+%Y%m%d'`

dbname={{ rds.dbname }}
dbuser={{ rds.dbuser }}
dbpass={{ rds.dbpass }}
dbhost="{{ rds.dbhost }}"

today_dir=${backup_dir}/${today}

if [ ! -d ${today_dir} ]
then
  mkdir -p ${today_dir}
fi

/usr/bin/mysqldump -u ${dbuser} -p --password=${dbpass} -h ${dbhost} ${dbname} | gzip > ${today_dir}/${dbname}_${today}.sql.gz

## if use custom profile
#aws s3 cp ${today_dir}/ s3://${s3_dir}/${today}/db --recursive --profile s3 > /dev/null
#aws s3 cp ${target_dir} s3://${s3_dir}/${today}/src --recursive --profile s3 > /dev/null

aws s3 cp ${today_dir}/ s3://${s3_dir}/${today}/db --recursive > /dev/null
aws s3 cp ${target_dir} s3://${s3_dir}/${today}/src --recursive > /dev/null

if [ -d ${today_dir} ]
then
  rm -rf ${today_dir}
fi
