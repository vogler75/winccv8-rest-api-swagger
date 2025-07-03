#!/usr/bin/env python3
"""
Swagger Documentation Web Server
Serves Swagger UI documentation from winccv8.yaml file
"""

from flask import Flask, jsonify, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
import yaml
import os
import sys

# Initialize Flask app
app = Flask(__name__)

# Configuration
SWAGGER_URL = '/swagger'  # URL for exposing Swagger UI
API_URL = '/api/docs'  # URL for the API documentation (JSON)
YAML_FILE = 'winccv8.yaml'  # Path to your YAML file


def load_swagger_spec():
    """Load and parse the YAML specification file"""
    try:
        if not os.path.exists(YAML_FILE):
            raise FileNotFoundError(f"YAML file '{YAML_FILE}' not found in current directory")

        with open(YAML_FILE, 'r', encoding='utf-8') as file:
            spec = yaml.safe_load(file)

        return spec
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading YAML file: {e}")
        sys.exit(1)


# Load the Swagger specification
swagger_spec = load_swagger_spec()

# Create Swagger UI blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "WinCC V8 API Documentation",
        'dom_id': '#swagger-ui',
        'url_prefix': SWAGGER_URL,
        'layout': 'BaseLayout',
        'deepLinking': True,
        'showExtensions': True,
        'showCommonExtensions': True
    }
)

# Register blueprint
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


@app.route('/api/docs')
def get_docs():
    """Serve the API documentation as JSON"""
    return jsonify(swagger_spec)


@app.route('/api/docs/yaml')
def get_yaml():
    """Serve the original YAML file"""
    try:
        return send_from_directory('.', YAML_FILE, as_attachment=False, mimetype='text/yaml')
    except FileNotFoundError:
        return jsonify({'error': 'YAML file not found'}), 404


@app.route('/')
def home():
    """Redirect to Swagger UI"""
    return f'''
    <html>
    <head>
        <title>WinCC V8 API Documentation</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .container {{ max-width: 600px; margin: 0 auto; text-align: center; }}
            .button {{ 
                display: inline-block; 
                padding: 10px 20px; 
                margin: 10px; 
                background-color: #007bff; 
                color: white; 
                text-decoration: none; 
                border-radius: 5px; 
            }}
            .button:hover {{ background-color: #0056b3; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>WinCC V8 API Documentation Server</h1>
            <p>Welcome to the WinCC V8 API documentation server.</p>
            <p>
                <a href="{SWAGGER_URL}" class="button">View Swagger UI</a>
                <a href="/api/docs" class="button">View JSON Spec</a>
                <a href="/api/docs/yaml" class="button">View YAML Spec</a>
            </p>
        </div>
    </body>
    </html>
    '''


@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'yaml_file': YAML_FILE,
        'yaml_exists': os.path.exists(YAML_FILE)
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Check if YAML file exists before starting
    if not os.path.exists(YAML_FILE):
        print(f"Error: YAML file '{YAML_FILE}' not found in current directory")
        print("Please ensure the file exists before starting the server")
        sys.exit(1)

    print(f"Starting Swagger Documentation Server...")
    print(f"Loading documentation from: {YAML_FILE}")
    print(f"Swagger UI will be available at: http://localhost:5000{SWAGGER_URL}")
    print(f"JSON API docs available at: http://localhost:5000/api/docs")
    print(f"YAML file available at: http://localhost:5000/api/docs/yaml")
    print(f"Health check available at: http://localhost:5000/health")

    # Run the Flask development server
    app.run(
        host='0.0.0.0',  # Allow external connections
        port=5000,
        debug=True,  # Enable debug mode for development
        threaded=True  # Handle multiple requests concurrently
    )