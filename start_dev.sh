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
	   -v ${DJANGO_STATIC_VOLUME}:/myapp/cyto_soft_mgr/cyto_soft_mgr/static \
	   -d -p ${DJANGO_PORT}:${DJANGO_PORT} \
	   --network ${NETWORK_NAME} \
	   ${DJANGO_IMAGE}
fi

# -------------------- NGINX --------------------
# If the image does not exit, then creates it
if [[ ! "$(docker images -q ${NGINX_IMAGE})" ]]
then
    cd nginx
    echo "---------- Buiding Nginx image ----------"
    docker build -t ${NGINX_IMAGE} . > /dev/null
    echo "---------- Nginx image created! ----------"
    cd ..
fi

# Build the container or restart it if it already exists
if [[ "$(docker ps -q -f name=${NGINX_CONTAINER})" ]]
then
    docker stop ${NGINX_CONTAINER}
    docker start ${NGINX_CONTAINER}
else
    docker volume create --name ${NGINX_VOLUME} > /dev/null
    docker run --name ${NGINX_CONTAINER} \
	   --env-file=.env \
	   -v `pwd`/nginx/templates/development:/etc/nginx/templates \
	   -v `pwd`/nginx/html_error_pages:/myapp/html_error_pages \
	   -v ${DJANGO_STATIC_VOLUME}:/myapp/cyto_soft_mgr/cyto_soft_mgr/static \
    	   -v ${NGINX_VOLUME}:/var/log/nginx \
	   --network ${NETWORK_NAME} \
	   -d -p ${NGINX_PORT}:${NGINX_PORT} \
	   ${NGINX_IMAGE}
fi

echo "Done."
