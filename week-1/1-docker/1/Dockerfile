# Create a python image that has pandas library installed.
# Python console is opened upon the creation of a container from the image.
# To create an image: docker build -t pandas:v01 .
# To create a container: docker run pandas:v01

FROM python:3.9

RUN pip install pandas

ENTRYPOINT ["python"]