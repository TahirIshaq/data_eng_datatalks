FROM python:3.9

RUN apt-get install wget gzip
RUN pip install pandas psycopg2 sqlalchemy

WORKDIR /app

COPY pipeline.py pipeline.py

ENTRYPOINT ["python", "pipeline.py"]