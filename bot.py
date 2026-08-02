import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
user_data = {}

LANG = {
    'en': {'start': '🪙 Welcome to Coin Tap Master!\nTap to earn coins!', 'balance': '💰 Balance: '},
    'bn': {'start': '🪙 Coin Tap Master এ স্বাগতম!\nকয়েন কামাতে Tap করুন!', 'balance': '💰 ব্যালেন্স: '},
    'hi': {'start': '🪙 Coin Tap Master में आपका स्वागत है!\nसिक्के कमाने के लिए टैप करें!', 'balance': '💰 बैलेंस: '}
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_data: user_data[user_id] = {'coins': 0, 'lang': 'bn'}
    lang = user_data[user_id]['lang']
    keyboard = [
        [InlineKeyboardButton("Tap Coin 🪙", callback_data='tap')],
        [InlineKeyboardButton("Wallet 🔗", callback_data='wallet')],
        [InlineKeyboardButton("Balance 💰", callback_data='balance')],
        [InlineKeyboardButton("Language 🌍", callback_data='lang')]
    ]
    await update.message.reply_text(LANG[lang]['start'], reply_markup=InlineKeyboardMarkup(keyboard))

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query; await query.answer(); user_id = query.from_user.id
    if user_id not in user_data: user_data[user_id] = {'coins': 0, 'lang': 'bn'}
    lang = user_data[user_id]['lang']
    if query.data == 'tap':
        user_data[user_id]['coins'] += 1;
        await query.edit_message_text("Coin Tapped! +1 🪙")
    elif query.data == 'wallet':
        await query.edit_message_text("Send: /connect <your_wallet_address>")
    elif query.data == 'balance':
        await query.edit_message_text(f"{LANG[lang]['balance']}{user_data[user_id]['coins']}")
    elif query.data == 'lang':
        await query.edit_message_text("Select: /lang en | /lang bn | /lang hi")

async def lang_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        user_data[update.effective_user.id]['lang'] = context.args[0];
        await update.message.reply_text("Language Changed ✅")

async def connect(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        await update.message.reply_text(f"Wallet Connected: {context.args[0]}")
    else:
        await update.message.reply_text("Usage: /connect <wallet_address>")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("lang", lang_cmd))
    app.add_handler(CommandHandler("connect", connect))
    app.add_handler(CallbackQueryHandler(button))
    print("Bot Running...")
    app.run_polling()

if __name__ == '__main__':
    main()
