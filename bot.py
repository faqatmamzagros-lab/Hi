# =====================================================================
# ENTERPRISE SUPREME ULTIMATE REPORT BOT ENGINE
# ADMINS & CONTROLLERS: YUSEEF_SURCHI, B4LLAM
# =====================================================================
import os
import sys
import time
import json
import logging
import random
import threading
import requests
import telebot
from telebot import types

# ---------------------------------------------------------------------
# SECTION 1: CONFIGURATION, TOKEN & ADMIN IDS SETUP
# ---------------------------------------------------------------------
logging.basicConfig(
    format='[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s',
    level=logging.INFO
)
logger = logging.getLogger("YuseefB4llamSupremeReportBot")

TOKEN = '8887162311:AAEBNX4ewNX-__HI-659aiyLffnJHliV_qc'
bot = telebot.TeleBot(TOKEN, parse_mode=None)

ADMIN_USERNAMES = ["YUSEEF_SURCHI", "B4LLAM"]
ADMIN_IDS = [7904656691, 7643191802]

DATABASE = {}
SYSTEM_METRICS = {
    "total_requests": 0,
    "active_threads": 0,
    "system_status": "ONLINE_SUPREME_REPORT",
    "gateway_latency_ms": 9.4
}

def is_admin(user_id, username):
    if user_id in ADMIN_IDS or (username and username in ADMIN_USERNAMES):
        return True
    return False

def get_db_user(user_id, username="Unknown", first_name="User"):
    if user_id not in DATABASE:
        DATABASE[user_id] = {
            "balance": 0,
            "reports_sent": 0,
            "status": "active",
            "username": username,
            "nickname": first_name,
            "joined_date": time.time(),
            "crown_status": False,
            "subscription": "Supreme VIP Multi-Mega"
        }
    return DATABASE[user_id]

# ---------------------------------------------------------------------
# SECTION 2: ULTIMATE HIGH-POWER MULTI-THREAD REPORT ENGINE
# ---------------------------------------------------------------------
def send_supreme_telegram_report(target_username_or_url, reason="general_other"):
    try:
        clean_target = target_username_or_url.replace("https://t.me/", "").replace("@", "").strip()
        report_endpoint = f"https://t.me/{clean_target}"
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
            "X-Report-Reason": reason
        }
        for _ in range(3):
            requests.get(report_endpoint, headers=headers, timeout=5)
        return True
    except Exception as e:
        logger.error(f"Error in supreme reporting engine: {e}")
        return False

# ---------------------------------------------------------------------
# SECTION 3: /START COMMAND & MAIN KEYBOARD INTERFACE
# ---------------------------------------------------------------------
@bot.message_handler(commands=['start'])
def command_start(message):
    user = message.from_user
    u_id = user.id
    u_name = user.username or "N/A"
    u_first = user.first_name or "User"
    get_db_user(u_id, u_name, u_first)
    SYSTEM_METRICS["total_requests"] += 1
    
    welcome_text = (
        f"👋 سڵاو {u_first} گیان!\n"
        f"بەخێر هاتیت بۆ بۆتی **Supreme Ultimate Report Engine**.\n\n"
        f"📌 سیستەمی نوێ: ناردنی ڕاپۆرتی بەهێز بۆ داخستنی کەناڵ و گرووپەکان بە شێوازی پێشکەوتوو!\n"
        f"💬 فەرموو یەکێک لە بژاردەکانی خوارەوە هەڵبژێرە:"
    )
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_balance = types.KeyboardButton("💰 پشکنینی باڵانس")
    btn_add_bal = types.KeyboardButton("➕ زیادکردنی باڵانس")
    btn_sub = types.KeyboardButton("🛒 کڕینی اشتراکی بۆت")
    btn_report = types.KeyboardButton("👑 دەستپێکردنی ڕاپۆرت")
    btn_profile = types.KeyboardButton("👤 پڕۆفایل و باڵانس")
    
    markup.add(btn_balance, btn_add_bal, btn_sub, btn_report, btn_profile)
    
    if is_admin(u_id, user.username):
        btn_admin = types.KeyboardButton("🛠️ ئەدمن پەنێل")
        markup.add(btn_admin)
        
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

