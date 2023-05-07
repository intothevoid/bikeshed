# Dockerfile to download python environment, install packages in requirements.txt
# and rtorrent binaries
FROM python:3.10-alpine

# Install rtorrent
RUN apk update
RUN apk add --no-cache aria2 gcc python3-dev musl-dev linux-headers

# Copy contents
COPY . .

# Install python packages
RUN pip install -r /requirements.txt

# Copy dht.dat file to avoid errors in docker container
# like [ERROR] Exception caught while loading DHT routing table from /root/.cache/aria2/dht.dat
COPY resources/dht.dat /root/.cache/aria2/dht.dat

# Launch motogp-dl
CMD ["python", "motogp_dl.py"]
