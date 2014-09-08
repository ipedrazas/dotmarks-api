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

CID=$(docker ps | grep "$DOCKERBUILD" | awk '{print $1}')
echo $CID

if [ -d "$SRC" ]; then
	echo ">> Cleaning up"
	rm -rf $SRC
fi

echo ">> Adding source"
cp -r ../../src .

echo ">> Running Docker Build"
# docker build -t $DOCKERBUILD .

docker build -t $DOCKERBUILD . | tee /tmp/docker_build_result.log
RESULT=$(cat /tmp/docker_build_result.log | tail -n 1)
if [[ "$RESULT" != *Successfully* ]];
then
  exit -1
fi


if [ -d "$SRC" ]; then
	echo ">> Cleaning up"
	rm -rf $SRC
fi


echo '>> Stopping old container'
if [ "$CID" != "" ];
then
  docker stop $CID
fi

if [ "api" == $TARGET ]; then

	docker run -d -p 5001:5000 --link mongodb:mongodb --link redis:redis \
    	-v /var/log/containers/dotmarks-api:/var/log ipedrazas/dotmarks-api

elif [ "celery" == $TARGET ]; then
	docker run -d --link redis:redis --link mongodb:mongodb \
		-v /var/log/containers/dotmarks-celery:/log ipedrazas/dotmarks-celery

fi