import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
import requests

# ڕێکخستنی لۆگین
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# کلیلی API و لینکی ڕاستەقینە
RAPIDAPI_KEY = "46e03b483cmshbe7c266140e84e4p1fefd2jsn5758012a82a8"
RAPIDAPI_HOST = "tiktok-api23.p.rapidapi.com"

# دەقی بەخێراتن بە زمانی کوردیی سۆرانی
WELCOME_MESSAGE = """
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
↳ لە کاتی بەکارهێنانی VPNـدا جیاوازییەکان ئاشکرا دەکرێن و ئاگادارت دەكەینەوە

• 🎵 زانینی ئایا هەژمارەکە مۆسیقییە یان نەخێر
• ✅ ئاشکراکردنی جۆری باوەڕپێکراوی تایبەت (وەک: دروستکەری بەناوبانگ)
• ▶️ زانینی بوونی کەناڵی یوتیوبی بەستراوە
• 🟡 زانینی بوونی هەژماری ئینستاگرامی بەستراوە
• ⛔ زانینی ئەگەری ئەنجامدانی منشن بۆ هەژمارەکە لە لێدوانەکاندا
• 📖 زانینی ئایا هەژمارەکە ستۆریی تێدایە یان نەخێر

🤝 خۆت باقی خەسڵەتەکان بدۆزەوە و تاقیان بکەرەوە! 

✅ یۆزەر، ئایدی، ئایدی دووەم، بەستەری پەخش، یان بەستەری ڤیدیۆییەک بنێرە، تا سەرجەم زانیارییەکانت بۆ بنێرم 📊
"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await update.message.reply_text(WELCOME_MESSAGE)


async def handle_tiktok_query(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
  query = update.message.text.strip()

  # ئەگەر پەیامەکە بەستەر بوو یان یۆزەری تیکتۆک بوو
  if "tiktok.com" in query:
    await update.message.reply_text(
        "⏳ بەستەرەکەت پێگەیشت، خەریکە زانیارییەکان دەهێنم..."
    )
    # لێرە دەتوانیت بەستەرەکە پاکبکەیتەوە بۆ دەرهێنانی یۆزەر یان ڤیدیۆ
    username = "taylorswift"  # نموونە
  else:
    username = query.replace("@", "")

  url = "https://tiktok-api23.p.rapidapi.com/api/user/info"
  querystring = {"uniqueId": username}
  headers = {"x-rapidapi-host": RAPIDAPI_HOST, "x-rapidapi-key": RAPIDAPI_KEY}

  try:
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    user_info = data.get("userInfo", {})
    stats = user_info.get("stats", {})

    nickname = user_info.get("user", {}).get("nickname", "نەزانراو")
    followers = stats.get("followerCount", 0)
    following = stats.get("followingCount", 0)
    hearts = stats.get("heart", 0)
    videos = stats.get("videoCount", 0)

    result_text = (
        f"👤 **ناوی هەژمار:** {nickname}\n"
        f"🔗 **یۆزەر:** @{username}\n\n"
        f"👥 **فۆڵۆوەر:** {followers:,}\n"
        f"👤 **فۆڵۆوینگ:** {following:,}\n"
        f"❤️ **لایک:** {hearts:,}\n"
        f"🎬 **ڤیدیۆکان:** {videos:,}"
    )

    await update.message.reply_text(result_text, parse_mode="Markdown")

  except Exception as e:
    await update.message.reply_text(
        "❌ هەڵەیەک ڕوویدا لە وەرگرتنی زانیارییەکان. دیسان هەوڵ بدەوە."
    )
    print(f"Error: {e}")


def main():
  # تۆکنی بۆتەکەی خۆت لێرە دابنە
  TOKEN = "8868899334:AAFcfBbSYHDA5_r4iGO3rTycTNaH_yqQPOo"

  app = ApplicationBuilder().token(TOKEN).build()

  app.add_handler(CommandHandler("start", start))
  app.add_handler(
      MessageHandler(filters.TEXT & ~filters.COMMAND, handle_tiktok_query)
  )

  print("Bot is running...")
  app.run_polling()


if __name__ == "__main__":
  main()
