import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

# Main Menu
menu = [
    ["የምግብ ፕሮግራም"],
    ["የካፌ location"],
    ["Help"]
]

# Days Menu
days = [
    ["ሰኞ", "ማክሰኞ"],
    ["እሮብ", "ሐሙስ"],
    ["አርብ", "ቅዳሜ"],
    ["እሁድ"]
]

# Locations Menu
locations_menu = [
    ["አሪድ", "ቢዝነስ"],
    ["ዓይደር", "ዲያስፖራ"]
]

# Food Data
food = {
    "ሰኞ": "ቁርስ: 2 ዳቦ+ሩዝ+ሻይ\nምሳ: ፓስታ+2 ዳቦ\nእራት: እንጀራ+ስልስ+ሽሮ",
    "ማክሰኞ": "ቁርስ: 2 ዳቦ+ፍርፍር+ሻይ\nምሳ: እንጀራ+ድንች\nእራት: እንጀራ+ድንች",
    "እሮብ": "ቁርስ: 2 ዳቦ+ማኮሮኒ+ሻይ\nምሳ: እንጀራ+ድንች\nእራት: እንጀራ+ክክ",
    "ሐሙስ": "ቁርስ: 2 ዳቦ+ፍርፍር+ሻይ\nምሳ: እንጀራ+ሽሮ\nእራት: እንጀራ+ሽሮ",
    "አርብ": "ቁርስ: 2 ዳቦ+ሻይ\nምሳ: እንጀራ+ድንች+ሽሮ\nእራት: እንጀራ+ሽሮ",
    "ቅዳሜ": "ቁርስ: 2 ዳቦ+ሩዝ+ሻይ\nምሳ: እንጀራ+ክክ\nእራት: እንጀራ+ስልስ+ሽሮ",
    "እሁድ": "ቁርስ: 2 ዳቦ+ፍርፍር+ሻይ\nምሳ: እንጀራ+ሽሮ+ስልስ\nእራት: እንጀራ+ክክ"
}

# Location Data
locations = {
    "አሪድ": "ከመግቢያ 500 ሜትር ወደ ሰሜን",
    "ቢዝነስ": "ከመግቢያ 300 ሜትር ወደ ምስራቅ",
    "ዓይደር": "ከመግቢያ 200 ሜትር ወደ ምዕራብ",
    "ዲያስፖራ": "ከመግቢያ 400 ሜትር ወደ ደቡብ"
}

# Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "እንኳን ደህና መጡ 🍽️",
        reply_markup=ReplyKeyboardMarkup(menu, resize_keyboard=True)
    )

# Handle Messages
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "የምግብ ፕሮግራም":
        await update.message.reply_text("ቀን ምረጥ:", reply_markup=ReplyKeyboardMarkup(days, resize_keyboard=True))

    elif text in food:
        await update.message.reply_text(food[text])

    elif text == "የካፌ location":
        await update.message.reply_text("location ምረጥ:", reply_markup=ReplyKeyboardMarkup(locations_menu, resize_keyboard=True))

    elif text in locations:
        await update.message.reply_text(locations[text])

    elif text == "Help":
        await update.message.reply_text("እባክህ ከmenu ምረጥ 🙂")

# Main Function
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle))

    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
