import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TELEGRAM_TOKEN")

user_data = {}

LANG = {
    'en': {'start': '🪙 Welcome to Coin Tap Master! Tap to earn!'},
    'bn': {'start': '🪙 Coin Tap Master এ স্বাগতম! Tap করে কয়েন কামাও!'},
    'hi': {'start': '🪙 Coin Tap Master में आपका स्वागत है! Tap करके सिक्के कमाओ!'}
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_data:
        user_data[user_id] = {'coins': 0, 'lang': 'bn'}
    lang = user_data[user_id]['lang']
    
    keyboard = [
        [InlineKeyboardButton("🪙 Tap Coin", callback_data='tap')],
        [InlineKeyboardButton("💰 Wallet", callback_data='wallet')],
        [InlineKeyboardButton("📊 Balance", callback_data='balance')],
        [InlineKeyboardButton("🌐 Language", callback_data='lang')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(LANG[lang]['start'], reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lang = user_data.get(user_id, {'lang': 'bn'})['lang']
    
    if query.data == 'tap':
        user_data[user_id]['coins'] += 1
        await query.edit_message_text(f"ট্যাপ করছো! মোট কয়েন: {user_data[user_id]['coins']}")
    elif query.data == 'wallet':
        await query.edit_message_text("Send: /connect your_wallet_address")
    elif query.data == 'balance':
        await query.edit_message_text(f"তোমার ব্যালেন্স: {user_data[user_id]['coins']} কয়েন")
    elif query.data == 'lang':
        await query.edit_message_text("Select Language: /lang en or /lang bn or /lang hi")

async def lang_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        user_id = update.effective_user.id
        user_data[user_id]['lang'] = context.args[0]
        await update.message.reply_text(f"Language Changed to {context.args[0]}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("lang", lang_cmd))
    app.add_handler(CallbackQueryHandler(button))
    print("Bot is running...")
    app.run_polling() # এটা খুব জরুরি
