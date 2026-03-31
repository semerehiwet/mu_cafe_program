import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("8601948108:AAGeRbLQ0II9mDdK9p7qmqOM_AOk1FFD_gI")

# Menu keyboard
main_menu = [["🍽 የምግብ ፕሮግራም", "📍 የካፌ location"], ["❓ Help"]]

food_days = [["ሰኞ", "ማክሰኞ", "እሮብ"], ["ሐሙስ", "አርብ", "ቅዳሜ", "እሁድ"]]

locations = [["አሪድ", "ቢዝነስ"], ["ዓይደር", "ዲያስፖራ"]]

menu_data = {
    "ሰኞ": "ቁርስ: 2 ዳቦ+ሩዝ+ሻይ\nምሳ: ፓስታ+2 ዳቦ\nእራት: እንጀራ+ስልስ+ሽሮ",
    "ማክሰኞ": "ቁርስ: 2 ዳቦ+ፍርፍር+ሻይ\nምሳ: እንጀራ+ድንች\nእራት: እንጀራ+ድንች",
    "እሮብ": "ቁርስ: 2 ዳቦ+ማኮሮኒ+ሻይ\nምሳ: እንጀራ+ድንች\nእራት: እንጀራ+ክክ",
    "ሐሙስ": "ቁርስ: 2 ዳቦ+ፍርፍር+ሻይ\nምሳ: እንጀራ+ሽሮ\nእራት: እንጀራ+ሽሮ",
    "አርብ": "ቁርስ: 2 ዳቦ+ሻይ\nምሳ: እንጀራ+ድንች+ሽሮ\nእራት: እንጀራ+ሽሮ",
    "ቅዳሜ": "ቁርስ: 2 ዳቦ+ሩዝ+ሻይ\nምሳ: እንጀራ+ክክ\nእራት: እንጀራ+ስልስ+ሽሮ",
    "እሁድ": "ቁርስ: 2 ዳቦ+ፍርፍር+ሻይ\nምሳ: እንጀራ+ሽሮ+ስልስ\nእራት: እንጀራ+ክክ"
}

location_data = {
    "አሪድ": "ከመግቢያ በር 500m ወደ ሰሜን",
    "ቢዝነስ": "ከግቢ መካከል",
    "ዓይደር": "ከሆስፒታል አጠገብ",
    "ዲያስፖራ": "ከመንገድ አጠገብ"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "እንኳን ወደ Cafe Bot በደህና መጡ!",
        reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🍽 የምግብ ፕሮግራም":
        await update.message.reply_text("ቀን ምረጥ:", reply_markup=ReplyKeyboardMarkup(food_days, resize_keyboard=True))

    elif text in menu_data:
        await update.message.reply_text(menu_data[text])

    elif text == "📍 የካፌ location":
        await update.message.reply_text("ቦታ ምረጥ:", reply_markup=ReplyKeyboardMarkup(locations, resize_keyboard=True))

    elif text in location_data:
        await update.message.reply_text(location_data[text])

    elif text == "❓ Help":
        await update.message.reply_text("ምን ማድረግ ትፈልጋለህ? ምርጫ ይምረጡ።")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
