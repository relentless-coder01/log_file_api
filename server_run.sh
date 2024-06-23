#!/bin/bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --reload --bind 0.0.0.0:8000 --chdir app