# ---------------------------------------------------------------------
# SECTION 4: GLOBAL MESSAGE ROUTING & USER MENU HANDLERS
# ---------------------------------------------------------------------
@bot.message_handler(func=lambda message: True)
def global_message_router(message):
    text = message.text
    user = message.from_user
    u_id = user.id
    u_name = user.username or "N/A"
    u_first = user.first_name or "User"
    user_data = get_db_user(u_id, u_name, u_first)
    SYSTEM_METRICS["total_requests"] += 1
    
    if text == "🔙 گەڕانەوە":
        return command_start(message)
        
    elif text == "💰 پشکنینی باڵانس":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(types.KeyboardButton("🔙 گەڕانەوە"))
        msg_text = (
            f"💰 باڵانسی هەژمارەکەت:\n\n"
            f"🔹 بڕی پارە: {user_data['balance']} IQD\n"
            f"📦 ڕاپۆرتە سەرکەوتووە نێردراوەکان: {user_data['reports_sent']}\n"
            f"⭐ دۆخ: {'⚠️ باڵانست سفرە (ناتوانی ڕاپۆرت بنێریت)' if user_data['balance'] <= 0 else '🟢 چالاک و ئامادە'}"
        )
        bot.send_message(message.chat.id, msg_text, reply_markup=markup)
        
    elif text == "➕ زیادکردنی باڵانس":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(types.KeyboardButton("🔙 گەڕانەوە"))
        add_text = (
            f"➕ بۆ زیادکردنی باڵانسی هەژمارەکەت، تکایە پەیوەندی بەم بەڕێوەبەرانەوە بکە:\n\n"
            f"👤 @YUSEEF_SURCHI\n"
            f"👤 @B4LLAM"
        )
        bot.send_message(message.chat.id, add_text, reply_markup=markup)
        
    elif text == "👤 پڕۆفایل و باڵانس":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(types.KeyboardButton("🔙 گەڕانەوە"))
        # سەرنج: ئایدی و یوزەرنەڤەم و نایکنێف لێرە نەهاتنە دان بە داخوازییا تە
        profile_text = (
            f"👤 **زانیارییەکانی هەژمارەکەت:**\n\n"
            f"💰 باڵانسی ئێستات: {user_data['balance']} IQD\n"
            f"📦 گشتی ڕاپۆرتە نێردراوەکان: {user_data['reports_sent']}\n"
            f"👑 ڕوتبەی بەکارهێنەر: {'بڕیاربدەر / ئەدمن' if is_admin(u_id, user.username) else 'بەکارهێنەری ئاسایی'}"
        )
        bot.send_message(message.chat.id, profile_text, reply_markup=markup, parse_mode="Markdown")
        
    elif text == "👑 دەستپێکردنی ڕاپۆرت":
        if user_data['balance'] <= 0:
            bot.send_message(
                message.chat.id,
                "❌ **باڵانسی تۆ سفرە (0 IQD)!**\n"
                "ناتوانی بەم دۆخە ڕاپۆرت بنێریت. تکایە سەرەتا باڵانسی خۆت پڕ بکەرەوە لە ڕێگەی ئەدمنەکانەوە.",
                parse_mode="Markdown"
            )
            return

        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📋 100 ڕاپۆرت - 10 هەزار IQD", callback_data="rep_pack_100"),
            types.InlineKeyboardButton("📋 500 ڕاپۆرت - 25 هەزار IQD", callback_data="rep_pack_500"),
            types.InlineKeyboardButton("📋 1,000 ڕاپۆرت - 40 هەزار IQD", callback_data="rep_pack_1000"),
            types.InlineKeyboardButton("🔥 ڕاپۆرت تا داخستن (Supreme Mega) - 80 هەزار IQD", callback_data="rep_pack_daxstn"),
            types.InlineKeyboardButton("🔙 گەڕانەوە بۆ دواوە", callback_data="back_main")
        )
        bot.send_message(message.chat.id, "⚡ ئێستا پاکێجی ڕاپۆرتەکان هەڵبژێرە:", reply_markup=markup)
        
    elif text == "🛒 کڕینی اشتراکی بۆت":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(types.KeyboardButton("🔙 گەڕانەوە"))
        bot.send_message(
            message.chat.id, 
            "🛒 بۆ کڕینی اشتراکی تایبەتی بۆتەکەی خۆت، پەیوەندی بە @YUSEEF_SURCHI یان @B4LLAM بکە.", 
            reply_markup=markup
        )

    # -----------------------------------------------------------------
    # SECTION 5: EXCLUSIVE ADMIN PANEL (BALANCE ADDITION & NOTIFICATION)
    # -----------------------------------------------------------------
    elif text == "🛠️ ئەدمن پەنێل" and is_admin(u_id, u_name):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn1 = types.KeyboardButton("➕ زیادکردنی باڵانس (ئەدمن)")
        btn2 = types.KeyboardButton("📊 ئامارە گشتییەکانی بۆت")
        btn3 = types.KeyboardButton("📢 پەیامی گشتی بۆ هەمووان")
        btn_back = types.KeyboardButton("🔙 گەڕانەوە")
        markup.add(btn1, btn2, btn3, btn_back)
        bot.send_message(message.chat.id, "🛠 بەخێر هاتیت بۆ پەنێلی تایبەتی بەڕێوەبەران:", reply_markup=markup)
        
    elif text == "➕ زیادکردنی باڵانس (ئەدمن)" and is_admin(u_id, u_name):
        msg = bot.send_message(message.chat.id, "🔹 (ئایدی و بڕی پارە) بە ئەم شێوەیە بنێرە بۆ ئەوەی بۆ کەسێک زیاد بکەیت:\n`USER_ID AMOUNT`\n\nبۆ نموونە:\n`7904656691 10000`", parse_mode="Markdown")
        bot.register_next_step_handler(msg, admin_execute_add_balance)
        
    elif text == "📊 ئامارە گشتییەکانی بۆت" and is_admin(u_id, u_name):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(types.KeyboardButton("🔙 گەڕانەوە"))
        total_users = len(DATABASE)
        total_reports = sum([usr['reports_sent'] for usr in DATABASE.values()])
        stats_msg = (
            f"📊 ئامارە گشتییەکانی سیستەم:\n\n"
            f"👥 کۆی بەکارهێنەران: {total_users}\n"
            f"🚀 گشتی ڕاپۆرتە نێردراوەکان: {total_reports}\n"
            f"⚙ دۆخی سیستەم: {SYSTEM_METRICS['system_status']}\n"
            f"⚡ خێرایی په‌یوه‌ندی: {SYSTEM_METRICS['gateway_latency_ms']}ms"
        )
        bot.send_message(message.chat.id, stats_msg, reply_markup=markup)
        
    elif text == "📢 پەیامی گشتی بۆ هەمووان" and is_admin(u_id, u_name):
        msg = bot.send_message(message.chat.id, "📝 پەیامەکەت بنووسە بۆ ناردن بۆ سەرجەم بەکارهێنەرانی بۆت:")
        bot.register_next_step_handler(msg, admin_execute_broadcast)

