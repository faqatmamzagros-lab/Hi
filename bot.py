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

# Towoken o id-i khawanezani bot (Owners)
TOKEN = "8868138985:AAGJ8_duPPPQXhBSf1DnQlImeUO-WRHSmMA"
BOT_USERNAME = "SYSTEM_EYE_OF_TELEGRAM_BOT"  #irak luga apnar bot-er asli username (bina @)
OWNERS = [7904656691, 7643191802]
OWNER_TAGS = "@Y2_KRD o @B4llam"

# Zaniyari-i bakarheneran la database-ekada
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
    nickname = user.first_name if user.first_name else "Bakarhener"
    username = f"@{user.username}" if user.username else "Nedyar"

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
            f"✨ Slaw barez **{nickname}**[span_4](start_span)[span_4](end_span), ba xer hatit bo boti fermi! 🌟[span_5](start_span)[span_5](end_span)\n\n"
            f"🎉 Eshtraki to esta la halati chalakdaye[span_6](start_span)[span_6](end_span)!\n"
            f"🔗 Girebest (Link) yan kodi QR taybet ba kanali to:[span_7](start_span)[span_7](end_span)\n"
            f"👉 `https://t.me/joinchannel_qr_link`[span_8](start_span)[span_8](end_span)\n\n"
            f"📌 **Zaniyari-i-akanuti to:**[span_9](start_span)[span_9](end_span)\n"
            f"🆔 Aydi (ID): `{user_id}`[span_10](start_span)[span_10](end_span)\n"
            f"🌐 Girebesti taybet (Safari / mobayl): `{user_link}`[span_11](start_span)[span_11](end_span)\n"
            f"💰 Balansi to: `{user_data['balance']}` dinar[span_12](start_span)[span_12](end_span)\n\n"
            f"👑 Xawanekani bot: {OWNER_TAGS}[span_13](start_span)[span_13](end_span)"
        )
    else:
        welcome_message = (
            f"✨ Slaw barez **{nickname}**[span_14](start_span)[span_14](end_span), ba xer hatit bo boti fermi! 🌟\n\n"
            f"❌ Bo binini QR Code o bakarhenani boteke, pewiste eshtrarek bkrit.\n"
            f"💎 Takaya yakek la eshtrakean halbjere bo bardewambun.\n\n"
            f"📌 **Zaniyari-i-akanuti to:**[span_15](start_span)[span_15](end_span)\n"
            f"🆔 Aydi (ID): `{user_id}`[span_16](start_span)[span_16](end_span)\n"
            f"🌐 Girebesti taybet (Safari / mobayl): `{user_link}`[span_17](start_span)[span_17](end_span)\n"
            f"💰 Balansi to: `{user_data['balance']}` dinar[span_18](start_span)[span_18](end_span)\n\n"
            f"👑 Xawanekani bot: {OWNER_TAGS}[span_19](start_span)[span_19](end_span)"
        )

    keyboard = [
        [InlineKeyboardButton("💳 Krini eshtrakean", callback_data="buy_subs")],
        [InlineKeyboardButton("👤 Zhmara o zaniyariyekanm", callback_data="my_info")],
    ]

    if user_id in OWNERS:
        keyboard.append([InlineKeyboardButton("⚙️ Peneli berreweberi (Admin Panel)", callback_data="admin_panel")])

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
        sub_status = user_data["subscription"] if check_user_active(user_id) else "Hich eshtrarek niye"
        info_text = (
            f"👤 **Zaniyari-i-akanut o mobayli to:**\n\n"
            f"▫️ Nawi xwazraw (Nickname): {user.first_name}\n"
            f"🆔 Aydi (ID): `{user.id}`\n"
            f"🔗 Yozerset: @{user.username if user.username else 'Nedyar'}\n"
            f"🌐 Girebesti taybet: `{user_link}`\n"
            f"💰 Balans: `{user_data['balance']}` dinar\n"
            f"📦 Eshtraki chalak: {sub_status}"
        )
        keyboard = [[InlineKeyboardButton("🔙 Garandewe (Back)", callback_data="back_start")]]
        await query.edit_message_text(info_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data == "buy_subs":
        sub_text = (
            "💎 **Listi eshtrakean o narxi ewan:**\n\n"
            "1️⃣ Eshtraki 1 mang ⬅️ 5,000 dinar\n"
            "2️⃣ Eshtraki 6 mang ⬅️️ 15,000 dinar\n"
            "3️⃣ Eshtraki 1 sal ⬅️ 25,000 dinar\n"
            "4️⃣ Eshtraki bo hata hetaye ⬅️ 50,000 dinar\n\n"
            "💬 Bo krin o ziyadkardni balans, sardani hardwu xawani bot bkan:\n"
            "👑 @Y2_KRD yan @B4llam"
        )
        keyboard = [
            [InlineKeyboardButton("🛒 Krini 1 mang (5,000)", callback_data="sub_1m")],
            [InlineKeyboardButton("🛒 Krini 6 mang (15,000)", callback_data="sub_6m")],
            [InlineKeyboardButton("🛒 Krini 1 sal (25,000)", callback_data="sub_1y")],
            [InlineKeyboardButton("🛒 Krini bo hata hetaye (50,000)", callback_data="sub_life")],
            [InlineKeyboardButton("🔙 Garandewe (Back)", callback_data="back_start")]
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
            
            success_text = "✅ Peyami sarkewtuwi! Eshtraki to ba sarkewtuwi chalak bow o balansi to safar/nwe krayewe."
            keyboard = [[InlineKeyboardButton("🔙 Garandewe (Back)", callback_data="back_start")]]
            await query.edit_message_text(success_text, reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            fail_text = f"❌ Balansi to bas niye! Pewiste balansi to bgate {cost} dinaran. Takaya sardani @Y2_KRD yan @B4llam bkan."
            keyboard = [[InlineKeyboardButton("🔙 Garandewe (Back)", callback_data="back_start")]]
            await query.edit_message_text(fail_text, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "admin_panel" and user_id in OWNERS:
        admin_text = (
            "⚙️ **Peneli berreweberi (Admin Panel):**\n\n"
            "🔹 Bo ziyadkardni balans bo har bakarhenerik, am fermane la chatda bakar henene:\n"
            "`/addbalance [ID] [br]`\n\n"
            "🔹 Bo binini gst kesakani ke eshtrakian kriwe o mawei basarchuniayan:\n"
            "/subscribers"
        )
        keyboard = [[InlineKeyboardButton("🔙 Garandewe (Back)", callback_data="back_start")]]
        await query.edit_message_text(admin_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data == "back_start":
        await start(update, context)

async def add_balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if user_id not in OWNERS:
        await update.message.reply_text("❌ To berreweber niyeti!")
        return

    try:
        args = context.args
        target_id = int(args[0])
        amount = int(args[1])

        if target_id in users_db:
            users_db[target_id]["balance"] += amount
            await update.message.reply_text(f"✅ Bri {amount} dinar ba sarkewtuwi bo aydi: `{target_id}` ziyad kra.", parse_mode="Markdown")
        else:
            await update.message.reply_text("❌ Am aydi-ye la systemda niye (pewiste bakarhener peshter /start la botekada ledabit).")
    except Exception:
        await update.message.reply_text("⚠️ Hala la nusini fermanda! Bakar henene: `/addbalance [ID] [AMOUNT]`", parse_mode="Markdown")

async def list_subscribers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if user_id not in OWNERS:
        return

    text = "📋 **Listi gst bakarhenerani eshtraknakraw:**\n\n"
    count = 0
    for uid, udata in users_db.items():
        if check_user_active(uid):
            count += 1
            text += f"👤 {udata['nickname']} (ID: `{uid}`)\n📦 Jor: {udata['subscription']}\n⏳ Mawa: {udata['sub_expiry']}\n\n"
    
    if count == 0:
        text += "Hich kesik eshtraki niye."

    await update.message.reply_text(text, parse_mode="Markdown")

def main() -> None:
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addbalance", add_balance))
    app.add_handler(CommandHandler("subscribers", list_subscribers))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot destpıkrd o ba tawawi kar dekat...")
    app.run_polling()

if __name__ == "__main__":
    main()
