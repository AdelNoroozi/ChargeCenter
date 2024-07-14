FROM python:3.9.9-slim

ADD requirements/ requirements/
RUN pip install -r requirements/production.txt

RUN mkdir /app
WORKDIR /app
ADD ./ /app/