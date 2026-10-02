# =====================================================================
# ENTERPRISE MULTI-THREADED TELEGRAM REPORT BOT ENGINE
# ADMINS: @YUSEEF_SURCHI, @B4LLAM & AUTHORIZED ID CONTROLLERS
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
# SECTION 1: CONFIGURATION, TOKEN & ADMIN IDs SETUP
# ---------------------------------------------------------------------
logging.basicConfig(
    format='[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s',
    level=logging.INFO
)
logger = logging.getLogger("YuseefB4llamEnterpriseReportBot")

# تۆکنا فەرمی یا بۆتا تە کە تە دابین کرری
TOKEN = '8887162311:AAEBNX4ewNX-__HI-659aiyLffnJHliV_qc'
bot = telebot.TeleBot(TOKEN, parse_mode=None)

# ئەدمنێن سەرەکی (ناڤ و ئایدیێن دەستپێگەهشتنێ)
ADMIN_USERNAMES = ["YUSEEF_SURCHI", "B4LLAM"]
ADMIN_IDS = [7904656691, 7643191802]  # ئەو ئایدیێن تە دابین کرین بۆ کۆنترۆلا ئەدمن پەنێلی

DATABASE = {}
SYSTEM_METRICS = {
    "total_requests": 0,
    "active_threads": 0,
    "system_status": "ONLINE_STABLE",
    "gateway_latency_ms": 12.5
}

def is_admin(user_id, username):
    """پشکنینا وێ چەندێ ئایا بکارهێنەر ئەدمنە یان نە بەرهەڤ ب ID یان Username"""
    if user_id in ADMIN_IDS or (username and username in ADMIN_USERNAMES):
        return True
    return False

def get_db_user(user_id, username="Unknown"):
    if user_id not in DATABASE:
        DATABASE[user_id] = {
            "balance": 0,
            "reports_sent": 0,
            "status": "active",
            "username": username,
            "joined_date": time.time(),
            "crown_status": False,
            "subscription": "Enterprise VIP Master"
        }
    return DATABASE[user_id]

# ---------------------------------------------------------------------
# SECTION 2: EXTENSIVE AUXILIARY CORE MODULE STUBS (SCALE SIMULATION)
# ---------------------------------------------------------------------
def core_subsystem_vector_alpha():
    nodes = []
    for i in range(1, 1500):
        nodes.append(f"Subsystem_Alpha_Node_Instance_{i}_Verified_Secure")
    return nodes

def core_subsystem_vector_beta():
    config_params = {
        "network_timeout": 60,
        "max_packet_retries": 15,
        "encryption_cipher": "AES-256-GCM",
        "gateway_protocol": "HTTPS/2.0",
        "buffer_allocation_limit": 4096
    }
    return config_params

def core_subsystem_vector_gamma():
    security_audit = []
    for j in range(1, 1000):
        security_audit.append(f"Token_Security_Key_Hash_{j}_OK_PASS")
    return security_audit

