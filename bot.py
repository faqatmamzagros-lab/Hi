import logging
from datetime import datetime, timedelta
import pytz
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# Token و ئایدیێن خودانان (Owners)
TOKEN = "8868138985:AAGJ8_duPPPQXhBSf1DnQlImeUO-WRHSmMA"
OWNERS = [7904656691, 7643191802]
OWNER_TAGS = "@Y2_KRD و @B4llam"

# زانیاریێن پایەیی یێن بەکارهێنەران (د دەبەت بێتە گلۆبال کرن یان د داتابەیسێ دا هێتە پاشەکەوتکرن)
users_db = {}  # {user_id: {"balance": 0, "subscription": None, "sub_expiry": None, "username": "", "nickname": ""}}

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

def get_baghdad_time():
    tz = pytz.timezone("Asia/Baghdad")
    return datetime.now(tz)

async def check_expiry(user_id):
    if user_id in users_db and users_db[user_id]["sub_expiry"]:
        now = get_baghdad_time()
        if now > users_db[user_id]["sub_expiry"]:
            users_db[user_id]["subscription"] = None
            users_db[user_id]["sub_expiry"] = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_id = user.id
    nickname = user.first_name if user.first_name else "بەکارهێنەر"
    username = f"@{user.username}" if user.username else "نەدیار"

    if user_id not in users_db:
        users_db[user_id] = {
            "balance": 0,
            "subscription": None,
            "sub_expiry": None,
            "username": username,
            "nickname": nickname
        }
    
    await check_expiry(user_id)
    user_data = users_db[user_id]

    # پشکنینا دەمژمێرا خۆڕایی (شڤا 11 بۆ 12 ل سەر دەمێ بەغدا)
    now = get_baghdad_time()
    is_free_hour = 23 <= now.hour < 24

    # پشکنینا QR Code و Join Channel ئەگەر اشتراک هەبێت یان دەمژمێرا خۆڕایی بیت
    if is_free_hour or user_data["subscription"] or user_id in OWNERS:
        welcome_message = (
            f"بەڕێز {nickname}، بە خێر هاتیت بۆ بۆتی فەرمی!\n\n"
            f"🎉 دەمژمێرا خۆڕایی یان اشتراکا تە یا چالاکە!\n"
            f"🔗 ئەڤەش لینکا QR Code یا تایبەت ب تە (Join Channel):\n"
            f"👉 https://t.me/your_channel_or_qr_link\n\n"
            f"💰 باڵانسا تە: `{user_data['balance']}` دینار\n"
            f"👑 خودانێن بۆتی: {OWNER_TAGS}"
        )
        keyboard = [
            [InlineKeyboardButton("💳 کڕینا اشتراکان", callback_data="buy_subs")],
            [InlineKeyboardButton("👤 ژمارە و زانیاریێن من", callback_data="my_info")],
        ]
    else:
        welcome_message = (
            f"بەڕێز {nickname}، بە خێر هاتیت!\n\n"
            f"❌ تو ناتوانی QR Code ببینیت ژ بەر کو اشتراکا تە نینە یان باڵانسا تە نەسافە.\n"
            f"💰 باڵانسا تە: `{user_data['balance']}` دینار\n"
            f"گەلەک سادە یە، بۆ بینینا QR Code پێدڤییە اشتراکەکێ بکڕی یان چاڤەڕێی دەمژمێرا خۆڕایی بکەی (شەڤ ژ 11 بۆ 12).\n\n"
            f"👑 خودانێن بۆتی: {OWNER_TAGS}"
        )
        keyboard = [
            [InlineKeyboardButton("💳 کڕینا اشتراکان", callback_data="buy_subs")],
            [InlineKeyboardButton("👤 ژمارە و زانیاریێن من", callback_data="my_info")],
        ]

    if user_id in OWNERS:
        keyboard.append([InlineKeyboardButton("⚙️ پانێلا ڕێڤەبەریێ (Admin Panel)", callback_data="admin_panel")])

    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(welcome_message, reply_markup=reply_markup, parse_mode="Markdown")
    elif update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(welcome_message, reply_markup=reply_markup, parse_mode="Markdown")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id

    await check_expiry(user_id)

    if data == "my_info":
        user = query.from_user
        user_data = users_db[user_id]
        info_text = (
            f"📌 **زانیاریێن ئەکاونتا تە:**\n"
            f"👤 ناڤ (Nickname): {user.first_name}\n"
            f"🆔 ئایدی (ID): `{user.id}`\n"
            f"🔗 یۆزەرسەید (Username): @{user.username if user.username else 'نەدیار'}\n"
            f"💰 باڵانس: `{user_data['balance']}` دینار\n"
            f"📦 اشتراکا چالاک: {user_data['subscription'] or 'چ نینە'}"
        )
        keyboard = [[InlineKeyboardButton("⬅️ ڤەڕەقی بۆ پەیەجا سەرەکی", callback_data="back_start")]]
        await query.edit_message_text(info_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data == "buy_subs":
        sub_text = (
            "💳 **لیستا اشتراکان و بوهایێن وان:**\n\n"
            "1️⃣ اشتراکا 1 حەیڤ: 5,000 دینار\n"
            "2️⃣ اشتراکا 6 حەیڤ: 15,000 دینار\n"
            "3️⃣ اشتراکا 1 سال: 25,000 دینار\n"
            "4️⃣ اشتراکا هەتا هەتایێ: 60,000 دینار\n\n"
            "بۆ کڕینێ، سەرەدانَا هەردوو خودانان بکەن بۆ دانانا باڵانسێ:\n"
            "👑 @Y2_KRD یان @B4llam"
        )
        keyboard = [
            [InlineKeyboardButton("کڕینا 1 حەیڤ (5,000)", callback_data="sub_1m")],
            [InlineKeyboardButton("کڕینا 6 حەیڤ (15,000)", callback_data="sub_6m")],
            [InlineKeyboardButton("کڕینا 1 سال (25,000)", callback_data="sub_1y")],
            [InlineKeyboardButton("کڕینا هەتا هەتایێ (60,000)", callback_data="sub_life")],
            [InlineKeyboardButton("⬅️ ڤەڕەقی بۆ پەیەجا سەرەکی", callback_data="back_start")]
        ]
        await query.edit_message_text(sub_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data.startswith("sub_"):
        prices = {"sub_1m": 5000, "sub_6m": 15000, "sub_1y": 25000, "sub_life": 60000}
        durations = {"sub_1m": 30, "sub_6m": 180, "sub_1y": 365, "sub_life": 36500}
        cost = prices[data]
        
        if users_db[user_id]["balance"] >= cost:
            users_db[user_id]["balance"] -= cost  # پارە سفر دبت یان کێم دبت ژ باڵانسی
            days = durations[data]
            users_db[user_id]["sub_expiry"] = get_baghdad_time() + timedelta(days=days)
            users_db[user_id]["subscription"] = data
            
            success_text = "✅ پەیاما سەرکەفتنێ! اشتراکا تە هاتە چالاککرن و باڵانسا تە هاتە نووکرن."
            keyboard = [[InlineKeyboardButton("⬅️ ڤەڕەقی بۆ پەیەجا سەرەکی", callback_data="back_start")]]
            await query.edit_message_text(success_text, reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            fail_text = f"❌ باڵانسا تە نە بسە بۆ ڤی کریارێ! پێدڤییە باڵانسا تە بگەهتە {cost} دیناران. سەرەدانَا @Y2_KRD یان @B4llam بکە."
            keyboard = [[InlineKeyboardButton("⬅️ ڤەڕەقی بۆ پەیەجا سەرەکی", callback_data="back_start")]]
            await query.edit_message_text(fail_text, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "admin_panel" and user_id in OWNERS:
        admin_text = (
            "⚙️ **پانێلا ڕێڤەبەریێ (Admin Panel):**\n\n"
            "بۆ زێدەکرنا باڵانسێ بۆ بەکارهێنەرەکی، ڤی فەرمانێ بکار بئینە:\n"
            "`/addbalance [USER_ID] [AMOUNT]`\n\n"
            "بۆ بینینا گشت کەسێن اشتراک کڕین (Expire / Active List):\n"
            "/subscribers"
        )
        keyboard = [[InlineKeyboardButton("⬅️ ڤەڕەقی بۆ پەیەجا سەرەکی", callback_data="back_start")]]
        await query.edit_message_text(admin_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data == "back_start":
        await start(update, context)

async def add_balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if user_id not in OWNERS:
        await update.message.reply_text("❌ تو نینە ڕێڤەبەر!")
        return

    try:
        args = context.args
        target_id = int(args[0])
        amount = int(args[1])

        if target_id in users_db:
            users_db[target_id]["balance"] += amount
            await update.message.reply_text(f"✅ سەرکەفتن! بڕێ {amount} دینار هاتە زێدەکرن بۆ باڵانسا ئایدی: `{target_id}`", parse_mode="Markdown")
        else:
            await update.message.reply_text("❌ ئەڤ ئایدییە د سیستەمی دا نینە (پێدڤییە بەکارهێنەر ئێکسەر `/start` ل بۆتی لێدابیت).")
    except Exception:
        await update.message.reply_text("⚠️ فۆرماتا ناسرۆست! بکار بئینە: `/addbalance [ID] [AMOUNT]`", parse_mode="Markdown")

async def list_subscribers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if user_id not in OWNERS:
        return

    text = "📋 **لیستا گشت بەکارهێنەرێن اشتراک کڕین (Expire & Active):**\n\n"
    count = 0
    for uid, udata in users_db.items():
        if udata["subscription"]:
            count += 1
            text += f"👤 {udata['nickname']} (ID: `{uid}`)\n📦 جۆر: {udata['subscription']}\n⏳ مابوون: {udata['sub_expiry']}\n\n"
    
    if count == 0:
        text += "چ کەسێن اشتراک نینە."

    await update.message.reply_text(text, parse_mode="Markdown")

def main() -> None:
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addbalance", add_balance))
    app.add_handler(CommandHandler("subscribers", list_subscribers))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("بۆت دەستپێکر و ب تەمامی کار دکەت...")
    app.run_polling()

if __name__ == "__main__":
    main()
