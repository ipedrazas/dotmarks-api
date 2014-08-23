#!/bin/bash

TARGET="$1"
SRC="src"
API="deploy/api"
CELERY="deploy/celery"

if [ "api" == $TARGET ]; then
	echo "Building API"
	cd $API

elif [ "celery" == $TARGET ]; then
	echo "Building Celery"
	cd $CELERY
else
	echo "please, use celery or api as params"
	exit 0
fi

echo ">> Cleaning up"
if [ -d "$SRC" ]; then
	rm -rf $SRC
fi

echo ">> Adding source"
cp -r ../../src .

echo ">> Running Docker Build"
docker build -t ipedrazas/dotmarks-api . | tee /tmp/docker_build_result.log
RESULT=$(cat /tmp/docker_build_result.log | tail -n 1)
if [[ "$RESULT" != *Successfully* ]];
then
	exit -1
fi