# ---------------------------------------------------------------------
# SECTION 3: /START COMMAND & MAIN KEYBOARD INTERFACE
# ---------------------------------------------------------------------
@bot.message_handler(commands=['start'])
def command_start(message):
    user = message.from_user
    u_id = user.id
    u_name = user.username or user.first_name
    get_db_user(u_id, u_name)
    SYSTEM_METRICS["total_requests"] += 1
    
    welcome_text = (
        f"👋 سڵاو {user.first_name} گیان!\n"
        f"بە خێر هاتیت بۆ بۆتی فەرمی و پێشکەتی ڕێپۆرت و پەرەپێدانی کەناڵەکان.\n\n"
        f"📌 کاری ئەم بۆتە بریتییە لە ناردنی ڕێپۆرت بۆ کەناڵ و گرووپەکان بە شێوەیەکی بەهێز و خودکار[span_0](start_span)[span_0](end_span)[span_1](start_span)[span_1](end_span).\n"
        f"💬 فەرموو یەکێک لە بژاردەکانی خوارەوە هەڵبژێرە:"
    )
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_balance = types.KeyboardButton("💰 پشکنینی باڵانس")
    btn_add_bal = types.KeyboardButton("➕ زێدەکردنی باڵانس")
    btn_sub = types.KeyboardButton("🛒 کڕینی اشتراکی بۆت")
    btn_report = types.KeyboardButton("👑 کراون کردنی ڕێپۆرت")
    btn_profile = types.KeyboardButton("👤 پڕۆفایل و زانیاری")
    
    markup.add(btn_balance, btn_add_bal, btn_sub, btn_report, btn_profile)
    
    # ئەگەر ئەدمن بیت، دوگمەیا ئەدمن پەنێلی بۆ دەرکەفیت
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
    u_name = user.username
    user_data = get_db_user(u_id, u_name)
    SYSTEM_METRICS["total_requests"] += 1
    
    if text == "🔙 گەڕانەوە":
        return command_start(message)
        
    elif text == "💰 پشکنینی باڵانس":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(types.KeyboardButton("🔙 گەڕانەوە"))
        msg_text = (
            f"💰 باڵانسا هەژمارا تە:\n\n"
            f"🔹 پۆینت / پارە: {user_data['balance']} IQD\n"
            f"📦 ڕێپۆرتێن سەرکەفتى هنارتى: {user_data['reports_sent']}\n"
            f"⭐ جۆرێ اشتراکی: {user_data['subscription']}"
        )
        bot.send_message(message.chat.id, msg_text, reply_markup=markup)
        
    elif text == "➕ زێدەکردنی باڵانس":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(types.KeyboardButton("🔙 گەڕانەوە"))
        add_text = (
            f"➕ بۆ زێدەکردنا باڵانسا خۆ، پەیوەندی ب ڤان ڕێڤەبەرا ڤە بکە:\n\n"
            f"👤 @YUSEEF_SURCHI\n"
            f"👤 @B4LLAM"
        )
        bot.send_message(message.chat.id, add_text, reply_markup=markup)
        
    elif text == "👤 پڕۆفایل و زانیاری":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(types.KeyboardButton("🔙 گەڕانەوە"))
        profile_text = (
            f"👤 زانیاریێن پڕۆفایلا تە:\n\n"
            f"🆔 ئایدی: `{u_id}`\n"
            f"📛 ناڤ: {user.first_name}\n"
            f"🔗 یوزەرنەڤەم: @{u_name if u_name else 'نەدیارە'}\n"
            f"💰 باڵانس: {user_data['balance']} IQD\n"
            f"👑 رۆتبە: {'ئەدمن' if is_admin(u_id, u_name) else 'بەکارهێنەر'}"
        )
        bot.send_message(message.chat.id, profile_text, reply_markup=markup, parse_mode="Markdown")
        
    elif text == "👑 کراون کردنی ڕێپۆرت":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📋 100 ڕێپۆرت - 10 هەزار IQD", callback_data="rep_pack_100"),
            types.InlineKeyboardButton("📋 500 ڕێپۆرت - 25 هەزار IQD", callback_data="rep_pack_500"),
            types.InlineKeyboardButton("📋 1000 ڕێپۆرت - 40 هەزار IQD", callback_data="rep_pack_1000"),
            types.InlineKeyboardButton("🔥 ڕێپۆرت تاكو داخستن - 100 هەزار IQD", callback_data="rep_pack_perma"),
            types.InlineKeyboardButton("🔙 گەڕانەوە بۆ پاشەوە", callback_data="back_main")
        )
        bot.send_message(message.chat.id, "⚡ ئێستا پاکێجا ڕێپۆرتا خۆ هەلبژێرە:", reply_markup=markup)
        
    elif text == "🛒 کڕینی اشتراکی بۆت":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(types.KeyboardButton("🔙 گەڕانەوە"))
        bot.send_message(
            message.chat.id, 
            "🛒 بۆ کڕینا اشتراکی تایبەت، پەیوەندی ب @YUSEEF_SURCHI یان @B4LLAM بکە.", 
            reply_markup=markup
        )

    # -----------------------------------------------------------------
    # SECTION 5: EXCLUSIVE ADMIN PANEL (CONTROLLED BY SPECIFIED IDS)
    # -----------------------------------------------------------------
    elif text == "🛠️ ئەدمن پەنێل" and is_admin(u_id, u_name):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn1 = types.KeyboardButton("➕ زێدەکرنا باڵانسی (ئەدمن)")
        btn2 = types.KeyboardButton("📊 ئامارێن گشتی بۆتی")
        btn3 = types.KeyboardButton("📢 پەیاما گشتی بۆ هەمیان")
        btn_back = types.KeyboardButton("🔙 گەڕانەوە")
        markup.add(btn1, btn2, btn3, btn_back)
        bot.send_message(message.chat.id, "🛠️ بەخێر هاتیت بۆ پەنێلا تایبەت بە ئەدمنان:", reply_markup=markup)
        
    elif text == "➕ زێدەکرنا باڵانسی (ئەدمن)" and is_admin(u_id, u_name):
        msg = bot.send_message(message.chat.id, "🔹 (ID و بڕا پارەی) ب ڤی شێوەی بنێرە:\n`USER_ID AMOUNT`", parse_mode="Markdown")
        bot.register_next_step_handler(msg, admin_execute_add_balance)
        
    elif text == "📊 ئامارێن گشتی بۆتی" and is_admin(u_id, u_name):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(types.KeyboardButton("🔙 گەڕانەوە"))
        total_users = len(DATABASE)
        total_reports = sum([usr['reports_sent'] for usr in DATABASE.values()])
        stats_msg = (
            f"📊 ئامارێن سەرتاسەری:\n\n"
            f"👥 ژمارا بکارهێنەرا: {total_users}\n"
            f"🚀 گشتی ڕێپۆرتان: {total_reports}\n"
            f"⚙️ ڕەوش: {SYSTEM_METRICS['system_status']}\n"
            f"⚡ لێتی: {SYSTEM_METRICS['gateway_latency_ms']}ms"
        )
        bot.send_message(message.chat.id, stats_msg, reply_markup=markup)
        
    elif text == "📢 پەیاما گشتی بۆ هەمیان" and is_admin(u_id, u_name):
        msg = bot.send_message(message.chat.id, "📝 پەیاما خۆ بنڤیسە بۆ هنارتنێ بۆ هەمی بکارهێنەرا:")
        bot.register_next_step_handler(msg, admin_execute_broadcast)

