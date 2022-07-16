FROM python:3.8-alpine

ENV PYTHONUNBUFFERD 1
WORKDIR /django_cms
#ADD . /django_cms
COPY . /django_cms/
#COPY ./requirements.txt /django_cms/requirements.txt
# packages for uwisg module
RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers
RUN pip install -r requirements.txt
#EXPOSE 5000
#RUN apk del .tmp


