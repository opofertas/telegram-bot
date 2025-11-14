from flask import Flask, request, jsonify
import telebot
import os

# Flask app
app = Flask(__name__)

# Tokens via variáveis de ambiente
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Bot
bot = telebot.TeleBot(BOT_TOKEN)


# ===== HOME =====
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Bot is running!"}), 200


# ===== WEBHOOK (RENDER chama aqui) =====
@app.route("/webhook", methods=["POST"])
def webhook():
    json_data = request.get_json()
    update = telebot.types.Update.de_json(json_data)
    bot.process_new_updates([update])
    return "OK", 200


# ===== EXEMPLO ENVIO MANUAL VIA API =====
@app.route("/send", methods=["POST"])
def send_message():
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' field"}), 400

    if not BOT_TOKEN or not CHAT_ID:
        return jsonify({"error": "Environment variables missing"}), 500

    text = data["text"]
    bot.send_message(CHAT_ID, text)

    return jsonify({"status": "Message sent successfully!"}), 200


# ===== COMANDO /start =====
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Bot funcionando no Render 🎉!")


# ===== INICIAR SERVER =====
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))

    bot.remove_webhook()
    bot.set_webhook(url="https://telegram-bot-21qr.onrender.com/webhook")

    app.run(host="0.0.0.0", port=port)
