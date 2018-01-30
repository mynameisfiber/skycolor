FROM python:3.6-slim
MAINTAINER Micha Gorelick <mynameisfiber>

WORKDIR /usr/local/app/
COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 5000
CMD python skycolor.py
