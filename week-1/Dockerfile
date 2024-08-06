FROM python:3.9-slim

RUN apt update && apt install -y wget

WORKDIR /app

COPY ["requirements.txt", "dataset_col_dtypes.py", "etl.env", "etl.py", "."]

RUN pip install -r requirements.txt

ENV DB_USERNAME="" \
	DB_PASSWORD="" \
	DB_HOST="" \
	DB_PORT="" \
	DB_NAME="" \
	URL=""

ENTRYPOINT ["python", "-u", "etl.py"]
# The -u will display the print statements in realtime.