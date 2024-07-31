#!/bin/bash


# Container name
container_name=$1
command=$2


# Run a Bash shell inside the container
docker exec -it $container_name $command

# ./container-command.sh botify_api_1 "python manage.py startapp customusers"
# ./container-command.sh botify-api-1 "python manage.py startapp customusers"
# CURRENT_UID=$(id -u):$(id -g) docker-compose up
# ./container-command.sh botify_api_1 "sh"

