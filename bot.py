import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ሰላም! ቦቱ እየሰራ ነው ✅")

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
📅 ሳምንታዊ ምግብ ፕሮግራም

ሰኞ:
ቁርስ: 2 ዳቦ + ሩዝ + ሻይ
ምሳ: ፓስታ + 2 ዳቦ
እራት: እንጀራ + ስልስ + ሽሮ

ማክሰኞ:
ቁርስ: 2 ዳቦ + ፍርፍር + ሻይ
ምሳ: እንጀራ + ድንች
እራት: እንጀራ + ድንች

(ቀሪው እንደዚሁ ይቀጥላል...)
"""
    await update.message.reply_text(text)

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