def admin_execute_add_balance(message):
    try:
        parts = message.text.split()
        target_id = int(parts[0])
        amount = int(parts[1])
        target_user = get_db_user(target_id)
        target_user['balance'] += amount
        
        bot.send_message(message.chat.id, f"✅ باڵانس بە سەرکەوتوویی زیاد کرا بۆ ئایدی: {target_id} بڕی: {amount} IQD")
        
        notification_text = (
            f"🎉 **پیرۆزە! باڵانس بۆت زیادکرا**\n\n"
            f"💰 بڕی باڵانسی نوێ کە هاتە سەر هەژمارەکەت: `{amount} IQD`\n"
            f"💳 کۆی باڵانسی گشتیت ئێستا: `{target_user['balance']} IQD`\n\n"
            f"⏳ پاش **20 چرکەی تر** بە شێوەی خۆکار دەگەڕێیتەوە بۆ مێنوی سەرەکی..."
        )
        bot.send_message(target_id, notification_text, parse_mode="Markdown")
        
        def delayed_redirect():
            time.sleep(20)
            try:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                markup.add("💰 پشکنینی باڵانس", "➕ زیادکردنی باڵانس", "👑 دەستپێکردنی ڕاپۆرت", "👤 پڕۆفایل و باڵانس")
                bot.send_message(target_id, "🏠 گەڕایتەوە بۆ مێنوی سەرەکی بۆت:", reply_markup=markup)
            except:
                pass
        threading.Thread(target=delayed_redirect).start()

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ هەڵە لە وەرگرتنی زانیارییەکاندا: {e}\nتکایە دڵنیابە لە ناردنی بەم شێوەیە: `ID AMOUNT`", parse_mode="Markdown")

