#!/bin/bash
#
# Creates images (if necessary)
# Creates containers and run or restart them
#

. .env


echo "Creating network"
docker network create --driver bridge ${NETWORK_NAME}
echo "Done."

echo "Starting cytomine software manager containers."

# -------------------- PostGres --------------------
# If the image does not exit, then creates it
if [[ ! "$(docker images -q ${POSTGRES_IMAGE})" ]]
then
    cd mypostgres
    echo "---------- Buiding postgres image ----------"
    docker build -t ${POSTGRES_IMAGE} . > /dev/null
    echo "---------- postgres image created! ----------"
    cd ..
fi

# Build the container or restart it if it already exists
if [[ "$(docker ps -q -f name=${POSTGRES_CONTAINER})" ]]
then
    docker stop ${POSTGRES_CONTAINER}
    docker start ${POSTGRES_CONTAINER}
else
    docker volume create --name ${POSTGRES_VOLUME} > /dev/null
    docker run --name ${POSTGRES_CONTAINER} \
	   --env-file=.env \
	   -d -p ${POSTGRES_DB_PORT}:${POSTGRES_DB_PORT} \
	   -v ${POSTGRES_VOLUME}:/var/lib/postgresql/data \
	   --network ${NETWORK_NAME} \
	   ${POSTGRES_IMAGE}
fi

# -------------------- RabbitMQ --------------------
# Build the container or restart it if it already exists
if [[ "$(docker ps -q -f name=${RABBITMQ_CONTAINER})" ]]
then
    docker stop ${RABBITMQ_CONTAINER}
    docker start ${RABBITMQ_CONTAINER}
else
    docker volume create --name ${RABBITMQ_VOLUME} > /dev/null
    docker run --name ${RABBITMQ_CONTAINER} \
	   -d -p ${RABBITMQ_PORT}:${RABBITMQ_PORT} \
	   -v ${RABBITMQ_VOLUME}:/var/lib/rabbitmq/data \
	   --network ${NETWORK_NAME} \
	   ${RABBITMQ_IMAGE}
fi

# -------------------- Django app --------------------
# If the image does not exit, then creates it
if [[ ! "$(docker images -q ${DJANGO_IMAGE})" ]]
then
    echo "---------- Buiding Django image ----------"
    # docker build --network=host --build-arg NEW=True -t ${DJANGO_IMAGE} . > /dev/null
    docker build --build-arg NEW=True -t ${DJANGO_IMAGE} -f Dockerfile.django . > /dev/null
    echo "---------- Django image created! ----------"
fi

# # Waiting for postgres to be ready
if [ true = true ]
then
    echo "Waiting for postgres..."
    # while ! nc -z ${POSTGRES_DB_HOST} ${POSTGRES_DB_PORT}; do
    while ! nc -z localhost ${POSTGRES_DB_PORT}; do
      sleep .1
    done
    echo "PostgreSQL started"
fi

# Build the container or restart it if it already exists
if [[ "$(docker ps -q -f name=${DJANGO_CONTAINER})" ]]
then
    docker stop ${DJANGO_CONTAINER}
    docker start ${DJANGO_CONTAINER}
else
    # docker run --name ${DJANGO_CONTAINER} \
    # 	   --env-file=.env \
    # 	   --gpus all \
    # 	   -v /var/run/docker.sock:/var/run/docker.sock \
    # 	   --network=host \
    # 	   -d ${DJANGO_IMAGE}
    docker run --name ${DJANGO_CONTAINER} \
	   --env-file=.env \
	   --gpus all \
	   -v /var/run/docker.sock:/var/run/docker.sock \
	   -d -p ${DJANGO_PORT}:${DJANGO_PORT} \
	   --network ${NETWORK_NAME} \
	   ${DJANGO_IMAGE}
fi

# -------------------- NGINX --------------------
# Build the container or restart it if it already exists
if [[ "$(docker ps -q -f name=${NGINX_CONTAINER})" ]]
then
    docker stop ${NGINX_CONTAINER}
    docker start ${NGINX_CONTAINER}
else
    docker run --name ${NGINX_CONTAINER} \
	   --env-file=.env \
	   -v /home/giussepi/Public/environments/cytomine_software_manager/nginx/templates/development:/etc/nginx/templates \
	   -v /home/giussepi/Public/environments/cytomine_software_manager/cyto_soft_mgr/cyto_soft_mgr/static:/myapp/static \
	   -v /home/giussepi/Public/environments/cytomine_software_manager/nginx/html_error_pages:/myapp/html_error_pages \
	   --network ${NETWORK_NAME} \
	   -d -p ${NGINX_PORT}:${NGINX_PORT} \
	   ${NGINX_IMAGE}
fi

echo "Done."
