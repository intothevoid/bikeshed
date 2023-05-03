#!/bin/bash

if ! [ -e $HOME/.cache/aria2/dht.dat ]; then
  # hide false error: Exception caught while loading DHT routing table
  # https://github.com/aria2/aria2/issues/1253
  # based on aria2/src/DHTRoutingTableDeserializer.cc
  hex=""
  hex+="a1 a2" # 0+2: magic
  hex+="02" # 2+1: format
  hex+="00 00 00" # 3+3
  hex+="00 03" # 6+2: version
  hex+=$(printf "%016x\n" $(date --utc +%s)) # 8+8: time
  hex+="00 00 00 00 00 00 00 00" # 16+8: localnode
  hex+=$(dd if=/dev/random bs=1 count=40 status=none | sha1sum - | cut -c1-40) # 24+20: localnode ID
  hex+="00 00 00 00" # 44+4: reserved
  hex+="00 00 00 00" # 48+4: num_nodes uint32_t
  hex+="00 00 00 00" # 52+4: reserved
  # 56 bytes
  mkdir -p $HOME/.cache/aria2
  echo $hex | xxd -r -p >$HOME/.cache/aria2/dht.dat
fi