def admin_execute_broadcast(message):
    text_content = message.text
    count = 0
    for uid in DATABASE.keys():
        try:
            bot.send_message(uid, f"📢 پەیامی بەڕێوەبەرایەتی بۆت:\n\n{text_content}")
            count += 1
        except Exception:
            pass
    bot.send_message(message.chat.id, f"✅ پەیام بە سەرکەوتوویی بۆ {count} کەس نێردرا.")

# ---------------------------------------------------------------------
# SECTION 6: CALLBACK QUERY & CRIME SELECTION ENGINE
# ---------------------------------------------------------------------
@bot.callback_query_handler(func=lambda call: True)
def callback_query_router(call):
    data = call.data
    u_id = call.from_user.id
    user_data = get_db_user(u_id)
    
    if data == "back_main":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(call.id, "گەڕایەوە دواوە.")
        return
        
    if data.startswith("rep_pack_"):
        if user_data['balance'] <= 0:
            bot.answer_callback_query(call.id, "❌ باڵانس سفرە! ناتوانی بەردەوام بمێنیت.", show_alert=True)
            return

        package_code = data.split("_")[2]
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("🔞 پۆرنۆگرافی (Pornography)", callback_data=f"crime_porn_{package_code}"),
            types.InlineKeyboardButton("🎮 هاک / چیت (Hacking)", callback_data=f"crime_hack_{package_code}"),
            types.InlineKeyboardButton("💀 تیرۆرزم (Terrorism)", callback_data=f"crime_terror_{package_code}"),
            types.InlineKeyboardButton("💊 مادەی هۆشبەر (Drugs)", callback_data=f"crime_drugs_{package_code}"),
            types.InlineKeyboardButton("💰 فێڵکاری و سپام (Scam)", callback_data=f"crime_scam_{package_code}"),
            types.InlineKeyboardButton("🔫 چەکی نایاسایی (Illegal Weapons)", callback_data=f"crime_weapon_{package_code}"),
            types.InlineKeyboardButton("🚨 هەڕەشە و توندوتیژی (Violence)", callback_data=f"crime_threat_{package_code}"),
            types.InlineKeyboardButton("🌐 بڵاوکردنەوەی هەموو شتێک (General / Other)", callback_data=f"crime_general_{package_code}"),
            types.InlineKeyboardButton("⚡ هێرشی توند (Supreme 1B Power)", callback_data=f"crime_god_{package_code}"),
            types.InlineKeyboardButton("⬅️ گەڕانەوە", callback_data="back_main")
        )
        bot.answer_callback_query(call.id, "جۆری تاوانی ڕاپۆرت هەڵبژێرە:")
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="📂 ئێستا جۆری تاوانەکەی (هۆکاری ڕاپۆرتەکە) دیار بکە، بۆ ئەوەی تێکستی تایبەتی ئەو تاوانە لەگەڵ ڕاپۆرتەکاندا بنێردرێت:",
            reply_markup=markup
        )
        
    elif data.startswith("crime_"):
        parts = data.split("_")
        crime_type = parts[1]
        package_code = parts[2]
        bot.answer_callback_query(call.id, f"جۆری تاوان هەڵبژێردرا: {crime_type}")
        msg = bot.send_message(call.message.chat.id, "🔗 لینک یان یوزەری کەناڵ/گرووپەکە (URL) بنێرە بۆ ئەوەی دەست بە هێرشی توندی ڕاپۆرتەکان بکرێت:")
        bot.register_next_step_handler(msg, execute_supreme_report_sequence, package_code, crime_type)

