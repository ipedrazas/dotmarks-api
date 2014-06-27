

dotMarks-api
============

### Self Hosted Bookmarks

Bookmarks? really? this is the thing. I'm lazy... I just wanted one single place to keep them all. I use delicious, Pocket, Kippt. I have bookmarks in my chromes, firefox and different browsers... all over the place. Which is fine. but as I said, I'm lazy, so I've ended up with a very wide amount of links spread between systems.

Every app has its purpouse but I just wanted to have a master copy of all of them. This is dotMarks. A system to keep your bookmarks. It's not going to replace any of the systems you currently use, it's just going to keep all your bookmarks there, you know, just in case you need them.

### Interior design
The system is built using [Eve][1] a Python REST API Framework. A [Nicola Iarocci][2] Project.


## Docker


### MongoDB image


Pull and run Mongodb Image:

    docker run -d -p 27017:27017 --name mongodb dockerfile/mongodb mongod

To run MongoDB with a persistent directory, use:

    mkdir /data/mongod
    docker run -d -p 27017:27017 -v /data/mongodb:/data/db --name mongodb dockerfile/mongodb mongod

This will run a container with mongod and the data will be stored in the directory /data/mongodb in the host. This is, where
the container runs.

To have a mongo console, you can run the following command:

    docker run -it --rm --link mongodb:mongodb dockerfile/mongodb bash -c 'mongo --host $MONGODB_PORT_27017_TCP_ADDR'


### Build dotmarks-api image

First we build our image, from the project folder we execute

    docker build -t dotmarks-api:1 .

Then, to run it, we will have to do

    docker run -it --rm --link mongodb:mongodb -p 5000:5000 dotmarks-api:1


  [1]: http://python-eve.org/
  [2]: https://twitter.com/nicolaiarocci