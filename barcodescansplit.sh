#!/bin/bash

set -e

# Move to file's dir
script_dir=$(dirname "$0")
cd $script_dir

# Default values
PROCESSES=$(nproc)  # Default to the number of CPU threads
MODE=""
SOURCE=""
DESTINATION=""
BACKUP=""
LOG=""
TEMP=""
IMAGE=""

# Function to display usage
display_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo
    echo "Options:"
    echo "  -s, --source       Directory containing PDF files."
    echo "  -d, --destination  Directory to store output files."
    echo "  -b, --backup       Directory to store backup files."
    echo "  -l, --log          Directory to store log files."
    echo "  -t, --temp         Temporary directory to store split files."
    echo "  -i, --image        Temporary directory to store images."
    echo "  -m, --mode         Processing mode (single or multi)."
    echo "  -p, --processes    Maximum number of processes to run (default: number of CPU threads)."
    echo
    echo "Example: $0 -s /path/to/source -d /path/to/dest -m multi -p 4"
    exit 1
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        -s|--source)
            SOURCE="$2"
            shift 2
            ;;
        -d|--destination)
            DESTINATION="$2"
            shift 2
            ;;
        -b|--backup)
            BACKUP="$2"
            shift 2
            ;;
        -l|--log)
            LOG="$2"
            shift 2
            ;;
        -t|--temp)
            TEMP="$2"
            shift 2
            ;;
        -i|--image)
            IMAGE="$2"
            shift 2
            ;;
        -m|--mode)
            MODE="$2"
            shift 2
            ;;
        -p|--processes)
            PROCESSES="$2"
            shift 2
            ;;
        -h|--help)
            display_usage
            ;;
        *)
            echo "Unknown option: $1"
            display_usage
            ;;
    esac
done

# Validate required arguments
if [[ -z "$SOURCE" || -z "$DESTINATION" || -z "$MODE" ]]; then
    echo "Error: -s/--source, -d/--destination, and -m/--mode are required."
    display_usage
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Please install Python3 and try again."
    exit 1
fi

echo "Python3 is installed."

# Create a virtual environment if not found
if [[ ! -d ".venv" ]]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    echo "Virtual environment created."
    source .venv/bin/activate
    pip install -r requirements.txt
else
    echo "Virtual environment already exists."
    source .venv/bin/activate
fi

# Run the script
python -B splitter.py -s "$SOURCE" -d "$DESTINATION" -b "$BACKUP" -l "$LOG" -t "$TEMP" -i "$IMAGE" -m "$MODE" -p "$PROCESSES"