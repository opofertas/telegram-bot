import os
from flask import Flask, request, jsonify
import telebot

# Carrega tokens
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not BOT_TOKEN:
    raise Exception("BOT_TOKEN não configurado no Render")

# Inicializa bot
bot = telebot.TeleBot(BOT_TOKEN)

# Inicializa Flask
app = Flask(__name__)

# ===== HOME =====
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Bot está rodando!"}), 200


# ===== WEBHOOK =====
@app.route("/webhook", methods=["POST"])
def webhook():
    json_data = request.get_json()

    if not json_data:
        return "No JSON", 400

    update = telebot.types.Update.de_json(json_data)
    bot.process_new_updates([update])

    return "OK", 200


# ===== ROTA MANUAL PARA ENVIO =====
@app.route("/send", methods=["POST"])
def send_message():
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "Campo 'text' é obrigatório"}), 400

    if not CHAT_ID:
        return jsonify({"error": "CHAT_ID não configurado"}), 500

    bot.send_message(CHAT_ID, data["text"])
    return jsonify({"status": "Mensagem enviada!"}), 200


# ===== COMANDO /start =====
@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Bot funcionando no Render 🎉")


# ===== INICIAR SERVIDOR =====
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))

    bot.remove_webhook()
    bot.set_webhook(url="https://telegram-bot-21qr.onrender.com/webhook")

    app.run(host="0.0.0.0", port=port)
