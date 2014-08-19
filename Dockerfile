############################################################
# Dockerfile to build Python WSGI Application Containers
# Based on Ubuntu
#
# build: docker build -t ipedrazas/dotmarks-api:1 .
# run: docker run -d -p 5000:5000 --link mongodb:mongodb --name dotmarks-api ipedrazas/dotmarks-api:1
# run: docker run -d -p 5000:5000 --link mongodb:mongodb --link redis:redis --name dotmarks-api ipedrazas/dotmarks-api:1
# docker run -d -v /var/sockets:/var/sockets --link mongodb:mongodb --name dotmarks-api ipedrazas/dotmarks-api:1
# docker run -d -v /var/sockets/dotmarks:/var/sockets -v /var/log/containers/dotmarks-api:/var/log \
       --link mongodb:mongodb --link dotmarks:redis --name dotmarks-api ipedrazas/dotmarks-api:1
#
# docker run -a stdin -a stdout -a stderr -i -t ipedrazas/dotmarks-api:1 /bin/bash
############################################################

# Set the base image to Ubuntu
#
# I use ubuntu:14.04 because my host is 14.04
#
FROM ubuntu:14.04

MAINTAINER Ivan Pedrazas <ivan@pedrazas.me>

RUN apt-get update && apt-get install -y build-essential python-setuptools python-pip python-dev


# Add and install Python modules
#ADD config/dotmarks-supervisor.conf /etc/supervisor/conf.d/service.conf
ADD src/requirements.txt /src/requirements.txt
RUN cd /src; pip install -r requirements.txt
RUN mkdir -p /var/sockets

# Bundle app source
ADD src /src

# Expose
EXPOSE  5000

# Run
#CMD /usr/bin/supervisord -n

CMD /usr/local/bin/gunicorn --debug --config /src/gunicorn.conf.py dotmarks:app



