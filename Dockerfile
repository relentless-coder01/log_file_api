FROM python:3.9

WORKDIR /log_file_api

COPY ./requirements.txt /log_file_api/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /log_file_api/requirements.txt

COPY ./app /log_file_api/app