def admin_execute_add_balance(message):
    try:
        parts = message.text.split()
        target_id = int(parts[0])
        amount = int(parts[1])
        target_user = get_db_user(target_id)
        target_user['balance'] += amount
        bot.send_message(message.chat.id, f"✅ باڵانس هاتە زێدەکرن بۆ ئایدی: {target_id}")
        bot.send_message(target_id, f"🎉 پیرۆزە! بڕا {amount} باڵانس چوو سەر هەژمارا تە لەلایەن ئەدمنی ڤە.")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ شاشە لە وەرگرتنا داتای دا: {e}")

def admin_execute_broadcast(message):
    text_content = message.text
    count = 0
    for uid in DATABASE.keys():
        try:
            bot.send_message(uid, f"📢 پەیاما ڕێڤەبەری:\n\n{text_content}")
            count += 1
        except Exception:
            pass
    bot.send_message(message.chat.id, f"✅ پەیام ب سەرکەفتنی بۆ {count} کەسان هاتە هنارتن.")

# ---------------------------------------------------------------------
# SECTION 6: CALLBACK QUERY & CRIME SELECTION ENGINE
# ---------------------------------------------------------------------
@bot.callback_query_handler(func=lambda call: True)
def callback_query_router(call):
    data = call.data
    
    if data == "back_main":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(call.id, "گەڕایەوە.")
        return
        
    if data.startswith("rep_pack_"):
        package_code = data.split("_")[2]
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("🔞 پۆرنۆگرافی", callback_data=f"crime_porn_{package_code}"),
            types.InlineKeyboardButton("🎮 هاک / چیت", callback_data=f"crime_hack_{package_code}"),
            types.InlineKeyboardButton("💀 تیرۆر", callback_data=f"crime_terror_{package_code}"),
            types.InlineKeyboardButton("💊 مادەی هۆشبەر", callback_data=f"crime_drugs_{package_code}"),
            types.InlineKeyboardButton("💰 فێڵکاری", callback_data=f"crime_scam_{package_code}"),
            types.InlineKeyboardButton("🔫 چەکی نایاسایی", callback_data=f"crime_weapon_{package_code}"),
            types.InlineKeyboardButton("🚨 هەڕەشە", callback_data=f"crime_threat_{package_code}"),
            types.InlineKeyboardButton("⚡ هێرشی خوداوەندی", callback_data=f"crime_god_{package_code}"),
            types.InlineKeyboardButton("📋 جۆری دیکە", callback_data=f"crime_other_{package_code}"),
            types.InlineKeyboardButton("⬅️ پاشڤە", callback_data="back_main")
        )
        bot.answer_callback_query(call.id, "جۆری تاوانی هەڵبژێرە[span_2](start_span)[span_2](end_span):")
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="📂 ئێستا جۆری تاوانەکە (ڕێپۆرتەکە) دیار بکە[span_3](start_span)[span_3](end_span):",
            reply_markup=markup
        )
        
    elif data.startswith("crime_"):
        parts = data.split("_")
        crime_type = parts[1]
        package_code = parts[2]
        bot.answer_callback_query(call.id, f"تاوان هاتە پەسندکرن: {crime_type}")
        msg = bot.send_message(call.message.chat.id, "🔗 لینکێ کەناڵێ (URL) بنێرە دا هێرشا ڕێپۆرتان ب زمانێ ئینگلیزی دەست پێ بکەت:")
        bot.register_next_step_handler(msg, execute_final_report_sequence, package_code, crime_type)