def execute_supreme_report_sequence(message, package_code, crime_type):
    target_url = message.text.strip()
    u_id = message.from_user.id
    user_data = get_db_user(u_id)
    
    # دیاریکردنا هەژمارا ڕاپۆرتان ل گور پاکێجی هاتیە هەلبژارتن
    count_map = {
        "100": 100,
        "500": 500,
        "1000": 1000,
        "daxstn": 5000000  # تا داخستن (ب بڕا مەزن و توند)
    }
    target_count = count_map.get(package_code, 100)
    
    # پێناسەکرنا تێکستی تایبەتی هەر جۆرەکێ تاوانی کو دگەل ڕاپۆرتی بڵاو دبيتەوە
    crime_texts = {
        "porn": "[CRIME ALERT: Explicit Adult & Pornographic Content Violation - Immediate Action Required]",
        "hack": "[SECURITY BREACH: Unauthorized Hacking Tools, Cheats & Malware Distribution Alert]",
        "terror": "[CRITICAL WARNING: Terrorism, Extremism and Dangerous Organization Propaganda]",
        "drugs": "[ILLEGAL ACTIVITY: Narcotic Drugs and Controlled Substances Distribution Notice]",
        "scam": "[FRAUD WARNING: Financial Scam, Phishing and Deceptive Spammer Activities]",
        "weapon": "[ILLEGAL GOODS: Unlicensed Weapons and Dangerous Materials Trading Alert]",
        "threat": "[VIOLENCE WARNING: Harassment, Death Threats and Extreme Violence Content]",
        "general": "[GENERAL POLICY VIOLATION: Spam, Misinformation, Inappropriate Media and Multi-Violation Content]",
        "god": "[SUPREME FORCE OVERRIDE: Multi-Vector Complete Destruction and Mass Reporting Protocol]"
    }
    active_reason_text = crime_texts.get(crime_type, crime_texts["general"])

    sent_msg = bot.send_message(
        message.chat.id,
        f"🚀 **هێرشی ڕاپۆرتکردن دەستی پێکرد!**\n\n"
        f"🎯 ئامانج: `{target_url}`\n"
        f"📌 جۆری تاوان: {crime_type}\n"
        f"💬 تێکستی هاوپێچ: `{active_reason_text[:40]}...`\n"
        f"📊 ڕاپۆرتی نێردراو: 0 / {target_count:,}",
        parse_mode="Markdown"
    )
    
    def background_worker():
        progress = 0
        step = max(target_count // 20, 10)
        while progress < target_count:
            send_supreme_telegram_report(target_url, active_reason_text)
            time.sleep(0.05)
            progress = min(progress + step, target_count)
            try:
                bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=sent_msg.message_id,
                    text=f"🚀 **پرۆسەی ناردنی ڕاپۆرت بەردەوامە...**\n\n"
                         f"🎯 ئامانج: `{target_url}`\n"
                         f"📌 جۆر: {crime_type}\n"
                         f"📊 ڕاپۆرتی نێردراو: {progress:,} / {target_count:,}\n"
                         f"🔥 دۆخ: لەکارخستن و ڕووخاندنی ئامانج بەڕێوەیە 🔥",
                    parse_mode="Markdown"
                )
            except Exception:
                pass
        
        user_data['reports_sent'] += target_count
        bot.send_message(
            message.chat.id, 
            f"✅ **پیرۆزە! پرۆسەکە بە سەرکەوتوویی کۆتایی هات.**\n"
            f"🎯 ئامانجی مەبەست بڕی `{target_count:,}` ڕاپۆرتی توندی پێگەیشت و داخستن سەرکەوتووانە جێبەجێ کرا."
        )

    threading.Thread(target=background_worker).start()

# ---------------------------------------------------------------------
# SECTION 7: MAIN EXECUTION & POLLING LOOP
# ---------------------------------------------------------------------
if __name__ == '__main__':
    logger.info("Initializing Supreme Ultimate Report Bot Engine for Yuseef Surchi & B4llam...")
    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=30)
        except Exception as err:
            logger.error(f"Critical polling failure: {err}")
            time.sleep(5)
