FROM python:3-alpine

label maintainer="Hamed Ahmadi<ahmadihamed167@gmail.com>"

ENV PYTHONUNBUFFERED 1

COPY ./requirements /requirements 
COPY ./src  /src

RUN pip install -U pip 
RUN pip install -r /requirements/base.txt

RUN adduser -D user 

WORKDIR /src 

USER  user 

