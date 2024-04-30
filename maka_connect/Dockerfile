# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.12.2

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# create root directory for our project in the container
RUN mkdir /maka_rest_api

# Set the working directory to /music_service
WORKDIR /maka_rest_api

# Copy the current directory contents into the container at /music_service
ADD . /maka_rest_api/
COPY requirements.txt /maka_rest_api/
# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt
COPY . /maka_rest_api/

RUN pip install -U channels["daphne"]

EXPOSE 4500
RUN daphne -b 0.0.0.0 -p 4500 maka_connect.asgi:application