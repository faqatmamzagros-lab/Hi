import os
import logging
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

# ڕێکخستنی لاگین
logging.basicConfig(level=logging.INFO)

# API Zanyari
API_ID = 34584240
API_HASH = "eba4f8333cba5f9697a1d20779d4d6e9"

# Bot 1 (Sərəki) & Bot 2 (Daxazi u Scan) Tokens
BOT_TOKEN_1 = "8887162311:AAEBNX4ewNX-__HI-659aiyLffnJHliV_qc"
BOT_TOKEN_2 = "8992244510:AAEkucauinM5zY45Emh95SxX1z0arTYEhAY"

# دەسەڵاتدارێن بۆتا سەرەکی
ALLOWED_USERS = ["YUSEEF_SURCHI", "B4LLAM"]

# Database یان فەرهەنگا دەمک بۆ تۆمارکرنا یوزەران و فایلێن دەنگی
USER_DATABASE = {}
CALL_RECORDINGS = {}

app = Client("spoof_main_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN_1)

def is_authorized(username: str) -> bool:
    if not username:
        return False
    return username.lstrip("@") in ALLOWED_USERS

# دوگمەیێن سەرەکی (2 Buttons)
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📞 لێدانی پەیوەندی و ژمارە", callback_data="start_call")],
        [InlineKeyboardButton("📁 تۆمارەکان (Recordings)", callback_data="view_recordings")],
        [InlineKeyboardButton("🔙 گەڕانەوە", callback_data="back_home")]
    ])

@app.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    user = message.from_user
    username = user.username or "N/A"
    user_id = user.id
    
    # سکەنکرنا سۆراوچاوى و تۆمارکرنا زانیارییان بۆ ئەمنیەتێ (Bot 2 Log Logic)
    logging.info(f"[SECURITY SCAN] User started bot -> ID: {user_id}, Username: @{username}, Name: {user.first_name}")
    
    if not is_authorized(username):
        await message.reply_text(
            "❌ **بەڕێزم، تۆ مافی کارپێکرنی ئەم بۆتەت نییە!**\n"
            "تکایە داواکاری بنێرە بۆ ئەم دوو بەڕێزە:\n"
            "👉 @YUSEEF_SURCHI\n"
            "👉 @B4LLAM"
        )
        return

    welcome_text = (
        "**بەخێر هاتن بۆ بۆتی پەیوەندی (SpoofCall Pro)**\n\n"
        "تکایە یەکێک لە دوگمەکانی خوارەوە هەڵبژێرە:"
    )
    await message.reply_text(welcome_text, reply_markup=main_menu())

@app.on_callback_query()
async def callback_handler(client: Client, callback_query):
    user = callback_query.from_user
    username = user.username or "N/A"
    
    if not is_authorized(username):
        await callback_query.answer("❌ تۆ مافی کارپێکرنی ئەم بۆتەت نییە!", show_alert=True)
        return

    data = callback_query.data
    
    if data == "start_call":
        await callback_query.message.edit_text(
            "📞 **ژمارەیەک دابنە (بۆ نموونە: 07503675554):**\n"
            "*(تێبینی: پەیوەندی پاش 24 دەمژمێران یان لە کاتی تەواوبوون بە شێوەی خۆکار Hang up دەبێت و دەنگی هەردووک کەس بە MP3 دەنێردرێت)*",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 گەڕانەوە", callback_data="back_home")]])
        )
    elif data == "view_recordings":
        # نیشاندانا تۆمارێن دەنگی یێن هە هەمی ژمارەیان
        recs = CALL_RECORDINGS.get(user.id, [])
        if not recs:
            rec_text = "📁 **هیچ تۆمارێکی دەنگی تا ئێستا نییە.**"
        else:
            rec_text = "📁 **تۆمارە دەنگییەکانی پاشەکەوتکراو:**\n" + "\n".join(recs)
            
        await callback_query.message.edit_text(
            rec_text,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 گەڕانەوە", callback_data="back_home")]])
        )
    elif data == "back_home":
        await callback_query.message.edit_text(
            "**بەخێر هاتن بۆ بۆتی پەیوەندی (SpoofCall Pro)**\n\n"
            "تکایە یەکێک لە دوگمەکانی خوارەوە هەڵبژێرە:",
            reply_markup=main_menu()
        )

# وەرگرتنا ژمارەیێ، چاودێریا 24 دەمژمێری و خلاسکرنا خۆتۆماری (Hang up)
@app.on_message(filters.text & ~filters.command("start"))
async def handle_phone_number(client: Client, message: Message):
    user = message.from_user
    username = user.username or "N/A"
    
    if not is_authorized(username):
        await message.reply_text("❌ تۆ مافی کارپێکرنی ئەم بۆتەت نییە!")
        return

    phone = message.text.strip()
    
    if phone.isdigit() or phone.startswith("+"):
        status_msg = await message.reply_text(
            f"🔄 **رەوش: پەیوەندی بۆ ژمارە {phone} دەست پێکرد...**\n"
            f"⏱️ *(سیستەم چاودێری 24 کاتژمێری دەکات)*"
        )
        
        # simulated call process & 24h/automatic hangup logic framework
        await asyncio.sleep(3)
        await status_msg.edit_text(f"🟢 **رەوش: پەیوەندی چالاکە (Live) بۆ {phone}...**")
        
        # لێرە پاش ماوەیەک یان تەواوبوونا پەیوەندیێ (Hang up خۆتۆکار)
        await asyncio.sleep(5)
        
        await status_msg.edit_text(
            f"🔴 **رەوش: پەیوەندی بە شێوەی خۆکار کۆتایی هات (Auto Hang up).**\n"
            f"📁 تۆمارکردنی دەنگی هەردووک کەس (MP3) ئامادەیە:"
        )
        
        # تۆمارکرنا ناڤێ فایلێ دەنگی د ליستا بەکارهێنەری دا
        if user.id not in CALL_RECORDINGS:
            CALL_RECORDINGS[user.id] = []
        CALL_RECORDINGS[user.id].append(f"📞 ژمارە: {phone} (MP3 Ready)")
        
        # await message.reply_audio("path_to_audio.mp3", caption=f"تۆمارکردنی دەنگی {phone}")
    else:
        await message.reply_text("❌ تکایە ژمارەیەکی دروست دابنە.")

if __name__ == "__main__":
    print("Bot 1 and Bot 2 security framework running...")
    app.run()
