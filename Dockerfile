FROM nikolaik/python-nodejs:latest

COPY ./requirements.txt /
COPY ./cortex /
RUN pip install -r requirements.txt
