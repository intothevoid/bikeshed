#!/bin/bash

# Once you have built the docker image, this script can be used to run the container.
# This command will create a Docker container with the image 'motogp-dl' and name the container 'motogp-dl'. 
# It will restart the container unless stopped and will also expose port 6911. 
# It also creates a volume to store any downloads in the current directory.

# run the container
docker run -d -it \
  --name motogp-dl \
  --restart unless-stopped \
  -p 6911:6911 -p 6881-6885:6881-6885 \
  -v /volume1/downloads:/downloads \
  --env-file=./scripts/config.env \
  motogp-dl:latest