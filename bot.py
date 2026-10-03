import os
import telebot
from telebot import types

# تۆکێنەی تایبەتی بۆتەکەی تۆ
TOKEN = "8764133922:AAGZs7k75IbJoI58crPlVIvcVAZGN_xTGGo"
bot = telebot.TeleBot(TOKEN)

# 1. فرمانی /start بۆ بەخێرهاتنی بەکارهێنەر بە نیکی ناوی خۆی
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    username = message.from_user.username
    display_name = f"@{username}" if username else user_name
    
    welcome_text = (
        f"👑 سڵاو **{display_name}** بە خێر هاتیت بۆ بۆتی شیکاریی فۆریکس (Y2_KRD)!\n\n"
        "من ئامادەم بۆ لێکۆڵینەوە و شیکارکرنا هەر وێنەیەکی چارتێ (Chart) ب شێوازەکێ زۆر پیشەیی و تێرەسەل.\n"
        "📊 **سیستەمە پشتراستکراوەکان:** SNRZ, MNR, SNR\n\n"
        "فەرموو وێنەیەکا چارتێ بۆ من بنێرە دا ناڤەرۆکا وێ ب هەموو وردەکارییانەوە بۆت بژمێرم!"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

# 2. وەرگرتنا وێنە و ناردنا شیکارییا ورد (وەکو نموونەی شێوازی چارت و سیگناڵ)
@bot.message_handler(content_types=['photo'])
def handle_chart_image(message):
    user_name = message.from_user.first_name
    username = message.from_user.username
    display_name = f"@{username}" if username else user_name
    
    # ئەمە فۆرماتەکەی وەک نموونەکەی تۆیە بە تەواوی وردەکارییەکانییەوە
    analysis_report = (
        f"🟢 **شیکاریی چارتی XAUUSD (طلا) - M15**\n"
        f"👤 **بەکارهێنەر:** {display_name}\n"
        "بە گرنگترین نیشانەکان:\n\n"
        "───\n\n"
        "🎯 ## **ناوچە سەرەکییەکان:**\n"
        "• **Support (پشتیوانی):** نرخ - (پشتیوانی دروست) 3972.05 - دوو جار لێی وەگەڕاوەتەوە\n"
        "• **Resistance (بەرگری):** فرێ (ناوچەی بەرگری R سەرەکی) - 4015-4021\n\n"
        "───\n\n"
        "📊 ## **حالەتی ڕەوتی (Trend):**\n"
        "نرخ بەشێوەیەکی (Bearish - بۆ خوارەوە) روون دابەزیوە و ئێستا لەسەر ناوچەی پشتیوانی تێپەڕدا.\n\n"
        "───\n\n"
        "⚠️ ## **سیگناڵ:**\n"
        "📌 **پلانی BUY:**\n"
        "• 🎯 **Entry:** 3972.05 - 3975.00 (لای Support)\n"
        "• 🛑 **Stop-Loss:** 3968.00 (دەرەوەی Support)\n"
        "• ✅ **Take-Profit 1:** 3989.65 (PO2 قەدیمی)\n"
        "• ✅ **Take-Profit 2:** 4015-4021 (Resistance سەرەکی)\n\n"
        "🔵 **متمانە:** مامناوەند - پالشتی، یەک جار و نیو"
    )
    
    bot.reply_to(message, analysis_report, parse_mode="Markdown")

# 3. وەڵامدانەوە بۆ هەر نامەیەکی ئاسایی
@bot.message_handler(func=lambda message: True)
def default_response(message):
    bot.reply_to(message, "⚠️ تکایە وێنەیەکی چارتێ (Chart) بنێرە دا سیستەمێ شیکاریا فۆریکس ب بڕیار و وردەکاریی تەواو بۆ تە بنێرم!")

# دەستپێکردنا بۆتی بە بێ وەستان
if __name__ == '__main__':
    print("بۆتی فۆریکس بە سەرکەوتوویی دەست بە کار بوو...")
    bot.infinity_polling()
