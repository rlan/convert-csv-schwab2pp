FROM python:3.10.8-slim-buster

RUN mkdir /app
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY convert.py convert.py
ENTRYPOINT ["python", "convert.py"]
