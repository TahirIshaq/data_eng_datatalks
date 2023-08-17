# Task

Make a docker image using python:3.9 as the base image. It should contain pandas and python shell should run on container creation.

Build docker image:

`docker build -t pandas:v01 .`

Run docker container:

`docker run -it pandas:v01`