FROM python:3.9

# Set working directory
WORKDIR /log_file_api

# Install dependencies
COPY ./requirements.txt /log_file_api/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /log_file_api/requirements.txt

# Copy application code
COPY ./app /log_file_api/app
