#!/bin/bash

# Once you have built the docker image, this script can be used to run the container.
# This command will create a Docker container with the image 'motogp-dl' and name the container 'motogp-dl'. 
# It will restart the container unless stopped and will also expose port 6911. 
# It also creates a volume to store any downloads in the current directory.

# create downloads directory if it doesn't exist, give it write permissions with existing user and group
mkdir -p ./downloads
chmod 777 ./downloads

# run the container
docker run -d \
  --name motogp-dl \
  --restart unless-stopped \
  -p 6911:6911 -p 6881-6885:6881-6885 \
  -v ./downloads:/downloads \
  motogp-dl:latest