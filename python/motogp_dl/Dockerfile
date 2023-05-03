# Dockerfile to download python environment, install packages in requirements.txt
# and rtorrent binaries
FROM python:3.10-alpine

# Install rtorrent
RUN apk update
RUN apk add --no-cache aria2

# Install python packages
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

# Launch app
COPY app.py .
CMD ["python", "app.py"]
