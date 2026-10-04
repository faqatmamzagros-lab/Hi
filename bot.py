import logging
from datetime import datetime, timedelta
import pytz
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

# تووکن و ئایدیی خاوەنەکانی بۆت (Owners)
TOKEN = "8868138985:AAGJ8_duPPPQXhBSf1DnQlImeUO-WRHSmMA"
OWNERS = [7904656691, 7643191802]
OWNER_TAGS = "@Y2_KRD و @B4llam"

# زانیاریی بەکارهێنەران لە داتابەیسەکەدا
users_db = {}

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

    # پشکنینی کاتی خۆڕایی (شەڤ لە سەعات 11 تا 12ی شەو بە کاتی بەغدا)
    now = get_baghdad_time()
    is_free_hour = 23 <= now.hour < 24

    user_link = f"https://t.me/your_bot_username?start={user_id}"

    if is_free_hour or user_data["subscription"] or user_id in OWNERS:
        welcome_message = (
            f"✨ سڵاو بەڕێز **{nickname}**، بە خێر هاتیت بۆ بۆتی فەرمی! 🌟\n\n"
            f"🎉 سەعاتی خۆڕاییی شەڤ یان اشتراکی تۆ ئێستا چالاکە!\n"
            f"🔗 گرێبەست (Link) یان کۆدی QR تایبەت بە کەناڵی تۆ:\n"
            f"👉 `https://t.me/joinchannel_qr_link`\n\n"
            f"📌 **زانیارییەکانی اکاونتی تۆ:**\n"
            f"🆔 ئایدی (ID): `{user_id}`\n"
            f"🌐 گرێبەستی تایبەت (Safari / مۆبایل): `{user_link}`\n"
            f"💰 باڵانسی تۆ: `{user_data['balance']}` دینار\n\n"
            f"👑 خاوەنەکانی بۆت: {OWNER_TAGS}"
        )
    else:
        welcome_message = (
            f"✨ سڵاو بەڕێز **{nickname}**، بە خێر هاتیت! 🌟\n\n"
            f"❌ تۆ ناتوانیت کۆدی QR ببینیت چونکە اشتراکت نییە یان باڵانست سفرە.\n"
            f"⏳ چاوەڕێی سەعاتی خۆڕایی بکە (شەڤ لە سەعات 11 تا 12) یان اشتڕاکێک بکڕە.\n\n"
            f"📌 **زانیارییەکانی اکاونتی تۆ:**\n"
            f"🆔 ئایدی (ID): `{user_id}`\n"
            f"🌐 گرێبەستی تایبەت (Safari / مۆبایل): `{user_link}`\n"
            f"💰 باڵانسی تۆ: `{user_data['balance']}` دینار\n\n"
            f"👑 خاوەنەکانی بۆت: {OWNER_TAGS}"
        )

    keyboard = [
        [InlineKeyboardButton("💳 کڕینی اشتڕاکەکان", callback_data="buy_subs")],
        [InlineKeyboardButton("👤 ژمارە و زانیارییەکانم", callback_data="my_info")],
    ]

    if user_id in OWNERS:
        keyboard.append([InlineKeyboardButton("⚙️ پەنێڵی بەڕێوەبەری (Admin Panel)", callback_data="admin_panel")])

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
        user_link = f"https://t.me/your_bot_username?start={user_id}"
        info_text = (
            f"👤 **زانیارییەکانی اکاونت و مۆبایلی تۆ:**\n\n"
            f"▫️ ناوی خوازراو (Nickname): {user.first_name}\n"
            f"🆔 ئایدی (ID): `{user.id}`\n"
            f"🔗 یۆزەرسەید: @{user.username if user.username else 'نەدیار'}\n"
            f"🌐 گرێبەستی تایبەت: `{user_link}`\n"
            f"💰 باڵانس: `{user_data['balance']}` دینار\n"
            f"📦 اشتراکی چالاک: {user_data['subscription'] or 'هیچ اشتڕاکێک نییە'}"
        )
        keyboard = [[InlineKeyboardButton("🔙 گەڕانەوە (Back)", callback_data="back_start")]]
        await query.edit_message_text(info_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data == "buy_subs":
        sub_text = (
            "💎 **لیستی اشتڕاکەکان و نرخی ئەوان:**\n\n"
            "1️⃣ اشتراکی 1 مانگ ⬅️ 5,000 دینار\n"
            "2️⃣ اشتراکی 6 مانگ ⬅️ 15,000 دینار\n"
            "3️⃣ اشتراکی 1 ساڵ ⬅️ 25,000 دینار\n"
            "4️⃣ اشتراکی بۆ هەتا هەتایێ ⬅️ 50,000 دینار\n\n"
            "💬 بۆ کڕین و زیادکردنی باڵانس، سەردانی هەردوو خاوەنی بۆت بکەن:\n"
            "👑 @Y2_KRD یان @B4llam"
        )
        keyboard = [
            [InlineKeyboardButton("🛒 کڕینی 1 مانگ (5,000)", callback_data="sub_1m")],
            [InlineKeyboardButton("🛒 کڕینی 6 مانگ (15,000)", callback_data="sub_6m")],
            [InlineKeyboardButton("🛒 کڕینی 1 ساڵ (25,000)", callback_data="sub_1y")],
            [InlineKeyboardButton("🛒 کڕینی بۆ هەتا هەتایێ (50,000)", callback_data="sub_life")],
            [InlineKeyboardButton("🔙 گەڕانەوە (Back)", callback_data="back_start")]
        ]
        await query.edit_message_text(sub_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data.startswith("sub_"):
        prices = {"sub_1m": 5000, "sub_6m": 15000, "sub_1y": 25000, "sub_life": 50000}
        durations = {"sub_1m": 30, "sub_6m": 180, "sub_1y": 365, "sub_life": 36500}
        cost = prices[data]
        
        if users_db[user_id]["balance"] >= cost:
            users_db[user_id]["balance"] -= cost  # پارە سفر دەبێتەوە یان کەم دەبێت
            days = durations[data]
            users_db[user_id]["sub_expiry"] = get_baghdad_time() + timedelta(days=days)
            users_db[user_id]["subscription"] = data
            
            success_text = "✅ پەیامی سەرکەوتوویی! اشتراکی تۆ بە سەرکەوتوویی چالاک بوو و باڵانسی تۆ سفر/نوێ کرایەوە."
            keyboard = [[InlineKeyboardButton("🔙 گەڕانەوە (Back)", callback_data="back_start")]]
            await query.edit_message_text(success_text, reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            fail_text = f"❌ باڵانسی تۆ بەس نییە! پێویستە باڵانسی تۆ بگاتە {cost} دیناران. تکایە سەردانی @Y2_KRD یان @B4llam بکە."
            keyboard = [[InlineKeyboardButton("🔙 گەڕانەوە (Back)", callback_data="back_start")]]
            await query.edit_message_text(fail_text, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "admin_panel" and user_id in OWNERS:
        admin_text = (
            "⚙️ **پەنێڵی بەڕێوەبەری (Admin Panel):**\n\n"
            "🔹 بۆ زیادکردنی باڵانس بۆ هەر بەکارهێنەرێک، ئەم فەرمانە لە چاتدا بەکار بهێنە:\n"
            "`/addbalance [ID] [بڕ]`\n\n"
            "🔹 بۆ بینینی گشت کەسەکانی کە اشتراکیان کڕیوە و ماوەی بەسەرچوونیان:\n"
            "/subscribers"
        )
        keyboard = [[InlineKeyboardButton("🔙 گەڕانەوە (Back)", callback_data="back_start")]]
        await query.edit_message_text(admin_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data == "back_start":
        await start(update, context)

async def add_balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if user_id not in OWNERS:
        await update.message.reply_text("❌ تۆ بەڕێوەبەر نییەتی!")
        return

    try:
        args = context.args
        target_id = int(args[0])
        amount = int(args[1])

        if target_id in users_db:
            users_db[target_id]["balance"] += amount
            await update.message.reply_text(f"✅ بڕی {amount} دینار بە سەرکەوتوویی بۆ ئایدی: `{target_id}` زیاد کرا.", parse_mode="Markdown")
        else:
            await update.message.reply_text("❌ ئەم ئایدییە لە سیستەمدا نییە (پێویستە بەکارهێنەر پێشتر /start لە بۆتەکەدا لێدابێت).")
    except Exception:
        await update.message.reply_text("⚠️ هەڵە لە نووسینی فەرماندا! بەکار بهێنە: `/addbalance [ID] [AMOUNT]`", parse_mode="Markdown")

async def list_subscribers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if user_id not in OWNERS:
        return

    text = "📋 **لیستی گشت بەکارهێنەرانی اشتڕاککڕاو:**\n\n"
    count = 0
    for uid, udata in users_db.items():
        if udata["subscription"]:
            count += 1
            text += f"👤 {udata['nickname']} (ID: `{uid}`)\n📦 جۆر: {udata['subscription']}\n⏳ ماوە: {udata['sub_expiry']}\n\n"
    
    if count == 0:
        text += "هیچ کەسێک اشتراکی نییە."

    await update.message.reply_text(text, parse_mode="Markdown")

def main() -> None:
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addbalance", add_balance))
    app.add_handler(CommandHandler("subscribers", list_subscribers))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("بۆت دەستپێکرد و بە تەواوی کار دەکات...")
    app.run_polling()

if __name__ == "__main__":
    main()
ID: 7643191802
