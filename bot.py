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
TOKEN = "8868138985:AAEs0BnrQX9QxyvY_hgFeEqAOsrxk2iCJ1M"
BOT_USERNAME = "SYSTEM_EYE_OF_TELEGRAM_BOT"  # یۆزەرسەیدێ بۆتا خۆ ل ڤێرە بنڤیسە بێ @
OWNERS = [7904656691, 7643191802]
OWNER_TAGS = "@Y2_KRD و @B4llam"

# داتابەیسا بەکارهێنەران
users_db = {}

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

def get_baghdad_time():
    tz = pytz.timezone("Asia/Baghdad")
    return datetime.now(tz)

def check_user_active(user_id):
    if user_id in OWNERS:
        return True
    if user_id in users_db:
        sub_expiry = users_db[user_id].get("sub_expiry")
        if sub_expiry:
            if get_baghdad_time() < sub_expiry:
                return True
            else:
                users_db[user_id]["subscription"] = None
                users_db[user_id]["sub_expiry"] = None
    return False

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
    
    user_data = users_db[user_id]
    is_active = check_user_active(user_id)
    user_link = f"https://t.me/{BOT_USERNAME}?start={user_id}"

    if is_active:
        welcome_message = (
            f"✨ سڵاو بەڕێز **{nickname}**، بە خێر هاتیت بۆ بۆتی فەرمی! 🚀\n\n"
            f"💎 اشتراکی تۆ ئێستا لە حاڵەتی چالاکدایە و دەتوانیت تەواوی خزمەتگوزارییەکان بەکار بهێنیت!\n\n"
            f"📌 **زانیارییەکانی ئەکاونتی تۆ:**\n"
            f"🆔 ئایدی (ID): `{user_id}`\n"
            f"🌐 لینکی تایبەت (Safari / مۆبایل): `{user_link}`\n"
            f"💰 باڵانسی تۆ: `{user_data['balance']}` دینار\n\n"
            f"👑 خاوەنەکانی بۆت: {OWNER_TAGS}"
        )
        keyboard = [
            [InlineKeyboardButton("⚡️️ دروستکردنی QR Code (١)", callback_data="make_qr_1"),
             InlineKeyboardButton("⚡️ دروستکردنی QR Code (٢)", callback_data="make_qr_2")],
            [InlineKeyboardButton("⚡️️ دروستکردنی QR Code (٣)", callback_data="make_qr_3"),
             InlineKeyboardButton("⚡️ دروستکردنی QR Code (٤)", callback_data="make_qr_4")],
            [InlineKeyboardButton("👤 ژمارە و زانیارییەکانم", callback_data="my_info")],
            [InlineKeyboardButton("💳 نوێکردنەوەی اشتڕاک", callback_data="buy_subs")]
        ]
    else:
        welcome_message = (
            f"✨ سڵاو بەڕێز **{nickname}**، بە خێر هاتیت بۆ بۆتی فەرمی! 🚀\n\n"
            f"❌ اشتراکی تۆ بەسەرچووە یان هیچ اشتڕاکێکت نییە.\n"
            f"⚡️ تکایە لە دوگمەی خوارەوە جۆرێک لە اشتڕاکەکان هەڵبژێرە بۆ کڕین و چالاککردنەوەی بۆتەکە!\n\n"
            f"📌 **زانیارییەکانی ئەکاونتی تۆ:**\n"
            f"🆔 ئایدی (ID): `{user_id}`\n"
            f"🌐 لینکی تایبەت: `{user_link}`\n"
            f"💰 باڵانسی تۆ: `{user_data['balance']}` دینار\n\n"
            f"👑 خاوەنەکانی بۆت: {OWNER_TAGS}"
        )
        keyboard = [
            [InlineKeyboardButton("💎 کڕینی اشتڕاکەکان (لیست)", callback_data="buy_subs")],
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

    if data == "my_info":
        user = query.from_user
        user_data = users_db[user_id]
        user_link = f"https://t.me/{BOT_USERNAME}?start={user_id}"
        sub_status = user_data["subscription"] if check_user_active(user_id) else "❌ هیچ اشتڕاکێکت نییە"
        info_text = (
            f"👤 **زانیارییەکانی ئەکاونت و مۆبایلی تۆ:**\n\n"
            f"▫️ ناوی خوازراو: {user.first_name}\n"
            f"🆔 ئایدی (ID): `{user.id}`\n"
            f"🔗 یۆزەرسەید: @{user.username if user.username else 'نەدیار'}\n"
            f"🌐 لینکی تایبەت: `{user_link}`\n"
            f"💰 باڵانس: `{user_data['balance']}` دینار\n"
            f"📦 اشتراکی چالاک: {sub_status}"
        )
        keyboard = [[InlineKeyboardButton("🔙 گەڕانەوە", callback_data="back_start")]]
        await query.edit_message_text(info_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data == "buy_subs":
        sub_text = (
            "💎 **لیستی اشتڕاکەکان و نرخی ئەوان:**\n\n"
            "👇 تکایە جۆرێک هەڵبژێرە بۆ کڕین:\n\n"
            "1️⃣ اشتراکی ١ مانگ ⬅️ ٥,٠٠٠ دینار\n"
            "2️⃣ اشتراکی ٦ مانگ ⬅️ ١٥,٠٠٠ دینار\n"
            "3️⃣ اشتراکی ١ ساڵ ⬅️ ٢٥,٠٠٠ دینار\n"
            "4️⃣ اشتراکی بۆ هەتا هەتایێ ⬅️️ ٥٠,٠٠٠ دینار\n\n"
            "💬 بۆ زیادکردنی باڵانس، سەردانی خاوەنەکانی بۆت بکەن:\n"
            "👑 @Y2_KRD یان @B4llam"
        )
        keyboard = [
            [InlineKeyboardButton("🛒 کڕینی ١ مانگ (٥,٠٠٠ دینار)", callback_data="sub_1m")],
            [InlineKeyboardButton("🛒 کڕینی ٦ مانگ (١٥,٠٠٠ دینار)", callback_data="sub_6m")],
            [InlineKeyboardButton("🛒 کڕینی ١ ساڵ (٢٥,٠٠٠ دینار)", callback_data="sub_1y")],
            [InlineKeyboardButton("🛒 کڕینی بۆ هەتا هەتایێ (٥٠,٠٠٠ دینار)", callback_data="sub_life")],
            [InlineKeyboardButton("🔙 گەڕانەوە", callback_data="back_start")]
        ]
        await query.edit_message_text(sub_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data.startswith("sub_"):
        prices = {"sub_1m": 5000, "sub_6m": 15000, "sub_1y": 25000, "sub_life": 50000}
        durations = {"sub_1m": 30, "sub_6m": 180, "sub_1y": 365, "sub_life": 36500}
        cost = prices[data]
        
        if users_db[user_id]["balance"] >= cost:
            users_db[user_id]["balance"] -= cost
            days = durations[data]
            users_db[user_id]["sub_expiry"] = get_baghdad_time() + timedelta(days=days)
            users_db[user_id]["subscription"] = data
            
            success_text = (
                f"✅ **پەیامی سەرکەوتوویی!**\n\n"
                f"🎉 اشتراکی تۆ بە سەرکەوتوویی کڕرا و چالاک بوو!\n"
                f"⚡️ ئێستا بۆتەکە بە تەواوی بۆت کار دەکات و دەتوانیت QR Code دروست بکەیت.\n\n"
                f"💰 باڵانسی ماوەی تۆ: `{users_db[user_id]['balance']}` دینار"
            )
            keyboard = [[InlineKeyboardButton("🔙 گەڕانەوە بۆ سەرەتا", callback_data="back_start")]]
            await query.edit_message_text(success_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
        else:
            fail_text = (
                f"❌ **باڵانسی تۆ بەس نییە!**\n\n"
                f"پێویستە باڵانسی تۆ بگاتە `{cost}` دیناران بۆ کڕینی ئەم اشتڕاکە.\n"
                f"تکایە بۆ پڕکردنەوەی باڵانسی خۆت سەردانی @Y2_KRD یان @B4llam بکە."
            )
            keyboard = [[InlineKeyboardButton("🔙 گەڕانەوە بۆ لیستی اشتڕاکەکان", callback_data="buy_subs")]]
            await query.edit_message_text(fail_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data.startswith("make_qr_"):
        if check_user_active(user_id):
            qr_text = f"⚡️ QR Code دروستکرا بە سەرکەوتوویی بۆ خزمەتگوزاری ({data[-1]})!\n🔗 لینک: `https://t.me/joinchannel_qr_link`"
            keyboard = [[InlineKeyboardButton("🔙 گەڕانەوە", callback_data="back_start")]]
            await query.edit_message_text(qr_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
        else:
            await start(update, context)

    elif data == "admin_panel" and user_id in OWNERS:
        admin_text = (
            "⚙️ **پەنێڵی بەڕێوەبەری (Admin Panel):**\n\n"
            "🔹 بۆ زیادکردنی باڵانس بۆ هەر بەکارهێنەرێک، ئەم فەرمانە لە چاتدا بەکار بهێنە:\n"
            "`/addbalance [ID] [بڕ]`\n\n"
            "🔹 بۆ بینینی گشت کەسێن اشتراک کڕین:\n"
            "/subscribers"
        )
        keyboard = [[InlineKeyboardButton("🔙 گەڕانەوە", callback_data="back_start")]]
        await query.edit_message_text(admin_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data == "back_start":
        await start(update, context)

async def add_balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if user_id not in OWNERS:
        await update.message.reply_text("❌ تۆ بەڕێوەبەر نیت!")
        return

    try:
        args = context.args
        target_id = int(args[0])
        amount = int(args[1])

        if target_id in users_db:
            users_db[target_id]["balance"] += amount
            await update.message.reply_text(f"✅ بڕی `{amount}` دینار بە سەرکەوتوویی بۆ ئایدی `{target_id}` زیاد کرا.", parse_mode="Markdown")
        else:
            await update.message.reply_text("❌ ئەم ئایدییە لە سیستەمدا نییە (پێویستە بەکارهێنەر پێشتر /start لە بۆتەکەدا لێدابێت).")
    except Exception:
        await update.message.reply_text("⚠️ هەڵە لە فۆرماتی فەرمانەکە! بەکار بهێنە: `/addbalance [ID] [بڕ]`", parse_mode="Markdown")

async def list_subscribers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if user_id not in OWNERS:
        return

    text = "📋 **لیستی گشت بەکارهێنەرێن اشتڕاککڕاو:**\n\n"
    count = 0
    for uid, udata in users_db.items():
        if check_user_active(uid):
            count += 1
            text += f"👤 {udata['nickname']} (ID: `{uid}`)\n📦 جۆر: {udata['subscription']}\n⏳ ماوە: {udata['sub_expiry']}\n\n"
    
    if count == 0:
        text += "هیچ کەسێک اشتراکی چالاکی نییە."

    await update.message.reply_text(text, parse_mode="Markdown")

def main() -> None:
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addbalance", add_balance))
    app.add_handler(CommandHandler("subscribers", list_subscribers))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("بۆت دەستپێکرد و بە شێوازێکی پرێمیوم و سۆرانییا پەتی کار دەکات...")
    app.run_polling()

if __name__ == "__main__":
    main()
