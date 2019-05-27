#!/usr/bin/env bash

source ./docker/mysql-client.env
DB_URL="tcp:127.0.0.1:$MASTER_DB_PORT*$MASTER_DB_NAME/$MASTER_DB_USER/$MASTER_DB_PASS" \
    goose -path ./migrations/master_db/ $@
