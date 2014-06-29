############################################################
# Dockerfile to build Python WSGI Application Containers
# Based on Ubuntu
############################################################

# Set the base image to Ubuntu
FROM ubuntu

MAINTAINER Ivan Pedrazas <ivan@pedrazas.me>

RUN apt-get update && apt-get install -y build-essential python-setuptools python-pip python-dev


# Add and install Python modules
ADD src/requirements.txt /src/requirements.txt
RUN cd /src; pip install -r requirements.txt

# Bundle app source
ADD src /src

# Expose
EXPOSE  5000

# Run
CMD ["python", "/src/dotmarks.py"]
