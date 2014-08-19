#
#   Docker image for executing a celery app
#

FROM ipedrazas/python:2.7

RUN groupadd -r celery && useradd -r -g celery celery

ADD . /code
RUN cd /code; pip install -r requirements.txt


VOLUME  ["/log", "/code"]

EXPOSE  6379

WORKDIR /code

CMD su -p celery -c "/usr/local/bin/celery -A postworker worker --loglevel=info --workdir=/code"


# docker build -t ipedrazas/dotmarks-celery .
# docker run -it --rm --link redis:redis --link mongodb:mongodb -v /var/log/containers/dotmarks-celery:/log ipedrazas/dotmarks-celery
