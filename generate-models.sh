#!/usr/bin/env bash

source ./docker/mysql-client.env
sqlacodegen "mysql://$MASTER_DB_USER:$MASTER_DB_PASS@127.0.0.1:$MASTER_DB_PORT/$MASTER_DB_NAME" > ./src/models/master_models_generated.py
#sqlacodegen "mysql://$RAW_DB_USER:$RAW_DB_PASS@127.0.0.1:$RAW_DB_PORT/$RAW_DB_NAME" > ./src/models/raw_models_generated.py
