FROM python:3.8-alpine

ENV PYTHONUNBUFFERD 1
WORKDIR /django_cms
#ADD . /django_cms
COPY . /django_cms/
#COPY ./requirements_origin.txt /django_cms/requirements_origin.txt
# packages for uwisg module
RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers g++ libffi-dev
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt
#EXPOSE 5000
#RUN apk del .tmp
CMD python manage.py runserver 0.0.0.0:8000


