FROM python:3.8.2-alpine

COPY . /hidden_service/

WORKDIR /hidden_service

RUN apk update && apk add build-base gcc make tor
RUN pip3 install -r requirements.txt

CMD python3 hidden_service.py