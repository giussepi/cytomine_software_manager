#!/bin/bash
#
# Stops all the containers
#

. .env


echo "Stopping cytomine software manager... data will be preserved in databases."

docker stop ${DJANGO_CONTAINER}
docker rm -v ${DJANGO_CONTAINER}

docker stop ${POSTGRES_CONTAINER}
docker rm -v ${POSTGRES_CONTAINER}

docker stop ${RABBITMQ_CONTAINER}
docker rm -v ${RABBITMQ_CONTAINER}

echo "Done."
