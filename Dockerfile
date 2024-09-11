FROM python:3.10-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install make

COPY requirements.txt requirements.txt

RUN apt-get update && \
    python -m pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

ENTRYPOINT [ "python", "bot.py" ]