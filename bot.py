import os
import logging
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

# ڕێکخستنی لاگین (Logging setup)
logging.basicConfig(level=logging.INFO)

# زانیارییەکانی بۆت و ئەی پی ئای
API_ID = 34584240
API_HASH = "eba4f8333cba5f9697a1d20779d4d6e9"
BOT_TOKEN = "8887162311:AAEBNX4ewNX-__HI-659aiyLffnJHLiV_qc"

app = Client("spoof_call_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# دروستکردنی دوگمەی سەرەکی
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📞 لێدانی پەیوەندی", callback_data="start_call")],
        [InlineKeyboardButton("🔙 گەڕانەوە", callback_data="back_home")]
    ])

@app.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    welcome_text = (
        "**بەخێر هاتن بۆ بۆتی پەیوەندی**\n\n"
        "تکایە یەکێک لە دوگمەکانی خوارەوە هەڵبژێرە:"
    )
    await message.reply_text(welcome_text, reply_markup=main_menu())

@app.on_callback_query()
async def callback_handler(client: Client, callback_query):
    data = callback_query.data
    
    if data == "start_call":
        await callback_query.message.edit_text(
            "📞 **ژمارەیەک دابنە (بۆ نموونە: 07503675554):**",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 گەڕانەوە", callback_data="back_home")]])
        )
    elif data == "back_home":
        await callback_query.message.edit_text(
            "**بەخێر هاتن بۆ بۆتی پەیوەندی**\n\n"
            "تکایە یەکێک لە دوگمەکانی خوارەوە هەڵبژێرە:",
            reply_markup=main_menu()
        )

# وەرگرتنی ژمارە و نیشاندانی ڕەوش و ناردنی دەنگی بە MP3
@app.on_message(filters.text & ~filters.command("start"))
async def handle_phone_number(client: Client, message: Message):
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
            f"📁 تۆمارکردنی دەنگی ئامادەیە:"
        )
        
        # بۆ ناردنی فایلی دەنگی MP3 دەتوانیت ئەم ڕێنماییە بەکاربهێنیت:
        # await message.reply_audio("path_to_audio.mp3", caption="تۆمارکردنی پەیوەندی (Call Recording)")
        
    else:
        await message.reply_text("❌ تکایە ژمارەیەکی دروست دابنە (بۆ نموونە: 07503675554).")

if __name__ == "__main__":
    print("Bot is running...")
    app.run()
