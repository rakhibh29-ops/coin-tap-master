import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TELEGRAM_TOKEN")

user_data = {}

LANG = {
    'en': {'start': '🪙 Welcome to Coin Tap Master! Tap to earn!'},
    'bn': {'start': '🪙 Coin Tap Master এ স্বাগতম! Tap করে কয়েন কামাও!'},
    'hi': {'start': '🪙 Coin Tap Master में आपका स्वागत है! Tap करके सिक्के कमाओ!'},
    'ar': {'start': '🪙 مرحبًا بك في Coin Tap Master! اضغط لكسب العملات!'},
    'zh': {'start': '🪙 欢迎来到 Coin Tap Master！点击赚钱！'}
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_data:
        user_data[user_id] = {'coins': 0, 'lang': 'bn'}
    lang = user_data[user_id]['lang']
    
    # নিচের Reply Keyboard
    reply_keyboard = [
        ["ট্যাপ করো 🔥", "ব্যালেন্স 💰"],
        ["ভিডিও দেখে 200 কয়েন 🎁"],
        ["রেফার 🤝", "উত্তোলন 💸"],
        ["📢 সবাইকে জানাও"]
    ]
    reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    
    # উপরের Inline Keyboard
    keyboard = [
        [InlineKeyboardButton("🪙 Tap Coin", callback_data='tap')],
        [InlineKeyboardButton("💰 Wallet", callback_data='wallet')],
        [InlineKeyboardButton("📊 Balance", callback_data='balance')],
        [InlineKeyboardButton("🌐 Language", callback_data='lang')]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(LANG[lang]['start'], reply_markup=inline_markup)
    await update.message.reply_text("মেনু:", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {'coins': 0, 'lang': 'bn'}
    
    if query.data == 'tap':
        user_data[user_id]['coins'] += 1
        await query.edit_message_text(f"ট্যাপ করছো! মোট কয়েন: {user_data[user_id]['coins']}")
    elif query.data == 'wallet':
        await query.edit_message_text("Send: /connect your_wallet_address")
    elif query.data == 'balance':
        await query.edit_message_text(f"তোমার ব্যালেন্স: {user_data[user_id]['coins']} কয়েন")
    elif query.data == 'lang':
        text = "اختر اللغة: /lang ar\n选择语言: /lang zh\nSelect: /lang en /lang bn /lang hi"
        await query.edit_message_text(text)

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_data:
        user_data[user_id] = {'coins': 0, 'lang': 'bn'}
    text = update.message.text
    
    if text == "ট্যাপ করো 🔥":
        user_data[user_id]['coins'] += 1
        await update.message.reply_text(f"ট্যাপ করছো! মোট কয়েন: {user_data[user_id]['coins']}")
    elif text == "ব্যালেন্স 💰":
        await update.message.reply_text(f"তোমার ব্যালেন্স: {user_data[user_id]['coins']} কয়েন")
    elif text == "ভিডিও দেখে 200 কয়েন 🎁":
        user_data[user_id]['coins'] += 200
        await update.message.reply_text(f"200 কয়েন পাইলা! মোট: {user_data[user_id]['coins']}")
    elif text == "রেফার 🤝":
        await update.message.reply_text(f"তোমার রেফার লিংক: https://t.me/{context.bot.username}?start={user_id}")
    elif text == "উত্তোলন 💸":
        await update.message.reply_text("Minimum 1000 কয়েন লাগবে উত্তোলনের জন্য")

async def lang_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        user_id = update.effective_user.id
        if user_id not in user_data:
            user_data[user_id] = {'coins': 0, 'lang': 'bn'}
        user_data[user_id]['lang'] = context.args[0]
        await update.message.reply_text(f"Language Changed to {context.args[0]}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("lang", lang_cmd))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    print("Bot is running...")
    app.run_polling()
