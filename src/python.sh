#!/usr/bin/env bash

while read line
do
  if [ "$line" != "" ] ; then
    export $line
  fi
done < ../docker/mysql-client.env

PYTHONPATH=$(pwd) MASTER_DB_HOST=127.0.0.1 python $@
