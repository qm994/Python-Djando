FROM python:3.7-alphine
MAINTAINER qINGYUAN

ENV PYTHONBUFFERED 1

COPY ./requiremens.txt /requiremens.txt
RUN pip install -r /requiremens.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user

