import os
import logging
from typing import Dict

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# -------------------------------
# Data
# -------------------------------

# Meal data for each day (Amharic names)
MEALS: Dict[str, Dict[str, str]] = {
    "ሰኞ": {
        "ቁርስ": "2 ዳቦ+ሩዝ+ሻይ",
        "ምሳ": "ፓስታ+2 ዳቦ",
        "እራት": "እንጀራ+ስልስ+ሽሮ"
    },
    "ማክሰኞ": {
        "ቁርስ": "2 ዳቦ+ፍርፍር+ሻይ",
        "ምሳ": "እንጀራ+ድንች",
        "እራት": "እንጀራ+ድንች"
    },
    "እሮብ": {
        "ቁርስ": "2 ዳቦ+ማኮሮኒ+ሻይ",
        "ምሳ": "እንጀራ+ድንች",
        "እራት": "እንጀራ+ክክ"
    },
    "ሐሙስ": {
        "ቁርስ": "2 ዳቦ+ፍርፍር+ሻይ",
        "ምሳ": "እንጀራ+ሽሮ",
        "እራት": "እንጀራ+ሽሮ"
    },
    "አርብ": {
        "ቁርስ": "2 ዳቦ+ሻይ",
        "ምሳ": "እንጀራ+ድንች+ሽሮ",
        "እራት": "እንጀራ+ሽሮ"
    },
    "ቅዳሜ": {
        "ቁርስ": "2 ዳቦ+ሩዝ+ሻይ",
        "ምሳ": "እንጀራ+ክክ",
        "እራት": "እንጀራ+ስልስ+ሽሮ"
    },
    "እሁድ": {
        "ቁርስ": "2 ዳቦ+ፍርፍር+ሻይ",
        "ምሳ": "እንጀራ+ሽሮ+ስልስ",
        "እራት": "እንጀራ+ክክ"
    }
}

# Mapping from English callback IDs to Amharic day names
DAY_MAPPING: Dict[str, str] = {
    "day_mon": "ሰኞ",
    "day_tue": "ማክሰኞ",
    "day_wed": "እሮብ",
    "day_thu": "ሐሙስ",
    "day_fri": "አርብ",
    "day_sat": "ቅዳሜ",
    "day_sun": "እሁድ"
}

# Location data (Amharic names and descriptions)
LOCATIONS: Dict[str, str] = {
    "አሪድ": "ከመግብያ በር 500 ሜትር ወደ ሰሜን",
    "ቢዝነስ": "ከመግብያ በር 300 ሜትር ወደ ምስራቅ",
    "ዓይደር": "ከመግብያ በር 1 ኪሎ ሜትር ወደ ደቡብ",
    "ዲያስፖራ": "ከመግብያ በር 700 ሜትር ወደ ምዕራብ"
}

# Mapping for location callbacks
LOCATION_MAPPING: Dict[str, str] = {
    "loc_arid": "አሪድ",
    "loc_business": "ቢዝነስ",
    "loc_ayder": "ዓይደር",
    "loc_diaspora": "ዲያስፖራ"
}

# -------------------------------
# Helper Functions
# -------------------------------

