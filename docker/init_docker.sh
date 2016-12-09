#!/bin/bash

# build the docker image to use to run the project
docker build -t flask_bootstrap-python3:latest --rm python3

PROJECT_DIR=$(realpath ..)

if [ ! "`docker ps | grep flask_bootstrap_postgres`" ]; then
    if [ "`docker ps -a | grep flask_bootstrap_postgres`" ]; then
        docker start flask_bootstrap_postgres
    else
        docker run -d -v /var/lib/postgres \
            -e POSTGRES_DB=flask_bootstrap \
            -e POSTGRES_USER=flask_bootstrap \
            -e POSTGRES_PASSWORD=flask_bootstrap \
            --name flask_bootstrap_postgres \
            postgres:9.5
    fi
fi

# make node build assets
# if [ ! "`docker ps | grep flask_node`" ]; then
#     if [ "`docker ps -a | grep flask_node`" ]; then
#         docker start flask_node
#     else
#         docker run -v $PROJECT_DIR/flask/client/:/home/node/flask/ \
#                    -d --name flask_node flask-nodejs
#     fi
# fi

# python server
if [ ! "`docker ps | grep flask_bootstrap_python`" ]; then
    if [ "`docker ps -a | grep flask_bootstrap_python`" ]; then
        docker start -ai flask_bootstrap_python
    else
        docker run -p 5000:5000 -v $PROJECT_DIR:/home/python/flask_bootstrap/ \
                   -e DATABASE_HOST=flask_bootstrap_postgres \
                   -e DATABASE_USER=flask_bootstrap \
                   -e DATABASE_NAME=flask_bootstrap \
                   -e DATABASE_PASSWORD=flask_bootstrap \
                   --link flask_bootstrap_postgres \
                   --hostname flask-bootstrap.dev \
                   --name flask_bootstrap_python \
                   -it flask_bootstrap-python3
    fi
fi
