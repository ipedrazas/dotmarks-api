############################################################
# Dockerfile to build Python WSGI Application Containers
# Based on Ubuntu
#
# build: docker build -t ipedrazas/dotmarks-api:2 .
# run: docker run -d -p 5000:5000 --link mongodb:mongodb --name dotmarks-api ipedrazas/dotmarks-api:1
# run: docker run -d -p 5001:5000 --link mongodb:mongodb --link redis:redis --name dotmarks-api2 ipedrazas/dotmarks-api:2
#
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

#CMD python dotmarks.py

# exec /usr/local/bin/gunicorn api.wsgi -w 1 -b 0.0.0.0:8005 --log-level=debug

CMD /usr/local/bin/gunicorn --config /src/gunicorn.conf.py  dotmarks:app
