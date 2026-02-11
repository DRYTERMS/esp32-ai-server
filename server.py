from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Your shared secret for ESP32 authentication
DEVICE_TOKEN = "esp32_secret_2026"

# OpenAI API key stored as environment variable (never hardcode it)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

@app.route("/ask", methods=["POST"])
def ask():
    # Check ESP32 token
    auth = request.headers.get("X-Device-Token")
    if auth != DEVICE_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401

    # Get message from ESP32
    data = request.json
    user_message = data.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Call OpenAI API
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": user_message}]
        }
    )

    # Return OpenAI response to ESP32
    return jsonify(response.json())

if __name__ == "__main__":
    # Run Flask server
    app.run(host="0.0.0.0", port=5000)
