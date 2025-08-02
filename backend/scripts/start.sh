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
run_dev() {
    export FLASK_ENV=development
    export FLASK_DEBUG=1
    export FLASK_APP=app/__init__.py
    
    echo "Starting development server..."
    flask run --host=0.0.0.0 --port=3333
}

# Function to run production server
run_prod() {
    export FLASK_ENV=production
    export FLASK_DEBUG=0
    export FLASK_APP=app/__init__.py
    
    echo "Starting production server with gunicorn..."
    pip install gunicorn
    gunicorn -w 4 -b 0.0.0.0:3333 'app:create_app()'
}

# Main script
cd "$(dirname "$0")/.."

case "$1" in
    "dev")
        activate_venv
        install_dependencies
        run_dev
        ;;
    "prod")
        activate_venv
        install_dependencies
        run_prod
        ;;
    *)
        echo "Usage: $0 {dev|prod}"
        exit 1
        ;;
esac
