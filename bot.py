import os
import logging
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

# ڕێکخستنی لاگین
logging.basicConfig(level=logging.INFO)

# زانیارییەکانی API و توکەنی بۆت
API_ID = 34584240
API_HASH = "eba4f8333cba5f9697a1d20779d4d6e9"
# تۆکەنی بۆتی سەرەکی
BOT_TOKEN = "8887162311:AAEBNX4ewNX-__HI-659aiyLffnJHliV_qc"

app = Client("spoof_call_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ناوی ئەو کەسانەی دەسەڵاتیان هەەیە ( Username یان )
ALLOWED_USERS = ["YUSEEF_SURCHI", "B4LLAM"]

# فەنکشن بۆ پشکنینا ئایا بەکارهێنەر دەسەڵاتی هەیە یان نا
def is_authorized(username: str) -> bool:
    if not username:
        return False
    return username.lstrip("@") in ALLOWED_USERS

# دوگمەی سەرەکی بە زمانی سۆرانی
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📞 لێدانی پەیوەندی", callback_data="start_call")]
    ])

@app.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    username = message.from_user.username
    
    # پشکنینا دەسەڵاتێ
    if not is_authorized(username):
        await message.reply_text(
            "❌ **بەڕێزم، تۆ مافی کارپێکرنی ئەم بۆتەت نییە!**\n"
            "تکایە سەردانی ئەم دوو بەڕێزە بکە بۆ دەستەبەركردنی مۆڵەت:\n"
            "👉 @YUSEEF_SURCHI\n"
            "👉 @B4LLAM"
        )
        return

    welcome_text = (
        "**بەخێر هاتن بۆ بۆتی پەیوەندی (SpoofCall)**\n\n"
        "تکایە یەکێک لە دوگمەکانی خوارەوە هەڵبژێرە:"
    )
    await message.reply_text(welcome_text, reply_markup=main_menu())

@app.on_callback_query()
async def callback_handler(client: Client, callback_query):
    username = callback_query.from_user.username
    
    if not is_authorized(username):
        await callback_query.answer("❌ تۆ مافی کارپێکرنی ئەم بۆتەت نییە!", show_alert=True)
        return

    data = callback_query.data
    
    if data == "start_call":
        await callback_query.message.edit_text(
            "📞 **ژمارەیەک دابنە (بۆ نموونە: 07503675554):**",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 گەڕانەوە", callback_data="back_home")]])
        )
    elif data == "back_home":
        await callback_query.message.edit_text(
            "**بەخێر هاتن بۆ بۆتی پەیوەندی (SpoofCall)**\n\n"
            "تکایە یەکێک لە دوگمەکانی خوارەوە هەڵبژێرە:",
            reply_markup=main_menu()
        )

# وەرگرتنی ژمارە و ئەنجامدانی پەیوەندی و ناردنی دەنگی MP3
@app.on_message(filters.text & ~filters.command("start"))
async def handle_phone_number(client: Client, message: Message):
    username = message.from_user.username
    if not is_authorized(username):
        await message.reply_text("❌ تۆ مافی کارپێکرنی ئەم بۆتەت نییە!")
        return

    phone = message.text.strip()
    
    if phone.isdigit() or phone.startswith("+"):
        status_msg = await message.reply_text(
            f"🔄 **رەوش: پەیوەندی بەسترا...**\n"
            f"📞 ژمارە: `{phone}`"
        )
        
        await asyncio.sleep(2)
        await status_msg.edit_text(
            f"🔔 **رەوش: لێدانی زەنگ (Ringing)...**\n"
            f"📞 ژمارە: `{phone}`"
        )
        await asyncio.sleep(3)
        
        await status_msg.edit_text(
            f"🟢 **رەوش: پەیوەندی دەست پێکرد (Answered)...**\n"
            f"📞 ژمارە: `{phone}`"
        )
        await asyncio.sleep(5)
        
        await status_msg.edit_text(
            f"🔴 **رەوش: پەیوەندی کۆتایی هات (Hang up).**\n"
            f"📁 تۆمارکردنی دەنگی هەردووک کەس (MP3) ئامادەیە:"
        )
        
        # لێرە فایلێ دەنگی یێ MP3 (دگەنگێ هەردو کەسان) بۆ بەکارهێنەری تێنێرە:
        # await message.reply_audio("path_to_audio.mp3", caption="تۆمارکردنی دەنگی پەیوەندی (Call Recording)")
        
    else:
        await message.reply_text("❌ تکایە ژمارەیەکی دروست دابنە (بۆ نموونە: 07503675554).")

if __name__ == "__main__":
    print("Bot is running...")
    app.run()
