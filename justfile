# Justfile for AWS Lambda Playground
# Commands for managing Python environment and testing Lambda functions

# Default Python interpreter path
python := ".venv/bin/python"


setup:
    #!/usr/bin/env bash
    if [ ! -d ".venv" ]; then
        python3.13 -m venv .venv
    fi
    {{python}} -m pip install --upgrade pip
    {{python}} -m pip install -r requirements.txt
    echo "Setup complete! Virtual environment created and dependencies installed."
# Install Python dependencies
install:
    {{python}} -m pip install --upgrade pip
    {{python}} -m pip install -r requirements.txt

# Copy .env.example to .env if it doesn't exist
setup-env:
    #!/usr/bin/env bash
    if [ ! -f ".env" ]; then
        cp .env.example .env
        echo ".env file created from .env.example"
        echo "Please edit .env and add your AWS credentials"
    else
        echo ".env file already exists"
    fi