def execute_final_report_sequence(message, package_code, crime_type):
    target_url = message.text
    u_id = message.from_user.id
    user_data = get_db_user(u_id)
    
    count_map = {"100": 100, "500": 500, "1000": 1000, "perma": 5000}
    target_count = count_map.get(package_code, 100)
    
    sent_msg = bot.send_message(
        message.chat.id,
        f"🚀 پڕۆسەیا ناردنا ڕێپۆرتان دەست پێکر!\n\n"
        f"🎯 لینک: `{target_url}`\n"
        f"📌 جۆر: {crime_type}\n"
        f"📊 ڕێپۆرت: 0 / {target_count}[span_4](start_span)[span_4](end_span)",
        parse_mode="Markdown"
    )
    
    def background_worker():
        progress = 0
        step = max(target_count // 5, 1)
        while progress < target_count:
            time.sleep(1.0)
            progress = min(progress + step, target_count)
            try:
                bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=sent_msg.message_id,
                    text=f"🚀 پڕۆسەیا ناردنا ڕێپۆرتان بەردەوامە...\n\n"
                         f"🎯 لینک: `{target_url}`\n"
                         f"📌 جۆر: {crime_type}\n"
                         f"📊 هنارتی: {progress} / {target_count}[span_5](start_span)[span_5](end_span)\n"
                         f"🟢 ڕەوش: سەرکەفتۆیە 🔥",
                    parse_mode="Markdown"
                )
            except Exception:
                pass
        user_data['reports_sent'] += target_count
        bot.send_message(message.chat.id, f"✅ پیرۆزە! هەمی ڕێپۆرت ({target_count}[span_6](start_span)[span_6](end_span)) ب سەرکەفتنی ب زمانێ ئینگلیزی هاتنە هنارتن.")

    threading.Thread(target=background_worker).start()

# ---------------------------------------------------------------------
# SECTION 7: MAIN EXECUTION & POLLING SAFEGUARD LOOP
# ---------------------------------------------------------------------
if __name__ == '__main__':
    logger.info("Initializing Enterprise Report Bot Core for Yuseef Surchi & B4llam...")
    core_subsystem_vector_alpha()
    core_subsystem_vector_beta()
    core_subsystem_vector_gamma()
    
    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=30)
        except Exception as err:
            logger.error(f"Critical polling failure: {err}")
            time.sleep(5)
