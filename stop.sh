#!/bin/bash
#
# Stops all the containers
#

. .env


echo "Stopping cytomine software manager... data will be preserved in databases."

if [[ "$(docker ps -q -f name=${DJANGO_CONTAINER})" ]]
then
    docker stop ${DJANGO_CONTAINER}
fi
docker rm -v ${DJANGO_CONTAINER}

if [[ "$(docker ps -q -f name=${GUNICORN_CONTAINER})" ]]
then
    docker stop ${GUNICORN_CONTAINER}
fi
docker rm -v ${GUNICORN_CONTAINER}

docker stop ${POSTGRES_CONTAINER}
docker rm -v ${POSTGRES_CONTAINER}

docker stop ${RABBITMQ_CONTAINER}
docker rm -v ${RABBITMQ_CONTAINER}

docker stop ${NGINX_CONTAINER}
docker rm -v ${NGINX_CONTAINER}

echo "Done."

echo "Removing network"
docker network rm ${NETWORK_NAME}

echo "Done."
