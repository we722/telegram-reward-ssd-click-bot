
import os
import json
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

TOKEN = os.getenv("BOT_TOKEN")
ADS_LINK = os.getenv("ADS_LINK", "https://example.com")
DATA_FILE = "users.json"

app = Flask(__name__)
application = ApplicationBuilder().token(TOKEN).build()

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"users": {}, "clicks": 0}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    data = load_data()
    data["users"][user_id] = data["users"].get(user_id, 0)
    save_data(data)
    keyboard = [[InlineKeyboardButton("Click to Earn", url=ADS_LINK)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Click the button below to earn points:", reply_markup=reply_markup)

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    total_users = len(data["users"])
    total_clicks = data["clicks"]
    income = total_clicks * 0.01
    await update.message.reply_text(
        f"Total Users: {total_users}\nTotal Clicks: {total_clicks}\nEstimated Income: ${income:.2f}"
    )

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = str(query.from_user.id)
    data = load_data()
    data["users"][user_id] = data["users"].get(user_id, 0) + 1
    data["clicks"] += 1
    save_data(data)
    await query.edit_message_text("Thanks for clicking! You earned 1 point.")

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("stat", stats))
application.add_handler(CallbackQueryHandler(button_click))

@app.route("/", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put(update)
    return "ok"

if __name__ == "__main__":
    app.run(port=5000)
