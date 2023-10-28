# This file is a template, and might need editing before it works on your project.
FROM python:3.7.9-slim-stretch
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

RUN ln -fs /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN dpkg-reconfigure -f noninteractive tzdata

COPY sources.list /etc/apt/sources.list
COPY . /usr/src/app/search_api_development
WORKDIR /usr/src/app/search_api_development

RUN mkdir /data
RUN mkdir /data/logs

RUN pip install --no-cache -r  requirements.txt

ENV FLASK_APP=app.py
ENV PYTHONPATH=/usr/src/app/search_api_development
ENV APP_NAME=search-api-development

EXPOSE ${APP_PORT}

CMD gunicorn -w 4 -k gevent --timeout 600 -b 0.0.0.0:${APP_PORT} app:app

