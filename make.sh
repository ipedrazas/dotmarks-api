#!/bin/bash

TARGET="$1"
SRC="src"
API="deploy/api"
CELERY="deploy/celery"

git pull

if [ "api" == $TARGET ]; then
	echo "Building API"
	cd $API
	DOCKERBUILD="ipedrazas/dotmarks-api"

elif [ "celery" == $TARGET ]; then
	echo "Building Celery"
	cd $CELERY
	DOCKERBUILD="ipedrazas/dotmarks-celery"
else
	echo "please, use celery or api as params"
	exit 0
fi

if [ -d "$SRC" ]; then
	echo ">> Cleaning up"
	rm -rf $SRC
fi

echo ">> Adding source"
cp -r ../../src .

echo ">> Running Docker Build"
docker build -t $DOCKERBUILD .


if [ -d "$SRC" ]; then
	echo ">> Cleaning up"
	rm -rf $SRC
fi
