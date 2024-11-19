#!/bin/bash

# Move to file's dir
script_dir=$(dirname "$0")
cd $script_dir

# Activating venv
source .venv/bin/activate

# Runs the script
python -B start.py

# Deactivates the venv
deactivate