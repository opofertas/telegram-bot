from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Load secrets from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Telegram Bot API is running!"})

@app.route("/send", methods=["POST"])
def send_message():
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "The field 'text' is required"}), 400

    text = data["text"]

    if not BOT_TOKEN or not CHAT_ID:
        return jsonify({"error": "Environment variables not configured"}), 500

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}

    response = requests.post(url, data=payload)

    if response.status_code == 200:
        return jsonify({"status": "Message sent successfully!"})
    else:
        return jsonify({
            "error": "Failed to send message",
            "details": response.text
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
