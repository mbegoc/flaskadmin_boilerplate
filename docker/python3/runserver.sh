#!/bin/bash

source /home/python/venv/bin/activate

cd /home/python/flask_bootstrap/

pip install -r /home/python/flask_bootstrap/requirements.txt
python flask_demo/main.py runserver
