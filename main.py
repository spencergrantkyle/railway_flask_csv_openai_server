from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# Use Railway's provided environment variables
PORT = int(os.getenv("PORT", 5000))
RAILWAY_PUBLIC_DOMAIN = os.getenv("RAILWAY_PUBLIC_DOMAIN", "")
RAILWAY_ENVIRONMENT_NAME = os.getenv("RAILWAY_ENVIRONMENT_NAME", "production")

# Build webhook URL using Railway's public domain
WEBHOOK_BASE_URL = f"https://{RAILWAY_PUBLIC_DOMAIN}" if RAILWAY_PUBLIC_DOMAIN else "http://localhost:5000"


@app.route('/')
def index():
    return jsonify({
        "Choo Choo": "Welcome to your Flask app 🚅",
        "environment": RAILWAY_ENVIRONMENT_NAME,
        "webhook_url": f"{WEBHOOK_BASE_URL}/webhook",
        "railway_domain": RAILWAY_PUBLIC_DOMAIN
    })


@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Webhook endpoint to receive POST requests from N8N server
    """
    try:
        # Get the JSON data from the request
        data = request.get_json()
        
        # Log the received data for debugging
        print(f"Received data from N8N: {data}")
        
        # Process the data here as needed
        # For now, we'll just echo it back with a success message
        
        response = {
            "status": "success",
            "message": "Data received successfully from N8N",
            "received_data": data,
            "environment": RAILWAY_ENVIRONMENT_NAME,
            "railway_domain": RAILWAY_PUBLIC_DOMAIN
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
    print(f"Starting Flask app on Railway")
    print(f"Environment: {RAILWAY_ENVIRONMENT_NAME}")
    print(f"Public Domain: {RAILWAY_PUBLIC_DOMAIN}")
    print(f"Webhook URL: {WEBHOOK_BASE_URL}/webhook")
    app.run(debug=False, port=PORT, host='0.0.0.0')