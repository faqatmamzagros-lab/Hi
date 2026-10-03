# -*- coding: utf-8 -*-
import os
import sys
import time
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
            "🔥 **فەرموو وێنەیەکی چارت (Chart) بنێرە، با سیستەم شیکاریت بۆ ئەنجام بدات!**"
        )
        bot.reply_to(message, response, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Command error: {e}")

@bot.message_handler(content_types=['photo', 'document', 'audio', 'video', 'sticker'])
def handle_chart_analysis(message):
    try:
        user_name = message.from_user.first_name
        user_id = message.from_user.id
        
        logger.info(f"Processing chart analysis for user {user_id}...")
        
        report = (
            f"💎 **[{SYSTEM_TITLE} - TRANSCENDENCE MASTER REPORT]**\n"
            f"👤 **بەکارهێنەر:** {user_name} | **ID:** `{user_id}`\n"
            f"🕒 **کاتی پشکنین:** `{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`\n"
            "────────────────────────────────────────\n\n"
            "🧠 **١. شیکاریی قوڵی مێشکی دەستکردی بازاڕ:**\n"
            "• پشکنینی تەواوی تایمفریمەکان سەرکەوتوانە ئەنجام درا.\n"
            "• قەبارەی نقدینگی و پەستانی کڕین/فرۆشتن لە دۆخێکی جێگیردایە.\n\n"
            "🛡 **٢. ناوچەکانی (SNR, MNR, SNRZ Matrix):**\n"
            "• **SNR Engine:** ئاستە ڕەقەکانی پشتگیری و بەرگری دەستنیشان کران.\n"
            "• **SNRZ Zone:** ناوچەی پەرچەکرداری بانکە جیهانییەکان چالاکە.\n\n"
            "⚙️️ **٣. کۆنسێپتەکانی SMC & ICT:**\n"
            "• **BOS & ChoCH:** پێکهاتەی بازاڕ و خاڵە حەساسەکانی وەرچەرخان پشتڕاستکرانەوە.\n"
            "• **FVG & Order Blocks:** ناوچە ڤاکیووم و ئۆردەر بلاکەکان دۆزرانەوە.\n\n"
            "🎯 **٤. پلانی مەترسی و چوونەژوورەوەی زێڕین:**\n"
            "• 🟢 **خاڵی چوونەژوورەوە:** لە ناوچەی پەسەندکراوی ئۆتۆماتیکی.\n"
            "• 🛑 **Stop-Loss:** پاراستنی پارە لە دەرەوەی تەڵەی بانکەکان.\n"
            "• ✅ **Take-Profit Targets:** ئامانجەکانی نزیک و مەزن بە سیستەمی Risk-Reward بەرز.\n\n"
            f"🚀 **دۆخی کۆتایی:** شیکارییەکە بە سەرکەوتوویی تەواو بوو!\n"
            f"💻 * Developer: {DEVELOPER_SIGNATURE} *"
        )
        
        bot.reply_to(message, report, parse_mode="Markdown")
        logger.info("Chart analysis report sent successfully.")
        
    except Exception as err:
        logger.error(f"Error in handle_chart_analysis: {err}")
        bot.reply_to(message, "⚠ هەڵەیەک ڕوویدا، بەڵام سیستەمەکە کار دەکات. تکایە دووبارە وێنەکە بنێرە.")

@bot.message_handler(func=lambda message: True)
def fallback(message):
    bot.reply_to(message, "⚠ تکایە وێنەیەک یان فایلی چارت بنێرە تا شیکاریت بۆ بکەم مامە گیان!")

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
