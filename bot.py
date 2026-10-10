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
BASE_URL = "https://faqatmamzagros-lab.github.io/Dev_y7_krd/"
CHANNEL_USERNAME = "@dev_y7_krd"
# =========================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

user_languages = {}

TEXTS = {
    "badini": {
        "join_req": (
            "⚠️ هیڤی دارین بەری هەر کەسەک ببیتە ئەندام د کەناڵێ مە دا:\n\n📢"
            f" {CHANNEL_USERNAME}"
        ),
        "btn_join": "📢 جۆینی کەناڵی ببە",
        "btn_check": "🔄 پشکنین (جۆین بووم)",
        "not_joined": (
            "❌ تۆ هێشتا جۆینی کەناڵی نەبووی! هیڤی دارین سەرەتا جۆین ببە."
        ),
        "link_ready": "✅ لینکا تە یا ئامادەیە!\n\n🔗 {url}",
        "new_link_ready": "✅ لینکا تە یا نوێ ئامادەیە!\n\n🔗 {url}",
        "btn_open": "🎯 ڤەکرنا لینکێ",
        "btn_generate": "🔄 دروستکرنا لینکا نوێ",
    },
    "sorani": {
        "join_req": (
            "⚠️ تکایە سەرەتا جۆینی کەناڵەکەمان بکە بۆ ئەوەی بۆتەکەت بۆ"
            f" کاربکات:\n\n📢 {CHANNEL_USERNAME}"
        ),
        "btn_join": "📢 جۆینی کەناڵ بکە",
        "btn_check": "🔄 پشکنینەوە (جۆین بووم)",
        "not_joined": (
            "❌ تۆ هێشتا جۆینی کەناڵەکەت نەکردووە! تکایە سەرەتا جۆین بکە."
        ),
        "link_ready": "✅ لینکەکەت ئامادەیە!\n\n🔗 {url}",
        "new_link_ready": "✅ لینکی نوێت ئامادەیە!\n\n🔗 {url}",
        "btn_open": "🎯 بەستەر بکەرەوە",
        "btn_generate": "🔄 دروستکردنی لینکی نوێ",
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
        "link_ready": "✅ Your Link is Ready!\n\n🔗 {url}",
        "new_link_ready": "✅ Your New Link is Ready!\n\n🔗 {url}",
        "btn_open": "🎯 Open Link",
        "btn_generate": "🔄 Generate New Link",
    },
    "ar": {
        "join_req": f"⚠️ يرجى الانضمام إلى قناتنا أولاً لاستخدام البوت:\n\n📢 {CHANNEL_USERNAME}",
        "btn_join": "📢 الانضمام للقناة",
        "btn_check": "🔄 التحقق من الانضمام",
        "not_joined": "❌ أنت لم تنضم إلى القناة بعد! يرجى الانضمام أولاً.",
        "link_ready": "✅ الرابط الخاص بك جاهز!\n\n🔗 {url}",
        "new_link_ready": "✅ الرابط الجديد الخاص بك جاهز!\n\n🔗 {url}",
        "btn_open": "🎯 فتح الرابط",
        "btn_generate": "🔄 إنشاء رابط جديد",
    },
}


async def check_channel_member(bot, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(
            chat_id=CHANNEL_USERNAME, user_id=user_id
        )
        return member.status in ["creator", "administrator", "member"]
    except Exception as e:
        logging.error(f"Error checking channel membership: {e}")
        return False


async def show_join_message(update: Update, lang: str):
    t = TEXTS.get(lang, TEXTS["sorani"])
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
    keyboard = [
        [
            InlineKeyboardButton("بادینی ☀️", callback_data="set_lang_badini"),
            InlineKeyboardButton("سۆرانی ☀️", callback_data="set_lang_sorani"),
        ],
        [
            InlineKeyboardButton("English 🇬🇧", callback_data="set_lang_en"),
            InlineKeyboardButton("العربية 🇸🇦", callback_data="set_lang_ar"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    msg = (
        "🌐 تکایە زمانێک هەڵبژێرە / زەحمەت نەبێت زمانەک هەڵبژێرە / Please select"
        " a language:"
    )

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
    lang = user_languages.get(int(user_id), "sorani")
    t = TEXTS.get(lang, TEXTS["sorani"])

    user_url = f"{BASE_URL}?chat_id={user_id}"

    keyboard = [
        [InlineKeyboardButton(t["btn_open"], url=user_url)],
        [InlineKeyboardButton(t["btn_generate"], callback_data="generate")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = (
        t["new_link_ready"].format(url=user_url)
        if is_new
        else t["link_ready"].format(url=user_url)
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

    # 1. ئەگەر بەکارهێنەر هێشتا زمان هەڵنەبژێرابێت، لیستەکا زمانان نیشا ددات
    if user_id not in user_languages:
        await ask_language(update)
        return

    lang = user_languages[user_id]

    # 2. پشکنینا جۆینبوونا کەناڵی
    is_joined = await check_channel_member(context.bot, user_id)
    if not is_joined:
        await show_join_message(update, lang)
        return

    # 3. ئەگەر جۆین بوو، لینکا تایبەت بۆ خۆی دەنێرێت
    await send_main_link(update, context, is_new=False)


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    data = query.data

    # کاتێک زمانەک هەڵدەبژێرێت
    if data.startswith("set_lang_"):
        await query.answer()
        selected_lang = data.replace("set_lang_", "")
        user_languages[user_id] = selected_lang

        # پاش هەڵبژارتنا زمانێ، دەستبەجێ پشکنینا جۆینبوونا کەناڵی دکەین
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

    # کاتێک دوگمەیا پشکنینا جۆین بوونێ لێدەت
    if data == "check_join":
        is_joined = await check_channel_member(context.bot, user_id)
        if is_joined:
            await query.answer("✅ ڕاستیپێدان سەرکەوتووبوو!")
            await send_main_link(update, context, is_new=False)
        else:
            await query.answer(
                TEXTS[lang].get(
                    "not_joined",
                    "❌ You have not joined the channel yet! Please join first.",
                ),
                show_alert=True,
            )
        return

    # دووبارە پشکنینا کەناڵی بۆ هەموارکرنا دوگمەیێن دی
    if not await check_channel_member(context.bot, user_id):
        await query.answer()
        await show_join_message(update, lang)
        return

    # دروستکرنا لینکا نوێ
    if data == "generate":
        await query.answer()
        await send_main_link(update, context, is_new=True)


if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot is starting...")
    app.run_polling()
