FROM python:3-alpine

label maintainer="Hamed Ahmadi<ahmadihamed167@gmail.com>"

ENV PYTHONUNBUFFERED 1

COPY ./requirements /requirements 
COPY ./src  /src

RUN apk add --update --no-cache postgresql-client
RUN pip install -U pip 
RUN apk add --update --no-cache --virtual .temp_depend \
        gcc libc-dev linux-headers  postgresql-dev
RUN pip install -r /requirements/base.txt
RUN apk del .temp_depend

RUN adduser -D user 

WORKDIR /src 

USER  user 

