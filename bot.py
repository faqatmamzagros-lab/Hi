import logging
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# ڕێکخستنی لۆگین
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# کلیلی API و لینکی ڕاستەقینە
RAPIDAPI_KEY = "46e03b483cmshbe7c266140e84e4p1fefd2jsn5758012a82a8"
RAPIDAPI_HOST = "tiktok-api23.p.rapidapi.com"

# ئۆنر و کەناڵی پشتگیری
OWNERS = "👨‍💻 Owners: @YUSEEF_SURCHI | @B4llam"
CHANNEL = "📢 Channel: @Tikinfo_krd"

# دەقی بەخێراتن بە زمانی کوردیی سۆرانی
WELCOME_MESSAGE = f"""
👋🏻 بە خێر بێیت بۆ بۆتی زانیارییەکانی تيك تۆک 👋🏻

👨🏼‍💻 یەکەمین بۆت لە جیهاندا کە سەرجەم تایبەتمەندییەکان لە خۆ دەگرێت. دەتوانیت هەموو زانیارییەکانی خاوەنی هەژمارەکە بزانیت وەک:

🔹 ناوی هەژمار
🔸 یۆزەری هەژمار 
✅ نیشانەی باوەڕپێکراوی (توثيق) 
📆 مێژووی دروستکردنی هەژمار 
⌚️ مێژووی گۆڕینی ناوی هەژمار 
🥇 ئاستی پشتگیری لە پەخشە ڕاستەوخۆکان (البثوث) 
💭 بایۆ (Bio) 
📍 وڵاتی هەژمار 
💬 زمانی هەژمار 
👫 ژمارەی هاوڕێکان 
👤 ژمارەی شوێنکەوتووکان (متابعين) 
👥 ژمارەی شوێنکەوتراوەکان (مضافين) 
👍 کۆۆی لایکەکان 
📺 ژمارەی ڤیدیۆکان 
🔴 پەخشی ڕاستەوخۆ (Live) 
🔢 ئایدی ژووری پەخش 
👀 ژمارەی بینەرانی پەخش 
🌟 ژمارەی بەشداربووانی ئەستێرە 
🎟️ ژمارەی بەشداربووانی تیپی خاوەن پەخش 
📛 ئایدی هەژمار (ID) 
🔑 ئایدی دووەم (الثانوي)

🚀 تایبەتمەندییە پێشکەوتووەکان:

• 🌐 دۆزینەوەی هەژمارە سزادراو و قەدەغەکراوەکان (محظورة)
• 💬 دۆزینەوەی ئەو هەژمارانەی لە بنکەدراوەی تیکتۆکدا نیین
• 🙂 زانینی وڵاتی ڕاستەقینە + شوێنی ئێستای هەژمار
↳ لە کاتی بەکارهێنانی VPNـدا جیاوازییەکان ئاشکرا دەکرێن و ئاگادارت دەکەینەوە

• 🎵 زانینی ئایا هەژمارەکە مۆسیقییە یان نەخێر
• ✅ ئاشکراکردنی جۆری باوەڕپێکراوی تایبەت (وەک: دروستکەری بەناوبانگ)
• ▶️ زانینی بوونی کەناڵی یوتیوبی بەستراوە
• 🟡 زانینی بوونی هەژماری انستاگرامی بەستراوە
• ⛔ زانینی ئەگەری ئەنجامدانی منشن بۆ هەژمارەکە لە لێدوانەکاندا
• 📖 زانینی ئایا هەژمارەکە ستۆریی تێدایە یان نەخێر

🤝 خۆت باقی خەسڵەتەکان بدۆزەوە و تاقیان بکەرەوە! 

✅ یۆزەر، ئایدی، ئایدی دووەم، بەستەری پەخش، یان بەستەری ڤیدیۆییەک بنێرە، تا سەرجەم زانیارییەکانت بۆ بنێرم 📊

---------------------------
{OWNERS}
{CHANNEL}
"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await update.message.reply_text(WELCOME_MESSAGE)


async def handle_tiktok_query(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
  query = update.message.text.strip()

  # لێرەدا دەتوانین یۆزەر لە پەیامەکە دەربهێنین (بۆ نموونە ئەگەر بەستەر بوو یان یۆزەری ڕووت بوو)
  if "tiktok.com" in query:
    # لێرە بە شێوازێکی سادە یۆزەر دەردەهێنین یان بە نموونە کار دەکەین
    # دەتوانیت لە داهاتوودا لینکی تیکتۆک شیکار بکەیت
    username = "taylorswift"
  else:
    username = query.replace("@", "")

  url = "https://tiktok-api23.p.rapidapi.com/api/user/info"
  querystring = {"uniqueId": username}
  headers = {"x-rapidapi-host": RAPIDAPI_HOST, "x-rapidapi-key": RAPIDAPI_KEY}

  await update.message.reply_text("⏳ چاوەڕێ بە، خەریکە سەرجەم زانیارییەکان دەهێنم...")

  try:
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    # دەرهێنانی زانیارییە فراوانەکان لە APIـیەکەوە
    user_info = data.get("userInfo", {})
    user_detail = user_info.get("user", {})
    stats = user_info.get("stats", {})

    # زانیارییە وردەکان
    nickname = user_detail.get("nickname", "نەزانراو")
    signature = user_detail.get("signature", "بوونی نییە")
    sec_uid = user_detail.get("secUid", "نەزانراو")
    user_id = user_detail.get("id", "نەزانراو")
    verified = (
        "✅ بەڵێ (مووثق)" if user_detail.get("verified") else "❌ نەخێر"
    )
    region = user_detail.get("region", "نەزانراو")

    followers = stats.get("followerCount", 0)
    following = stats.get("followingCount", 0)
    hearts = stats.get("heart", 0)
    videos = stats.get("videoCount", 0)
    friends = stats.get("friendCount", 0)

    # دروستکردنی پەیامی کۆتایی بە هەموو زانیارییەکانەوە
    result_text = (
        f"📊 **سەرجەم زانیارییەکانی هەژماری تیکتۆک:**\n\n"
        f"🔹 **ناوی هەژمار:** {nickname}\n"
        f"🔸 **یۆزەر:** @{username}\n"
        f"📛 **ئایدی هەژمار (ID):** {user_id}\n"
        f"🔑 **ئایدی دووەم (SecUid):** {sec_uid}\n"
        f"✅ **التوثيق (تاییدکراو):** {verified}\n"
        f"📍 **وڵاتی هەژمار:** {region}\n"
        f"💭 **بایۆ (Bio):** {signature}\n\n"
        f"👤 **ژمارەی شوێنکەوتووکان (متابعين):** {followers:,}\n"
        f"👥 **ژمارەی مضافين (Followings):** {following:,}\n"
        f"👫 **ژمارەی هاوڕێکان (Friends):** {friends:,}\n"
        f"❤️️ **کۆی لایکەکان:** {hearts:,}\n"
        f"🎬 **ژمارەی ڤیدیۆکان:** {videos:,}\n\n"
        f"---------------------------\n"
        f"{OWNERS}\n"
        f"{CHANNEL}"
    )

    await update.message.reply_text(result_text)

  except Exception as e:
    await update.message.reply_text(
        f"❌ هەڵەیەک ڕوویدا لە هێنانی زانیارییەکان.\n\n---------------------------\n{OWNERS}\n{CHANNEL}"
    )
    print(f"Error: {e}")


def main():
  # تۆکنی بۆتەکەت لێرە دابنە
  TOKEN = "8868899334:AAGsbrI61_s7hasbA-dvoUD54JZ31dHd6mI"  # تۆکنی ڕاستەقینەی خۆت لێرە دابنە

  app = ApplicationBuilder().token(TOKEN).build()

  app.add_handler(CommandHandler("start", start))
  app.add_handler(
      MessageHandler(filters.TEXT & ~filters.COMMAND, handle_tiktok_query)
  )

  print("Bot is running...")
  app.run_polling()


if __name__ == "__main__":
  main()
