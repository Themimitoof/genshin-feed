FROM python:3.11-alpine

RUN apk add hugo && pip install poetry

COPY . /app
WORKDIR /app

RUN poetry install && chmod 655 build-website.sh

CMD sh /app/build-website.sh
