#!/bin/bash

# Function to activate virtual environment
activate_venv() {
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    echo "Activating virtual environment..."
    source venv/bin/activate
}

# Function to install dependencies
install_dependencies() {
    echo "Installing dependencies..."
    pip install -r requirements.txt
}

# Function to run development server
run() {
    export FLASK_ENV=development
    export FLASK_DEBUG=1
    export FLASK_APP=app/__init__.py
    
    echo "Starting development server..."
    flask run --host=0.0.0.0 --port=3333
}

# Main script
cd "$(dirname "$0")/.."

case "$1" in
    *)
        activate_venv
        install_dependencies
        run
        ;;
esac
