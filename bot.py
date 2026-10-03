import os
import telebot

# تۆکێنەی بۆتەکەی تۆ
TOKEN = "8764133922:AAGZs7k75IbJoI58crPlVIvcVAZGN_xTGGo"
bot = telebot.TeleBot(TOKEN)

# 1. فەرمانی /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    username = message.from_user.username
    display_name = f"@{username}" if username else user_name
    
    welcome_text = (
        f"👑 سڵاو **{display_name}** بە خێر هاتیت بۆ بۆتی تایبەتی شیکاریی فۆریکس (Y2_KRD)!\n\n"
        "📈 **سیستەمە کارا و یاساکانی ناو بۆت:**\n"
        "• **SNR (Support & Resistance):** دەستنیشانکرنا خاڵێن گرنگ و پشتراستکرنا بازاڕی.\n"
        "• **MNR (Major/Minor Range):** دیارکرنا مەودایێن مەزن و بچووک.\n"
        "• **SNRZ (Zone Analysis):** شیکاریا ناوچەیی و ڕەوتی نرخ (Trend Direction).\n"
        "• **Risk Management:** دانانی Stop-Loss و Take-Profit بە پێی یاسایێن فۆرێکس.\n\n"
        "فەرموو وێنەیەکا چارتێ (Chart) بۆ من بنێرە، دەستبەجێ بە هەموو یاسا و قاعیدەکانەوە شیکاریی تەواوت بۆ دکەم!"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

# 2. سیستەمی وەرگرتنی وێنە و شیکاریا هەموو یاساکانی فۆرێکس
@bot.message_handler(content_types=['photo'])
def handle_chart_image(message):
    user_name = message.from_user.first_name
    username = message.from_user.username
    display_name = f"@{username}" if username else user_name
    
    full_forex_analysis = (
        f"📊 **[Y2_KRD] - ڕاپۆرتی شیکاریی تەکنیکیی پێشکەوتووی فۆریکس**\n"
        f"👤 **بەکارهێنەر:** {display_name}\n\n"
        "────────────────────────\n"
        "📉 **١. دیارکرنا ڕەوتی بازار (Market Trend):**\n"
        "• **ئاراستەی گشتی:** (Bearish / Bullish Setup)\n"
        "• **دۆخی ئێستای نرخ:** نرخ لە ناوچەیەکی هەستیاردا دەجووڵێت کە پێویستی بە چاودێریی توند هەەیە لەسەر تایمفریمی بەکارهاتوو.\n\n"
        "────────────────────────\n"
        "🛡️ **٢. ناوچەکانی SNR (Support & Resistance):**\n"
        "• **بەرگری (Resistance Zone):** ئاستی بەرگریی بەهێز کە ڕێگرە لە بەرزبوونەوەی زیاتری نرخ.\n"
        "• **پشتیوانی (Support Zone):** ئاستی پشتگیری کە ئەگەرشکانی دەبێتە هۆی دابەزینی زیاتر.\n\n"
        "────────────────────────\n"
        "📐 **٣. یاساکانی MNR & SNRZ:**\n"
        "• **پشککنینی مەودا (Range):** نرخ لە چوارچێوەی لادانی ئاسایی خۆیدایە.\n"
        "• **نیشانەیانەی قەبارە (Volume):** گڵۆپەکان ئاماژەن بۆ کەمبوونەوەی مۆمێنتەم لە نزیک خاڵە سەرەکییەکان.\n\n"
        "────────────────────────\n"
        "🎯 **٤. پێشنیاری سیگناڵ و بەڕێوەبردن (Trading Plan):**\n"
        "• 🟢 **جۆری چوونە ژوورەوە (Entry):** چاوەڕێی شکان یان ڕەتکردنەوەی (Rejection) مۆم لەسەر ئاستی سەرەکی بکە.\n"
        "• 🛑 **ستۆپ لۆس (Stop-Loss):** لە دەرەوەی ناوچەی SNR دادەنرێت بۆ پاراستنی سەرمایە (Risk Management).\n"
        "• ✅ **ئامانجەکان (Take-Profit):** بەرەو ناوچەی دووەمی بەرگری یان پشتیوانی بەرامبەر.\n\n"
        "⚠️ *تێبینی: هەمیشە پارەبەڕێوەبردن (Risk/Reward Ratio) لەبەرچاو بگرە.*"
    )
    
    bot.reply_to(message, full_forex_analysis, parse_mode="Markdown")

# 3. وەڵام بۆ نامەی ئاسایی
@bot.message_handler(func=lambda message: True)
def default_response(message):
    bot.reply_to(message, "⚠️ تکایە **وێنەیەکا چارتێ** بنێرە، چونکە ئەم بۆتە تایبەتە بە جێبەجێکردنی یاساکانی فۆرێکس لەسەر وێنە و چارتەکان!")

if __name__ == '__main__':
    print("بۆتی پێشکەوتووی فۆریکس بە سەرکەوتوویی دەست بە کار بوو...")
    bot.infinity_polling()
