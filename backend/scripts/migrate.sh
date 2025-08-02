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

# Function to create database (only if it doesn't exist)
init_database() {
    DB_PATH="database/db.sqlite"
    if [ ! -f "$DB_PATH" ]; then
        echo "Creating database directory..."
        mkdir -p database
        
        echo "Initializing database..."
        export FLASK_APP=app/__init__.py
        flask shell <<EOF
from app.shared.database import init_db
from app import create_app
app = create_app()
with app.app_context():
    init_db(app)
EOF
        
        echo "Database initialized successfully!"
    else
        echo "Database already exists. Skipping initialization."
    fi
}

# Function to reset database
reset_database() {
    DB_PATH="database/db.sqlite"
    if [ -f "$DB_PATH" ]; then
        echo "Removing existing database..."
        rm "$DB_PATH"
    fi
    init_database
}

# Function to update database schema (non-destructive)
update_database() {
    echo "Applying database updates (non-destructive)..."
    export FLASK_APP=app/__init__.py
    flask shell <<EOF
from app.shared.database import init_db
from app import create_app
app = create_app()
with app.app_context():
    init_db(app)
EOF
    echo "Database update complete."
}

# Main script
cd "$(dirname "$0")/.."

case "$1" in
    "init")
        activate_venv
        install_dependencies
        init_database
        ;;
    "reset")
        activate_venv
        install_dependencies
        reset_database
        ;;
    "update")
        activate_venv
        install_dependencies
        update_database
        ;;
    *)
        echo "Usage: $0 {init|reset|update}"
        echo "  init    - Initialize the database if it doesn't exist"
        echo "  reset   - Reset the database (warning: this will delete all data)"
        echo "  update  - Apply schema updates without deleting data"
        exit 1
        ;;
esac