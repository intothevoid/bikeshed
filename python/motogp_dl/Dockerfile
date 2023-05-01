# Dockerfile to download python environment, install packages in requirements.txt
# and rtorrent binaries
FROM python:3.10-alpine

# Set working directory
WORKDIR /home/rtorrent

# Install rtorrent
RUN apk update
RUN apk add --no-cache rtorrent

# Install python packages
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

# Create user
RUN adduser -D -u 1000 -h /home/rtorrent rtorrent

# Create directories
RUN mkdir -p /home/rtorrent/.rtorrent/session

# Set permissions
RUN chown -R rtorrent:rtorrent /home/rtorrent

# Copy rtorrent config
COPY .rtorrent.rc /home/rtorrent/

# Launch app
COPY app.py /home/rtorrent/
USER rtorrent
CMD ["python", "app.py"]
