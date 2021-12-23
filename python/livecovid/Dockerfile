FROM python:3.10

WORKDIR /appascovidwatch

COPY requirements.txt .
COPY main.py .
COPY index.html .
COPY ./scrapers/ ./scrapers
COPY ./static/ ./static

RUN pip install -r requirements.txt

CMD ["python3", "./main.py"]