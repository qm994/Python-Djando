FROM python:3.7-alpine
MAINTAINER Qingyuan:qm28@georgetown.edu

ENV PYTHONBUFFERED 1

COPY ./requiremens.txt /requiremens.txt
RUN apk add --update --no-cache postgresql-client
# these are temp dependencies for insyalling pkgs in requirements.txt
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev

RUN pip install -r /requiremens.txt
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./ /app

RUN adduser -D user
USER user

