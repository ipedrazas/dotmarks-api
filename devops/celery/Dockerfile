#
#   Docker image for executing a celery app
#

FROM ubuntu:14.04

MAINTAINER Ivan Pedrazas <ivan@pedrazas.me>

RUN apt-get update -y && apt-get install --no-install-recommends -y -q build-essential python2.7 python2.7-dev python-pip git mercurial

RUN pip install -U pip

RUN apt-get clean && rm -rf /var/cache/apt/*


RUN groupadd -r celery && useradd -r -g celery celery

ADD ../../src /code
RUN cd /code; pip install -r requirements.txt


VOLUME  ["/log", "/code"]

WORKDIR /code

CMD su -p celery -c "/usr/local/bin/celery -A workers.postworker worker --loglevel=info --workdir=/code"


# docker build -t ipedrazas/dotmarks-celery .
# docker run -it --rm --link mongodb:mongodb -v /var/log/containers/dotmarks-celery:/log ipedrazas/dotmarks-celery
