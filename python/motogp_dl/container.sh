#!/bin/bash

# Once you have built the docker image, this script can be used to run the container.
# The container mounts the /home/rtorrent/downloads directory to the host's /volume1/downloads directory.
# The container restarts automatically unless stopped manually.
# The name of the container is motogp_dl

docker run -d \
  --name motogp-dl \
  --restart unless-stopped \
  -v /volume1/downloads:/home/rtorrent/downloads \
  motogp_dl:latest
