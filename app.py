from flask import Flask
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler
import os
import threading

app = Flask(__name__)

# Токен из переменной окружения (на Render нужно будет её добавить)
TOKEN = os.environ.get("TELEGRAM_TOKEN")

# Если токена нет — бот не запустится
if not TOKEN:
    raise ValueError("Нет токена! Добавьте TELEGRAM_TOKEN в переменные окружения.")

async def start(update, context):
    keyboard = [[InlineKeyboardButton("Инфо", url="https://t.me/skdnfgsdnfgksjfg")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Нажмите кнопку, чтобы перейти в канал:",
        reply_markup=reply_markup
    )

def run_bot():
    bot_app = Application.builder().token(TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))
    print("Бот запущен...")
    bot_app.run_polling()

@app.before_first_request
def start_bot():
    thread = threading.Thread(target=run_bot)
    thread.daemon = True
    thread.start()

@app.route('/')
def index():
    return "Бот работает!"

@app.route('/health')
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))