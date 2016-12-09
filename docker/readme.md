Read Me
=======

First install docker. You may have to add your user to the docker group in
order to be able to connect to the docker service.

Once it's installed, run the init_docker.sh command. It will build the python2
image and run the graffmap within it.

The first launch may be a little long since pip requirements and db migrates
are run. Subsequent launches will be faster. The container 8000 port is mapped
to the host 80 port, so the app is available through http://localhost or
through the machine IP.