def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """Return the main menu keyboard."""
    keyboard = [
        [InlineKeyboardButton("🍽 የምግብ ፕሮግራም", callback_data="food_menu")],
        [InlineKeyboardButton("📍 የካፌ location", callback_data="location_menu")],
        [InlineKeyboardButton("❓ Help", callback_data="help")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_days_menu_keyboard() -> InlineKeyboardMarkup:
    """Return the days selection keyboard."""
    buttons = [
        [InlineKeyboardButton("ሰኞ", callback_data="day_mon"),
         InlineKeyboardButton("ማክሰኞ", callback_data="day_tue")],
        [InlineKeyboardButton("እሮብ", callback_data="day_wed"),
         InlineKeyboardButton("ሐሙስ", callback_data="day_thu")],
        [InlineKeyboardButton("አርብ", callback_data="day_fri"),
         InlineKeyboardButton("ቅዳሜ", callback_data="day_sat")],
        [InlineKeyboardButton("እሁድ", callback_data="day_sun")],
        [InlineKeyboardButton("🔙 ወደ ዋና ምናሌ", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(buttons)

def get_location_menu_keyboard() -> InlineKeyboardMarkup:
    """Return the location selection keyboard."""
    keyboard = [
        [InlineKeyboardButton("አሪድ", callback_data="loc_arid"),
         InlineKeyboardButton("ቢዝነስ", callback_data="loc_business")],
        [InlineKeyboardButton("ዓይደር", callback_data="loc_ayder"),
         InlineKeyboardButton("ዲያስፖራ", callback_data="loc_diaspora")],
        [InlineKeyboardButton("🔙 ወደ ዋና ምናሌ", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_to_days_keyboard() -> InlineKeyboardMarkup:
    """Return keyboard with 'Back to days' and 'Main menu' buttons."""
    keyboard = [
        [InlineKeyboardButton("🔙 ወደ ቀናት ምናሌ", callback_data="food_menu")],
        [InlineKeyboardButton("🏠 ዋና ምናሌ", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_to_locations_keyboard() -> InlineKeyboardMarkup:
    """Return keyboard with 'Back to locations' and 'Main menu' buttons."""
    keyboard = [
        [InlineKeyboardButton("🔙 ወደ location ምናሌ", callback_data="location_menu")],
        [InlineKeyboardButton("🏠 ዋና ምናሌ", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def format_meal_message(day_name: str, meals: Dict[str, str]) -> str:
    """Format the meal details for a given day."""
    breakfast = meals.get("ቁርስ", "አልተገኘም")
    lunch = meals.get("ምሳ", "አልተገኘም")
    dinner = meals.get("እራት", "አልተገኘም")
    return (
        f"📅 *{day_name}*\n\n"
        f"🍳 *ቁርስ*: {breakfast}\n"
        f"🍝 *ምሳ*: {lunch}\n"
        f"🍲 *እራት*: {dinner}\n"
    )

# -------------------------------
# Command Handlers
# -------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message and show the main menu."""
    user = update.effective_user
    welcome_text = (
        f"እንኳን ደህና መጡ {user.first_name}! 👋\n\n"
        "ከዚህ በታች ካለው ምናሌ መምረጥ ትችላላችሁ።"
    )
    await update.message.reply_text(welcome_text, reply_markup=get_main_menu_keyboard())

# -------------------------------
# Callback Query Handlers
# -------------------------------

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle all inline keyboard button presses."""
    query = update.callback_query
    await query.answer()

    data = query.data

    # Main menu items
    if data == "food_menu":
        await query.edit_message_text(
            "ቀን ምረጥ፡",
            reply_markup=get_days_menu_keyboard()
        )
    elif data == "location_menu":
        await query.edit_message_text(
            "location ምረጥ፡",
            reply_markup=get_location_menu_keyboard()
        )
    elif data == "help":
        help_text = (
            "❓ *ማጠቃለያ*\n\n"
            "ይህ ቦት የካፌውን የምግብ ፕሮግራም፣ ቅርንጫፎችን አድራሻ እና እገዛ ይሰጣል።\n\n"
            "🔹 *የምግብ ፕሮግራም* → ቀን ምረጥ → የቁርስ፣ ምሳ እና እራት ዝርዝር ታያለህ።\n"
            "🔹 *የካፌ location* → ቅርንጫፍ ምረጥ → አድራሻውን ታያለህ።\n"
            "🔹 *Help* → ይህ መልእክት ያሳያል።\n\n"
            "ማንኛውንም ጥያቄ ካለህ ለአስተዳዳሪዎቻችን መግለጽ ትችላለህ።"
        )
        await query.edit_message_text(help_text, reply_markup=get_main_menu_keyboard())
    elif data == "main_menu":
        await query.edit_message_text("ዋና ምናሌ፡", reply_markup=get_main_menu_keyboard())

    # Day selections
    elif data in DAY_MAPPING:
        day_amharic = DAY_MAPPING[data]
        if day_amharic in MEALS:
            meal_text = format_meal_message(day_amharic, MEALS[day_amharic])
            await query.edit_message_text(
                meal_text,
                parse_mode="Markdown",
                reply_markup=get_back_to_days_keyboard()
            )
        else:
            await query.edit_message_text(
                f"ለ{day_amharic} የምግብ መረጃ አልተገኘም።",
                reply_markup=get_back_to_days_keyboard()
            )

    # Location selections
    elif data in LOCATION_MAPPING:
        loc_amharic = LOCATION_MAPPING[data]
        if loc_amharic in LOCATIONS:
            loc_info = LOCATIONS[loc_amharic]
            await query.edit_message_text(
                f"📍 *{loc_amharic}*\n\n{loc_info}",
                parse_mode="Markdown",
                reply_markup=get_back_to_locations_keyboard()
            )
        else:
            await query.edit_message_text(
                f"ለ{loc_amharic} አድራሻ አልተገኘም።",
                reply_markup=get_back_to_locations_keyboard()
            )

    else:
        await query.edit_message_text(
            "የማይታወቅ ምርጫ። እባክህ እንደገና ሞክር።",
            reply_markup=get_main_menu_keyboard()
        )

# -------------------------------
# Main
# -------------------------------

def main() -> None:
    """Start the bot."""
    # Get token from environment variable
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("No TELEGRAM_BOT_TOKEN found in environment variables.")
        return

    # Create the Application
    application = Application.builder().token(token).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_callback))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
