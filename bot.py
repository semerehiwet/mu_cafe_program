import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

menu_keyboard = [
    ["የምግብ ፕሮግራም"],
    ["የካፌ location"],
    ["Help"]
]

days_keyboard = [
    ["ሰኞ","ማክሰኞ"],
    ["እሮብ","ሐሙስ"],
    ["አርብ","ቅዳሜ"],
    ["እሁድ"]
]

locations_keyboard = [
    ["አሪድ","ቢዝነስ"],
    ["ዓይደር","ዲያስፖራ"]
]

food_menu = {
    "ሰኞ": "ቁርስ: 2 ዳቦ+ሩዝ+ሻይ\nምሳ: ፓስታ+2 ዳቦ\nእራት: እንጀራ+ስልስ+ሽሮ",
    "ማክሰኞ": "ቁርስ: 2 ዳቦ+ፍርፍር+ሻይ\nምሳ: እንጀራ+ድንች\nእራት: እንጀራ+ድንች",
    "እሮብ": "ቁርስ: 2 ዳቦ+ማኮሮኒ+ሻይ\nምሳ: እንጀራ+ድንች\nእራት: እንጀራ+ክክ",
    "ሐሙስ": "ቁርስ: 2 ዳቦ+ፍርፍር+ሻይ\nምሳ: እንጀራ+ሽሮ\nእራት: እንጀራ+ሽሮ",
    "አርብ": "ቁርስ: 2 ዳቦ+ሻይ\nምሳ: እንጀራ+ድንች+ሽሮ\nእራት: እንጀራ+ሽሮ",
    "ቅዳሜ": "ቁርስ: 2 ዳቦ+ሩዝ+ሻይ\nምሳ: እንጀራ+ክክ\nእራት: እንጀራ+ስልስ+ሽሮ",
    "እሁድ": "ቁርስ: 2 ዳቦ+ፍርፍር+ሻይ\nምሳ: እንጀራ+ሽሮ+ስልስ\nእራት: እንጀራ+ክክ"
}

locations = {
    "አሪድ": "ከመግቢያ በር 500 ሜትር ወደ ሰሜን",
    "ቢዝነስ": "ከመግቢያ በር 300 ሜትር ወደ ምስራቅ",
    "ዓይደር": "ከመግቢያ በር 200 ሜትር ወደ ምዕራብ",
    "ዲያስፖራ": "ከመግቢያ በር 400 ሜትር ወደ ደቡብ"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "እንኳን ወደ ካፌ ቦት በደህና መጡ",
        reply_markup=ReplyKeyboardMarkup(menu_keyboard, resize_keyboard=True)
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "የምግብ ፕሮግራም":
        await update.message.reply_text("ቀን ምረጥ:", reply_markup=ReplyKeyboardMarkup(days_keyboard, resize_keyboard=True))

    elif text in food_menu:
        await update.message.reply_text(food_menu[text])

    elif text == "የካፌ location":
        await update.message.reply_text("location ምረጥ:", reply_markup=ReplyKeyboardMarkup(locations_keyboard, resize_keyboard=True))

    elif text in locations:
        await update.message.reply_text(locations[text])

    elif text == "Help":
        await update.message.reply_text("ምን እርዳታ ትፈልጋለህ?")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
