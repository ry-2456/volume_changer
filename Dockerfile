FROM python:3
ENV PYTHONBUFFERED=1
WORKDIR /code
RUN apt update && apt install -y vim libsndfile1 sox ffmpeg mediainfo
# libsndfile1 for soundfile
# sox ffmpeg mediainfo for audiofile
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
