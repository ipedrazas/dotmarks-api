#!/bin/bash


set -e

export LC_ALL=C

TS=$( date --utc '+%Y-%m-%dT%H:%M:%SZ' )

BACKUP_DIR="/data/backup/${TS}"

docker run -it --rm --link mongodb:mongodb -v /data/mongodb:/data dockerfile/mongodb bash -c 'mongodump --out '${BACKUP_DIR}' --host $MONGODB_PORT_27017_TCP_ADDR'
