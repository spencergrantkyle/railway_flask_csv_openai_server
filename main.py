from flask import Flask, jsonify, request
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Environment-driven configuration
DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"
PORT = int(os.getenv("PORT", 5000))
WEBHOOK_BASE_URL = os.getenv("WEBHOOK_BASE_URL", "http://localhost:5000")


@app.route('/')
def index():
    return jsonify({
        "Choo Choo": "Welcome to your Flask app 🚅",
        "environment": os.getenv("FLASK_ENV", "production"),
        "webhook_url": f"{WEBHOOK_BASE_URL}/webhook"
    })


@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Webhook endpoint to receive POST requests from N8N server
    """
    try:
        # Get the JSON data from the request
        data = request.get_json()
        
        # Log the received data (only in debug mode)
        if DEBUG:
            print(f"Received data from N8N: {data}")
        
        # Process the data here as needed
        # For now, we'll just echo it back with a success message
        
        response = {
            "status": "success",
            "message": "Data received successfully from N8N",
            "received_data": data,
            "environment": os.getenv("FLASK_ENV", "production")
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        # Handle any errors
        error_response = {
            "status": "error",
            "message": f"Error processing request: {str(e)}"
        }
        return jsonify(error_response), 400


if __name__ == '__main__':
    print(f"Starting Flask app in {'DEBUG' if DEBUG else 'PRODUCTION'} mode")
    print(f"Webhook URL: {WEBHOOK_BASE_URL}/webhook")
    app.run(debug=DEBUG, port=PORT, host='0.0.0.0')