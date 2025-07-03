# WinCC V8 API Documentation Server

This project provides a web server to serve Swagger UI and API documentation from a `winccv8.yaml` OpenAPI specification file.

## Features

- Serves Swagger UI for interactive API documentation
- Provides endpoints to download the API spec in JSON and YAML formats
- Health check endpoint

## Requirements

- Python 3.7+
- `pip` (Python package manager)

## Installation

1. Clone or download this repository.
2. Ensure your `winccv8.yaml` file is in the project directory.
3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

Start the server with:

```bash
python winccv8.py