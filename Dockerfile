FROM python:3
ENV PYTHONBUFFERED=1
WORKDIR /code
RUN apt update && apt install -y vim
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
