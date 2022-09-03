FROM python:3.8-alpine

ENV PYTHONUNBUFFERD 1
WORKDIR /django_cms

COPY . /django_cms/

RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers g++ libffi-dev
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt

EXPOSE  8080

CMD python manage.py runserver 0.0.0.0:8080


