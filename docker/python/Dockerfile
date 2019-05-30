FROM python:3.6.5-alpine3.7

RUN mkdir /src
ADD requirements.txt /src/requirements.txt
RUN pip install --upgrade pip
#RUN pip install --upgrade setuptools
#RUN apk update && apk add --no-cache --virtual .pynacl_deps build-base libressl-dev postgresql-dev libffi-dev gcc musl-dev python3-dev
RUN pip install -r /src/requirements.txt

