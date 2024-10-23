FROM python:3.9

RUN pip install mysql-connector-python

RUN pip install faker

WORKDIR /usr/app/src

COPY fakedata_generator.py ./