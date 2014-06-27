

#dotMarks-api -- Self Hosted Bookmarks

dotMarks is a lightweight AngularJs client, a REST API, and a Google Chrome extension that allows you to manage your bookmarks.

### An API to rule them all!
The dotMarks REST API is built using [Eve][1] a Python REST API Framework. A [Nicola Iarocci][2] Project.


### Docker

The easiest way of running dotMarks is by launching [Docker][3] containers. To install Docker, go to [docker.com][4] and follow the instructions.

You can run docker in Linux, OSX and Windows.

### MongoDB image


Pull and run Mongodb Image:

    docker run -d -p 27017:27017 --name mongodb dockerfile/mongodb mongod

To run MongoDB with a persistent directory, use:

    mkdir /data/mongod
    docker run -d -p 27017:27017 -v /data/mongodb:/data/db \
        --name mongodb dockerfile/mongodb mongod

This will run a container with mongod and the data will be stored in the directory /data/mongodb in the host. This is, where
the container runs.

To have a mongo console, you can run the following command:

    docker run -it --rm --link mongodb:mongodb \
        dockerfile/mongodb bash -c 'mongo --host $MONGODB_PORT_27017_TCP_ADDR'


### Build dotmarks-api image

First we build our image, from the project folder we execute

    docker build -t dotmarks-api:1 .

Then, to run it, we will have to do

    docker run -it --rm --link mongodb:mongodb -p 5000:5000 dotmarks-api:1


If you want to run it as a daemon or dettached, use the following command

    docker run -d -p 5000:5000 --rm --link mongodb:mongodb  --name dotmarks-api dotmarks-api:1


  [1]: http://python-eve.org/
  [2]: https://twitter.com/nicolaiarocci
  [3]: http://www.docker.com/
  [4]: https://docs.docker.com/installation/#installation