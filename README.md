## Purpose:
Create and setup a python environment using Docker to deploy FastAPI application with Gunicorn and nginx.

## Configuration files:
```
/log_file_api
|-- app
|   |-- main.py
|   |-- ...
|-- requirements.txt
|-- Dockerfile
|-- docker-compose.yml
|-- server_run.sh
```

## Steps
1. Clone github repository

git clone https://github.com/relentless-coder01/log_file_api.git

#### 2. Deployment with Docker
2.1 Install Docker by following the instructions

https://docs.docker.com/engine/install/ubuntu/

2.2 Create Dockerfile

This file contains the configuration for docker. Pulls base image, installs dependencies and runs Gunicorn (Python WSGI server)
```
# Dockerfile
FROM python:3.9

# Set working directory
WORKDIR /log_file_api

# Install dependencies
COPY ./requirements.txt /log_file_api/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /log_file_api/requirements.txt

# Copy application code
COPY ./app /log_file_api/app

```

2.3 Create docker-compose.yaml

```
version: '3.1'
services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
    command: sh -c "gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --reload --bind 0.0.0.0:8000 --chdir app"
    ports:
      - 8000:8000
```

2.4 Build and run your application

```
docker-compose up
```

2.5 Access the API at

http://localhost:8000/api/v1/logs

Note: All the configuration files are included in this repository

#### 3. Deployment without Docker 

3.1 Install git, python
```
apt-get update
apt-get install git
apt-get install python3 python3-venv python3-pip
```

3.2 Navigate to project directory
```
cd home\log_file_api
```

3.3 Run server with file: server_run.sh
```
server_run.sh

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install modules
pip install -r requirements.txt

# Run Gunicorn with uvicorn
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --reload --bind 0.0.0.0:8000 --chdir app

```

#### 4. Documentation:

* API Specifications: https://github.com/relentless-coder01/log_file_api/blob/main/docs/Log%20File%20API%20Specification.docx

* Test Cases: 
```
Unit Tests:
pytest /app/tests.py

Postman:
/postman/Log File API.postman_collection.json
```

* Design
[![API docs](docs/Sequence_Diagram.png)](https://github.com/relentless-coder01/log_file_api/blob/main/docs/Sequence_Diagram.png)

10. UI

Interact with the API using the UI: http://localhost:8000/static/index.html

![Alt text](https://github.com/relentless-coder01/log_file_api/blob/main/images/ui_page1.jpg)

![Alt text](https://github.com/relentless-coder01/log_file_api/blob/main/images/ui_page2.jpg)

