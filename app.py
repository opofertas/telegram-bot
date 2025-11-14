from flask import Flask, request
import telebot
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")  # opcional

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    json_data = request.get_json()
    update = telebot.types.Update.de_json(json_data)
    bot.process_new_updates([update])
    return "OK", 200

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Bot funcionando no Render 🎉!")

@app.route("/")
def home():
    return "Bot está no ar!", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    bot.remove_webhook()
    bot.set_webhook(url=f"https://telegram-bot-21qr.onrender.com/webhook")
    app.run(host="0.0.0.0", port=port)
