#!/bin/bash

# Go to the backend directory
cd "$(dirname "$0")/.."

# Activate virtual environment
source venv/bin/activate

# Run the seed script
python scripts/seed_db.py
