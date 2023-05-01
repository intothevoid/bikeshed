# Dockerfile to download python environment, install packages in requirements.txt
# and rtorrent binaries
# Build stage
FROM python:3.10-alpine
WORKDIR /home/rtorrent
COPY requirements.txt /tmp/
RUN python -m venv /home/rtorrent/venv
ENV PATH="/home/rtorrent/venv/bin:$PATH"
RUN pip install --no-cache-dir -r /tmp/requirements.txt
COPY downloaded.txt .
COPY app.py .

# Package stage
FROM python:3.10.0-alpine3.14
RUN apk add --no-cache rtorrent
RUN adduser -D -h /home/rtorrent rtorrent
RUN mkdir -p /home/rtorrent/.rtorrent/session
RUN chown -R rtorrent:rtorrent /home/rtorrent
COPY .rtorrent.rc /home/rtorrent/
COPY --from=build /home/rtorrent /home/rtorrent
USER rtorrent
CMD ["python", "app.py"]


