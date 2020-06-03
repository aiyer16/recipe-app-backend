FROM python:3.8.3-buster
LABEL Akshay Iyer

ENV PYTHONUNBUFFERED 1 

# Install dependencies
COPY ./requirements.txt /requirements.txt
RUN apt-get update
RUN apt-get --assume-yes install postgresql-client
RUN pip install -r requirements.txt 

# Setup directory structure
RUN mkdir /src
WORKDIR /src
COPY ./src/ /src 

# For security reasons, create a new user
# App will run using this user instead of root
RUN adduser --disabled-password guest 
USER guest

