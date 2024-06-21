# Pull updates
sudo apt-get update
# Install python
sudo apt-get install python3 python3-pip python3-venv
# Install git
sudo apt-get install git
# Give "Y" to any prompts that follow

# Navidate inside unix home/ directory
cd home

#Clone github repository
git clone https://github.com/relentless-coder01/log_file_api.git

# Navigate to project directory
cd log_file_api

# Create a virtual environment
python3 -m venv .venv

# Activate
source .venv/bin/activate

# Install python modules
pip install -r requirements.txt

# Run Test server
cd app
python3 local_run.py

# Test from within the server
sudo apt-get install curl
curl -X GET "http://localhost:8000/api/v1/logs?filename=file1.log"

# Access the server from your machine using the host server ip
host_ip:8000/api/v1/logs

# Access the UI
host_ip:8000/static/index.html

# If there is any problem, make sure you are exposing the port 8000 from your unix machine
sudo ufw allow 8000/tcp
