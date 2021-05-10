FROM python:3.8-alpine

ENV PATH="/scripts:${PATH}"

COPY ./django_cms/requirements.txt /requirements.txt
# packages for uwisg module
RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers
RUN pip install -r /requirements.txt
RUN apk del .tmp

RUN mkdir /django_cms
COPY ./django_cms/django_cms /django_cms
COPY ./django_cms/home /django_cms
COPY ./django_cms/UserManagement /django_cms
WORKDIR /django_cms
COPY ./django_cms/scripts /scripts

RUN chmod +x /scripts/*

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

# create a user for the app
RUN adduser -D user
RUN chown -R user:user /vol
RUN chmod -R 755 /vol/web
USER user

CMD ["entrypoint.sh"]
