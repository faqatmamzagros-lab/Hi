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

TEXTS = {
    "join_req": (
        "⚠️ تکایە سەرەتا جۆینی کەناڵەکەمان بکە بۆ ئەوەی بۆتەکەت بۆ کاربکات:\n\n📢"
        f" {CHANNEL_USERNAME}"
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


async def show_join_message(update: Update):
    t = TEXTS
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


async def send_main_link(
    update: Update, context: ContextTypes.DEFAULT_TYPE, is_new: bool = False
):
    user_id = str(update.effective_user.id)
    t = TEXTS

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

    is_joined = await check_channel_member(context.bot, user_id)
    if not is_joined:
        await show_join_message(update)
        return

    await send_main_link(update, context, is_new=False)


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    data = query.data

    if data == "check_join":
        is_joined = await check_channel_member(context.bot, user_id)
        if is_joined:
            await query.answer("✅ پشکنین سەرکەوتووبوو!")
            await send_main_link(update, context, is_new=False)
        else:
            await query.answer(TEXTS["not_joined"], show_alert=True)
        return

    if not await check_channel_member(context.bot, user_id):
        await query.answer()
        await show_join_message(update)
        return

    if data == "generate":
        await query.answer()
        await send_main_link(update, context, is_new=True)


if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot is starting...")
    app.run_polling()
