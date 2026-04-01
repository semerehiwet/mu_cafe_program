import os
import logging
from typing import Dict

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# -------------------------------
# TOKEN (IMPORTANT)
# -------------------------------
TOKEN = os.getenv("8601948108:AAGeRbLQ0II9mDdK9p7qmqOM_AOk1FFD_gI")

if not TOKEN:
    raise ValueError("❌ BOT_TOKEN not found in environment variables")

# -------------------------------
# DATA
# -------------------------------

MEALS = {
    "ሰኞ": {"ቁርስ": "2 ዳቦ+ሩዝ+ሻይ", "ምሳ": "ፓስታ+2 ዳቦ", "እራት": "እንጀራ+ስልስ+ሽሮ"},
    "ማክሰኞ": {"ቁርስ": "2 ዳቦ+ፍርፍር+ሻይ", "ምሳ": "እንጀራ+ድንች", "እራት": "እንጀራ+ድንች"},
    "እሮብ": {"ቁርስ": "2 ዳቦ+ማኮሮኒ+ሻይ", "ምሳ": "እንጀራ+ድንች", "እራት": "እንጀራ+ክክ"},
    "ሐሙስ": {"ቁርስ": "2 ዳቦ+ፍርፍር+ሻይ", "ምሳ": "እንጀራ+ሽሮ", "እራት": "እንጀራ+ሽሮ"},
    "አርብ": {"ቁርስ": "2 ዳቦ+ሻይ", "ምሳ": "እንጀራ+ድንች+ሽሮ", "እራት": "እንጀራ+ሽሮ"},
    "ቅዳሜ": {"ቁርስ": "2 ዳቦ+ሩዝ+ሻይ", "ምሳ": "እንጀራ+ክክ", "እራት": "እንጀራ+ስልስ+ሽሮ"},
    "እሁድ": {"ቁርስ": "2 ዳቦ+ፍርፍር+ሻይ", "ምሳ": "እንጀራ+ሽሮ+ስልስ", "እራት": "እንጀራ+ክክ"}
}

DAY_MAPPING = {
    "day_mon": "ሰኞ", "day_tue": "ማክሰኞ", "day_wed": "እሮብ",
    "day_thu": "ሐሙስ", "day_fri": "አርብ", "day_sat": "ቅዳሜ", "day_sun": "እሁድ"
}

# -------------------------------
# KEYBOARDS
# -------------------------------

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🍽 የምግብ ፕሮግራም", callback_data="food")],
        [InlineKeyboardButton("❓ Help", callback_data="help")]
    ])

def days_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("ሰኞ", callback_data="day_mon"),
         InlineKeyboardButton("ማክሰኞ", callback_data="day_tue")],
        [InlineKeyboardButton("እሮብ", callback_data="day_wed"),
         InlineKeyboardButton("ሐሙስ", callback_data="day_thu")],
        [InlineKeyboardButton("አርብ", callback_data="day_fri"),
         InlineKeyboardButton("ቅዳሜ", callback_data="day_sat")],
        [InlineKeyboardButton("እሁድ", callback_data="day_sun")],
        [InlineKeyboardButton("🔙 Back", callback_data="main")]
    ])

# -------------------------------
# HANDLERS
# -------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ሰላም 👋", reply_markup=main_menu())

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "food":
        await query.edit_message_text("ቀን ምረጥ:", reply_markup=days_menu())

    elif data in DAY_MAPPING:
        day = DAY_MAPPING[data]
        m = MEALS[day]

        text = f"📅 {day}\n\n🍳 {m['ቁርስ']}\n🍝 {m['ምሳ']}\n🍲 {m['እራት']}"
        await query.edit_message_text(text, reply_markup=days_menu())

    elif data == "main":
        await query.edit_message_text("Main Menu", reply_markup=main_menu())

    elif data == "help":
        await query.edit_message_text("Use menu buttons", reply_markup=main_menu())

# -------------------------------
# MAIN
# -------------------------------

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))

    print("✅ Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
