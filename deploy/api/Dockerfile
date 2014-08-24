############################################################
# Dockerfile to build Python WSGI Application Containers
# Based on Ubuntu
#
# build: docker build -t ipedrazas/dotmarks-api:2 .
# run: docker run -d -p 5001:5000 --link mongodb:mongodb --link redis:redis --name dotmarks-api ipedrazas/dotmarks-api
#
# docker run -d -p 6379:6379 -v /data/redis:/data --name redis dockerfile/redis
# docker run -d -p 27017:27017 -v /data/mongodb:/data/db  --name mongodb dockerfile/mongodb mongod
# docker run -d -v /var/sockets/dotmarks:/var/sockets -v /var/log/containers/dotmarks-api:/var/log \
#       --link mongodb:mongodb --link redis:redis --name dotmarks-api ipedrazas/dotmarks-api
#
############################################################

# Set the base image to Ubuntu
#
# I use ubuntu:14.04 because my host is 14.04
#
FROM ubuntu:14.04

MAINTAINER Ivan Pedrazas <ivan@pedrazas.me>

RUN apt-get update && apt-get install -y build-essential python-setuptools python-pip python-dev


# Bundle app source
ADD src /src

RUN cd /src; pip install -r requirements.txt
RUN mkdir -p /var/sockets


# Expose
EXPOSE  5000

WORKDIR /src

# exec /usr/local/bin/gunicorn api.wsgi -w 1 -b 0.0.0.0:8005 --log-level=debug

#CMD /usr/local/bin/gunicorn --config gunicorn.conf.py  dotmarks:app
#CMD /usr/local/bin/gunicorn --config gunicorn.conf.py  dotmarks:app
CMD /usr/local/bin/gunicorn -w 4 -b 0.0.0.0:5000  dotmarks:app