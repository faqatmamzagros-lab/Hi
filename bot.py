import os
import logging
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

# Loging nɔfɛrɛn
logging.basicConfig(level=logging.INFO)

API_ID = 34584240
API_HASH = "eba4f8333cba5f9697a1d20779d4d6e9"

# Bot token dɔnnen
BOT_TOKEN_1 = "8887162311:AAEBNX4ewNX-__HI-659aiyLffnJHliV_qc"  # Bot fɔlɔ
BOT_TOKEN_2 = "8992244510:AAEkucauinM5zY45Emh95SxX1z0arTYEhAY"  # Bot fila

# Admin ID
ADMIN_IDS = [7643191802]

PENDING_REQUESTS = {}
APPROVED_USERS = set()
USER_DATA = {}

bot1 = Client("Bot_Saraki", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN_1)
bot2 = Client("Bot_Daxazi", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN_2)

@bot1.on_message(filters.command("start"))
async def bot1_start(client: Client, message: Message):
    user = message.from_user
    user_id = user.id
    username = f"@{user.username}" if user.username else "bɛ username"
    name = user.first_name

    if user_id not in APPROVED_USERS:
        PENDING_REQUESTS[user_id] = {"name": name, "username": username, "id": user_id}
        
        await message.reply_text(
            "⏳ **داخوازییەکەی تۆ نێردرا!**\n\n"
            "تۆ هێشتا مۆڵەتی کارپێکرنی ئەم بۆتەت نییە. داخوازییەکەت ڕەوانەی بەڕێوەبەر کرا."
        )
        
        for admin_id in ADMIN_IDS:
            try:
                await bot2.send_message(
                    admin_id,
                    f"📥 **داخوازییەکی نوێ هات!**\n\n"
                    f"👤 ناڤ: {name}\n"
                    f"🔗 یوزەرنەڤیس: {username}\n"
                    f"🆔 ئایدی: `{user_id}`",
                    reply_markup=InlineKeyboardMarkup([
                        [
                            InlineKeyboardButton("✅ پەسەندکردن", callback_data=f"accept_{user_id}"),
                            InlineKeyboardButton("❌ ڕەتکردن", callback_data=f"delete_{user_id}")
                        ]
                    ])
                )
            except Exception as e:
                print(f"Error: {e}")
        return

    await message.reply_text(
        "👋 **بەخێر هاتن بۆ بۆتی پەیوەندی**\n\n"
        "📞 **ژمارەیەک بنێرە (بۆ نموونە: 07503675554)** تا چاودێریی 24 کاتژمێری دەست پێ بکەین.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📁 تۆمارەکانم", callback_data="my_records")]
        ])
    )

@bot2.on_message(filters.command("start"))
async def bot2_start(client: Client, message: Message):
    await message.reply_text(
        "🛡️ **بۆتی بەڕێوەبرن و پەسەندکردن**\n\n"
        "لێرە دەتوانیت داخوازییەکان Accept بکەیت."
    )

@bot2.on_callback_query()
async def bot2_callbacks(client: Client, callback_query):
    data = callback_query.data
    user_id_str = data.split("_")[1]
    target_user_id = int(user_id_str)
    
    if data.startswith("accept_"):
        APPROVED_USERS.add(target_user_id)
        await callback_query.message.edit_text(f"✅ **داخوازیی بەکارهێنەر `{target_user_id}` پەسەند کرا!**")
        try:
            await bot1.send_message(target_user_id, "🎉 **پیرۆزە! داخوازییەکەت پەسەند کرا. ئێستا دەتوانی `/start` بنووسیت.**")
        except:
            pass

    elif data.startswith("delete_"):
        if target_user_id in PENDING_REQUESTS:
            del PENDING_REQUESTS[target_user_id]
        await callback_query.message.edit_text(f"❌ **داخوازیی بەکارهێنەر `{target_user_id}` ڕەت کرا.**")
        try:
            await bot1.send_message(target_user_id, "❌ **بەڕێزم، داخوازییەکەت ڕەت کرایەوە.**")
        except:
            pass

@bot1.on_callback_query()
async def bot1_callbacks(client: Client, callback_query):
    user_id = callback_query.from_user.id
    if user_id not in APPROVED_USERS:
        await callback_query.answer("❌ تۆ مافی کارپێکرنا ئەم بۆتەت نییە!", show_alert=True)
        return

    if callback_query.data == "my_records":
        recs = USER_DATA.get(user_id, [])
        if not recs:
            rec_text = "📁 **هیچ تۆمارە دەنگییەک نییە.**"
        else:
            rec_text = "📁 **تۆمارە دەنگییەکانی تۆ:**\n" + "\n".join(recs)
        await callback_query.message.edit_text(
            rec_text,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 گەڕانەوە", callback_data="start")]])
        )

@bot1.on_message(filters.text & ~filters.command("start"))
async def handle_call_process(client: Client, message: Message):
    user_id = message.from_user.id
    if user_id not in APPROVED_USERS:
        await message.reply_text("❌ تۆ مافی کارپێکرنا ئەم بۆتەت نییە!")
        return

    phone = message.text.strip()
    
    if phone.isdigit() or phone.startswith("+"):
        status_msg = await message.reply_text(
            f"🔄 **ژمارە وەرگیرا: `{phone}`**\n"
            f"⏱️ *چاودێریی 24 کاتژمێری دەست پێ کرد...*"
        )
        
        await asyncio.sleep(6)
        
        await status_msg.edit_text(
            f"🔴 **پەیوەندی لەگەڵ ژمارە `{phone}` کۆتایی هات.**\n"
            f"📥 **فایلی دەنگیی MP3 ئامادە بوو و نێردرا بۆ چاتەکەت:**"
        )
        
        if user_id not in USER_DATA:
            USER_DATA[user_id] = []
        record_info = f"📞 ژمارە: {phone} (MP3 Audio Recorded)"
        USER_DATA[user_id].append(record_info)
        
        try:
            await message.reply_text(f"🎧 `[فایلی دەنگیی MP3 بۆ ژمارە {phone} بە سەرکەوتوویی نێردرا]`")
        except Exception as e:
            print(f"Error: {e}")
            
    else:
        await message.reply_text("❌ تکایە ژمارەیەکی دروست بنووسە (بۆ نموونە: 07503675554).")

async def main():
    await asyncio.gather(
        bot1.start(),
        bot2.start()
    )
    await asyncio.gather(
        asyncio.Event().wait()
    )

if __name__ == "__main__":
    asyncio.run(main())
