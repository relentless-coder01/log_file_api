## Purpose:
Create and setup a python environment using Docker to deploy FastAPI application with Gunicorn and nginx.

## Configuration files:
```
/log_file_api
|-- app
|   |-- main.py
|   |-- ...
|
|-- nginx
|   |-- nginx.conf
|
|-- requirements.txt
|-- Dockerfile
|-- docker-compose.yml
```

## Steps
1. Clone github repository

git clone https://github.com/relentless-coder01/log_file_api.git

2. Install Docker by following the instructions

https://docs.docker.com/engine/install/ubuntu/

3. Create Dockerfile

This file contains the configuration for docker. Pulls base image, installs dependencies and runs Gunicorn (Python WSGI server)

4. Create nginx.conf

Create a file nginx/nginx.conf. Nginx is the web server / reverse proxy.

6. Create docker-compose.yaml

This file builds the docker image.

7. Navigate to the project diretory. Build and run your application

```
docker-compose up -d --build
```
Note: All the configuration files are included in this repository
