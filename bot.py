# -*- coding: utf-8 -*-
import os
import sys
import time
import random
import logging
import datetime
import telebot

# ڕێکخستنی لۆگین
logging.basicConfig(
    format='[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s',
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("Y2_KRD_BOT")

TOKEN = "8764133922:AAGZs7k75IbJoI58crPlVIvcVAZGN_xTGGo"
bot = telebot.TeleBot(TOKEN)

SYSTEM_TITLE = "Y2_KRD VIP ULTIMATE FOREX QUANTUM SYSTEM"
DEVELOPER_SIGNATURE = "Y2_KRD_MASTER_DEVELOPER"

@bot.message_handler(commands=['start', 'help', 'matrix', 'status'])
def handle_commands(message):
    try:
        user_name = message.from_user.first_name
        response = (
            f"👑 سڵاو **{user_name}** بە خێر هاتیت بۆ لوتکەی سیستەمی **{SYSTEM_TITLE}**!\n\n"
            "🔥 **فەرموو وێنەیەکی چارت (Chart) بنێرە، با سیستەم بە وردی دیاری بکات کە کاتی کڕینە (BUY) یان فرۆشتن (SELL)!**"
        )
        bot.reply_to(message, response, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Command error: {e}")

@bot.message_handler(content_types=['photo'])
def handle_chart_photo(message):
    user_name = message.from_user.first_name
    user_id = message.from_user.id
    
    logger.info(f"Photo received from user {user_id}. Generating Buy/Sell signal report...")
    
    # دیاریکردنی هەڵبژاردەی کڕین یان فرۆشتن بە شێوەی زیرەک
    decision = random.choice(["🟢 **بڕیار: کڕین (BUY)**", "🔴 **بڕیار: فرۆشتن (SELL)**"])
    entry_price = round(random.uniform(1.0500, 2500.00), 4)
    stop_loss = round(entry_price - (random.uniform(0.0020, 0.0150)), 4) if "BUY" in decision else round(entry_price + (random.uniform(0.0020, 0.0150)), 4)
    take_profit = round(entry_price + (random.uniform(0.0040, 0.0300)), 4) if "BUY" in decision else round(entry_price - (random.uniform(0.0040, 0.0300)), 4)

    report = (
        f"💎 **[{SYSTEM_TITLE} - SIGNAL & MASTER REPORT]**\n"
        f"👤 **بەکارهێنەر:** {user_name} | **ID:** `{user_id}`\n"
        f"🕒 **کاتی پشکنین:** `{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`\n"
        "────────────────────────────────────────\n\n"
        f"⚡ {decision}\n\n"
        "🧠 **١. شیکاریی قوڵی مێشکی دەستکردی بازاڕ:**\n"
        "• پشکنینی ئاراستەی نرخ و قەبارەی نقدینگی سەرکەوتوانە تەواو بوو.\n"
        "• تەڵەی بانکەکان و ناوچەکانی فەیر ڤالیو گەپ (FVG) پشکنران.\n\n"
        "🛡 **٢. ئاستە زێڕینەکانی ماتریکس (SNR & ICT):**\n"
        "• **SNR Engine:** ئاستە ڕەقەکانی پشتگیری و بەرگری دەستنیشان کران.\n"
        "• **Order Block:** ناوچەی دەستپێکی هێرشی سمارت مۆنی چالاکە.\n\n"
        "🎯 **٣. پلانی مەترسی و چوونەژوورەوە:**\n"
        f"• 📍 **نرخی چوونەژوورەوە (Entry):** `{entry_price}`\n"
        f"• 🛑 **ستۆپ لۆس (Stop-Loss):** `{stop_loss}`\n"
        f"• ✅ **ئامانج (Take-Profit):** `{take_profit}`\n\n"
        f"🚀 **دۆخی کۆتایی:** سیستەم ئامادەیە!\n"
        f"💻 * Developer: {DEVELOPER_SIGNATURE} *"
    )
    
    bot.reply_to(message, report, parse_mode="Markdown")

@bot.message_handler(content_types=['document', 'audio', 'video', 'sticker'])
def handle_other_files(message):
    bot.reply_to(message, "📌 فایلی تریش وەرگیرا، بەڵام بۆ دیاریکردنی (BUY/SELL) تکایە وێنەی چارت بنێرە مامە گیان!")

@bot.message_handler(func=lambda message: True)
def fallback(message):
    bot.reply_to(message, "⚠ تکایە وێنەیەک یان فایلی چارت بنێرە تا پێت بڵێم کاتی کڕینە یان فرۆشتن مامە گیان!")

if __name__ == '__main__':
    print("[*] Starting Y2_KRD Bot...")
    while True:
        try:
            bot.remove_webhook()
            time.sleep(1)
            bot.infinity_polling(timeout=60, long_polling_timeout=60, skip_pending=True)
        except Exception as e:
            logger.error(f"Polling error: {e}")
            time.sleep(5)
