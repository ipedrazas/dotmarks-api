#
#   Docker image for executing a celery app
#

FROM ubuntu:14.04

MAINTAINER Ivan Pedrazas <ivan@pedrazas.me>

RUN apt-get update -y && apt-get install --no-install-recommends -y -q build-essential python2.7 python2.7-dev python-setuptools python-pip git

RUN pip install -U pip && apt-get clean && rm -rf /var/cache/apt/*


RUN groupadd -r celery && useradd -r -g celery celery

ADD src /code
RUN cd /code; pip install -r requirements.txt

VOLUME  ["/log", "/code"]

WORKDIR /code

RUN chown celery.celery /log
USER celery

CMD /usr/local/bin/celery -A workers.postworker worker --loglevel=info --workdir=/code --logfile=/log/%n.log





# docker build -t ipedrazas/dotmarks-celery .



# docker run -d -p 6379:6379 -v /data/redis:/data --name redis dockerfile/redis
# docker run -d -p 27017:27017 -v /data/mongodb:/data/db  --name mongodb dockerfile/mongodb mongod
# docker run -it --rm --link mongodb:mongodb --link redis:redis -v /var/log/containers/dotmarks-celery:/log ipedrazas/dotmarks-celery


# docker run -d --link mongodb:mongodb --link redis:redis -v /var/log/containers/dotmarks-celery:/log ipedrazas/dotmarks-celery
