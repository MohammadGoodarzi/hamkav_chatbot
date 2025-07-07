#!/bin/bash

# Define the directory name
DIR="app/logs"

# Create the directory if it does not exist
mkdir -p "$DIR"
echo "directory '$DIR' has been created/already exist successfuly."

# Cretae db tables
source venv/bin/activate
python app/init_db.py

# Running

uvicorn app.main:app --reload