FROM python:3.7-alpine
MAINTAINER Qingyuan:qm28@georgetown.edu

ENV PYTHONBUFFERED 1

COPY ./requiremens.txt /requiremens.txt
RUN pip install -r /requiremens.txt

RUN mkdir /app
WORKDIR /app
COPY ./ /app

RUN adduser -D user
USER user

