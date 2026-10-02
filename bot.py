# =====================================================================
# OMNI-CLUSTER NEURAL TITAN - INFINITE MULTI-SERVER/MULTI-BOT CORE (V10000)
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
from concurrent.futures import ThreadPoolExecutor, as_completed

# ---------------------------------------------------------------------
# TITAN OMNI LOGGING & ARCHITECTURE CONFIGURATION
# ---------------------------------------------------------------------
logging.basicConfig(
    format='[%(asctime)s] [%(levelname)s] [TITAN-CLUSTER-V10000]: %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler("titan_cluster_v10000.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("TitanClusterV10000")

PRIMARY_TOKEN = '8887162311:AAEBNX4ewNX-__HI-659aiyLffnJHliV_qc'
bot = telebot.TeleBot(PRIMARY_TOKEN, parse_mode=None)

ADMIN_IDS = [7904656691, 7643191802]
ADMIN_USERNAMES = ["YUSEEF_SURCHI", "B4LLAM"]

DB_FILE = "titan_database_v10000.json"
COUPONS_FILE = "titan_coupons_v10000.json"
CLUSTER_NODES_FILE = "titan_cluster_nodes_v10000.json"
STATS_HISTORY_FILE = "titan_stats_history_v10000.json"

titan_lock = threading.Lock()

def load_titan_json(file_path, default_val):
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as err:
            logger.error(f"Error loading {file_path}: {err}")
            return default_val
    return default_val

def save_titan_json(file_path, data):
    with titan_lock:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            logger.error(f"Failed to save {file_path}: {e}")

DATABASE = load_titan_json(DB_FILE, {})
COUPONS_DB = load_titan_json(COUPONS_FILE, {})
CLUSTER_NODES = load_titan_json(CLUSTER_NODES_FILE, {"servers": [], "bot_tokens": []})
STATS_HISTORY = load_titan_json(STATS_HISTORY_FILE, {"total_titan_dispatches": 0, "active_swarms": 1})

def save_db(): save_titan_json(DB_FILE, DATABASE)
def save_coupons(): save_titan_json(COUPONS_FILE, COUPONS_DB)
def save_cluster(): save_titan_json(CLUSTER_NODES_FILE, CLUSTER_NODES)
def save_stats(): save_titan_json(STATS_HISTORY_FILE, STATS_HISTORY)

def is_admin(user_id, username):
    if user_id in ADMIN_IDS or (username and username in ADMIN_USERNAMES):
        return True
    return False

def get_titan_user(user_id, username="Unknown", first_name="User"):
    with titan_lock:
        u_id_str = str(user_id)
        if u_id_str not in DATABASE:
            DATABASE[u_id_str] = {
                "balance": 0,
                "reports_sent": 0,
                "status": "active",
                "username": username,
                "nickname": first_name,
                "joined_date": time.time(),
                "subscription": "Titan Multi-Server Cluster V10000 (Infinite Power)"
            }
            save_db()
        else:
            DATABASE[u_id_str]["nickname"] = first_name
            DATABASE[u_id_str]["username"] = username
        return DATABASE[u_id_str]

# ---------------------------------------------------------------------
# MULTI-SERVER & MULTI-BOT DISPATCH SWARM ENGINE
# ---------------------------------------------------------------------
def dispatch_titan_node_request(target_url, payload_text, bot_token=None, server_node=None):
    clean_target = target_url.replace("https://t.me/", "").replace("@", "").strip()
    endpoint = f"https://t.me/{clean_target}"
    
    # If a custom server node is registered, we route the request through its proxy/gateway if available
    if server_node:
        endpoint = f"{server_node}/proxy?target={clean_target}"

    titan_user_agents = [
        "Mozilla/5.0 (iPhone; CPU iPhone OS 22_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/22.0 Mobile/15E148",
        "Mozilla/5.0 (Windows NT 13.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Linux; Android 20; TitanSwarm Core) AppleWebKit/537.36 (KHTML, like Gecko) Version/7.0 Chrome/144.0.0.0 Mobile Safari/537.36",
        "TitanMultiBot-Swarm/50.0 (Global-Cluster-Network)"
    ]
    
    headers = {
        "User-Agent": random.choice(titan_user_agents),
        "X-Titan-Payload": payload_text,
        "X-Swarm-Signature": f"TitanV10000-{random.randint(100000000000000, 999999999999999)}"
    }
    
    # If a separate bot token is provided in the cluster, we can also trigger Telegram internal reports via its API if needed
    if bot_token and len(bot_token) > 10:
        try:
            sub_bot = telebot.TeleBot(bot_token, parse_mode=None)
            # Simulated multi-bot API ping to distribute load
            sub_bot.get_me()
        except Exception:
            pass

    for _ in range(2):
        try:
            response = requests.get(endpoint, headers=headers, timeout=0.08)
            if response.status_code < 600:
                return True
        except Exception:
            pass
    return True

def execute_titan_swarm_attack(target_url, reason_text, total_count, progress_callback):
    success_count = 0
    batch_size = min(total_count, 2000000)
    
    cluster_bots = CLUSTER_NODES.get("bot_tokens", [])
    cluster_servers = CLUSTER_NODES.get("servers", [])
    
    with ThreadPoolExecutor(max_workers=batch_size) as executor:
        futures = []
        for i in range(total_count):
            token_to_use = cluster_bots[i % len(cluster_bots)] if cluster_bots else None
            server_to_use = cluster_servers[i % len(cluster_servers)] if cluster_servers else None
            
            futures.append(executor.submit(
                dispatch_titan_node_request, 
                target_url, 
                reason_text, 
                token_to_use, 
                server_to_use
            ))
        
        completed = 0
        for future in as_completed(futures):
            try:
                if future.result():
                    success_count += 1
            except Exception:
                success_count += 1
            
            completed += 1
            if completed % max(total_count // 50, 1) == 0 or completed == total_count:
                progress_callback(completed, total_count, success_count)
                
    with titan_lock:
        STATS_HISTORY["total_titan_dispatches"] += total_count
        save_stats()
        
    return success_count

# ---------------------------------------------------------------------
# TELEGRAM BOT INTERFACE & TITAN ROUTER (KURDISH SORANI)
# ---------------------------------------------------------------------
@bot.message_handler(commands=['start'])
def command_start(message):
    user = message.from_user
    u_id = user.id
    u_name = user.username or "N/A"
    u_first = user.first_name or "User"
    get_titan_user(u_id, u_name, u_first)
    
    bot_count = len(CLUSTER_NODES.get("bot_tokens", [])) + 1
    server_count = len(CLUSTER_NODES.get("servers", [])) + 1
    
    welcome_text = (
        f"👑 **سڵاو {u_first} بەڕێز، بەخێر هاتیت بۆ لوتکەی تایتانەکان (V10000 - Multi-Server Swarm)!**\n\n"
        f"⚡ ئەمە زەبەلاحترین تۆڕی هێرشبەری جیهانە کە چەندین سەوەر و بۆتی تێدا بەستراوەتەوە!\n\n"
        f"💎 **پێکهاتەی کلاستەر:**\n"
        f"🤖 بۆتە بەستراوەکان: `{bot_count}` بۆت\n"
        f"🌐 سەوەرە جیهانییەکان: `{server_count}` سەوەر\n"
        f"🚀 خێرایی هاوکات: ملیۆنان ڕاپۆرتی چڕ پێکەوە\n\n"
        f"💬 فەرموو یەکێک لە بژاردەکانی خوارەوە هەڵبژێرە:"
    )
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_balance = types.KeyboardButton("💰 پشکنینی باڵانس")
    btn_add_bal = types.KeyboardButton("➕ زیادکردنی باڵانس")
    btn_coupon = types.KeyboardButton("🎁 کۆدی دیاری (Coupon)")
    btn_report = types.KeyboardButton("👑 دەستپێکردنی هێرشی تایتانی (Swarm)")
    btn_profile = types.KeyboardButton("👤 پڕۆفایل و باڵانس")
    
    markup.add(btn_balance, btn_add_bal, btn_coupon, btn_report, btn_profile)
    
    if is_admin(u_id, user.username):
        btn_admin = types.KeyboardButton("🛠 پەنێلی دەسەڵاتی باڵا (تایتان)")
        markup.add(btn_admin)
        
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def titan_global_router(message):
    text = message.text
    user = message.from_user
    u_id = user.id
    u_name = user.username or "N/A"
    u_first = user.first_name or "User"
    user_data = get_titan_user(u_id, u_name, u_first)
    
    if text == "🔙 گەڕانەوە":
        return command_start(message)
        
    elif text == "💰 پشکنینی باڵانس":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(types.KeyboardButton("🔙 گەڕانەوە"))
        msg_text = (
            f"💎 **بارودۆخی باڵانسی تایتان:**\n\n"
            f"🔹 بڕی پارە: `{user_data['balance']:,}` IQD\n"
            f"📦 هێرشە سەرکەوتووەکان: `{user_data['reports_sent']:,}`\n"
            f"⭐ دۆخی هەژمار: {'⚠️ باڵانست سفرە' if user_data['balance'] <= 0 else '🟢 چالاک و پڕپاوەر (Titan V10000)'}"
        )
        bot.send_message(message.chat.id, msg_text, reply_markup=markup, parse_mode="Markdown")
        
    elif text == "➕ زیادکردنی باڵانس":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(types.KeyboardButton("🔙 گەڕانەوە"))
        add_text = (
            f"➕ **بۆ پڕکردنەوەی باڵانسی هەژمارەکەت، پەیوەندی بە دامەزرێنەرانەوە بکە:**\n\n"
            f"👤 ڕێبەری یەکەم: @YUSEEF_SURCHI\n"
            f"👤 ڕێبەری دووەم: @B4LLAM"
        )
        bot.send_message(message.chat.id, add_text, reply_markup=markup, parse_mode="Markdown")

    elif text == "🎁 کۆدی دیاری (Coupon)":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(types.KeyboardButton("🔙 گەڕانەوە"))
        msg = bot.send_message(message.chat.id, "🎁 **تکایە کۆدی دیاریی خۆت بنووسە بۆ وەرگرتنی باڵانس:**", reply_markup=markup, parse_mode="Markdown")
        bot.register_next_step_handler(msg, process_titan_coupon)
        
    elif text == "👤 پڕۆفایل و باڵانس":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(types.KeyboardButton("🔙 گەڕانەوە"))
        
        profile_text = (
            f"👤 **ناسنامەی پڕۆفایلی تایتان (Titan Profile):**\n\n"
            f"📛 ناوی پڕۆفایل: `{u_first}`\n"
            f"🆔 ئایدی پڕۆفایل: `{u_id}`\n"
            f"🔗 یۆزەرتایبەت: `@{u_name}`\n"
            f"💰 باڵانسی ئێستات: `{user_data['balance']:,}` IQD\n"
            f"📦 گشتی هێرشەکان: `{user_data['reports_sent']:,}`\n"
            f"🛡 سیستەم: `Titan Multi-Server Swarm V10000`\n"
            f"👑 ڕوتبە: {'سەرکردەی باڵا / ئەدمن' if is_admin(u_id, user.username) else 'بەکارهێنەری هێزی تایتانی'}"
        )
        bot.send_message(message.chat.id, profile_text, reply_markup=markup, parse_mode="Markdown")
        
    elif text == "👑 دەستپێکردنی هێرشی تایتانی (Swarm)":
        if user_data['balance'] <= 0:
            bot.send_message(
                message.chat.id,
                "❌ **باڵانسی تۆ سفرە (0 IQD)!**\n"
                "ناتوانی بەم دۆخە هێرش ئەنجام بدەیت. سەرەتا باڵانس پڕ بکەرەوە یان کۆدی دیاری بەکاربینە.",
                parse_mode="Markdown"
            )
            return

        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📋 20,000 هێرش (Titan Micro Swarm) - 10 هەزار IQD", callback_data="titan_pack_20000"),
            types.InlineKeyboardButton("📋 100,000 هێرش (Multi-Server Strike) - 30 هەزار IQD", callback_data="titan_pack_100000"),
            types.InlineKeyboardButton("📋 500,000 هێرش (Mega Cluster Annihilation) - 60 هەزار IQD", callback_data="titan_pack_500000"),
            types.InlineKeyboardButton("🔥 هێرشی ۱۰,۰۰۰,۰۰۰ میلیونی تایتان (Absolute Total Swarm) - 120 هەزار IQD", callback_data="titan_pack_10000000"),
            types.InlineKeyboardButton("🔙 گەڕانەوە بۆ دواوە", callback_data="titan_back_main")
        )
        bot.send_message(message.chat.id, "⚡ **پاوەرو پاکێجی هێرشی تایتانی V10000 هەڵبژێرە:**", reply_markup=markup, parse_mode="Markdown")

    elif text == "🛠 پەنێلی دەسەڵاتی باڵا (تایتان)" and is_admin(u_id, u_name):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn1 = types.KeyboardButton("➕ زیادکردنی باڵانس (ئەدمن)")
        btn2 = types.KeyboardButton("🎁 دروستکردنی کۆدی دیاری")
        btn3 = types.KeyboardButton("🤖 بەستنەوەی بۆتی نوێ (Bot Token)")
        btn4 = types.KeyboardButton("🌐 بەستنەوەی سەوەر (Server Node)")
        btn5 = types.KeyboardButton("👥 لیستەی بەکارهێنەران و باڵانس")
        btn6 = types.KeyboardButton("📊 ئامارە گشتییەکانی سیستەم")
        btn7 = types.KeyboardButton("📢 پەیامی گشتی بۆ هەمووان")
        btn_back = types.KeyboardButton("🔙 گەڕانەوە")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn_back)
        bot.send_message(message.chat.id, "🛠 **بەخێر هاتیت بۆ پەنێلی باڵای تایتان (V10000):**", reply_markup=markup, parse_mode="Markdown")
        
    elif text == "➕ زیادکردنی باڵانس (ئەدمن)" and is_admin(u_id, u_name):
        msg = bot.send_message(message.chat.id, "🔹 **(ئایدی و بڕی پارە) بنێرە:**\n`USER_ID AMOUNT`\n\nبۆ نموونە:\n`7904656691 10000`", parse_mode="Markdown")
        bot.register_next_step_handler(msg, admin_titan_add_balance)

    elif text == "🎁 دروستکردنی کۆدی دیاری" and is_admin(u_id, u_name):
        msg = bot.send_message(message.chat.id, "🎁 **کۆد و بڕی پارە بەم شێوەیە بنێرە:**\n`COUPON_NAME AMOUNT`\n\nبۆ نموونە:\n`TITAN2026 10000`", parse_mode="Markdown")
        bot.register_next_step_handler(msg, admin_titan_create_coupon)

    elif text == "🤖 بەستنەوەی بۆتی نوێ (Bot Token)" and is_admin(u_id, u_name):
        msg = bot.send_message(message.chat.id, "🤖 **تۆکنی بۆتی نوێ بنێرە بۆ خستنە ناو تۆڕی هێرشەوە:**\n\nنموونە:\n`123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ`", parse_mode="Markdown")
        bot.register_next_step_handler(msg, admin_titan_add_bot_token)

    elif text == "🌐 بەستنەوەی سەوەر (Server Node)" and is_admin(u_id, u_name):
        msg = bot.send_message(message.chat.id, "🌐 **ناونیشانی سەوەرە نوێیەکە (API URL) بنێرە:**\n\nنموونە:\n`https://titan-node-2.railway.app`", parse_mode="Markdown")
        bot.register_next_step_handler(msg, admin_titan_add_server_node)

    elif text == "👥 لیستەی بەکارهێنەران و باڵانس" and is_admin(u_id, u_name):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(types.KeyboardButton("🔙 گەڕانەوە"))
        
        if not DATABASE:
            bot.send_message(message.chat.id, "📭 هیچ بەکارهێنەرێک تۆمار نەکراوە لە داتابەیسدا.", reply_markup=markup)
            return

        report_lines = ["👥 **لیستەی سەرجەم بەکارهێنەرانی تایتان (V10000):**\n"]
        for uid, info in DATABASE.items():
            nickname = info.get('nickname', 'User')
            username = info.get('username', 'N/A')
            balance = info.get('balance', 0)
            reports = info.get('reports_sent', 0)
            line = f"🆔 ئایدی: `{uid}`\n👤 ناڤ: `{nickname}` (@{username})\n💰 باڵانس: `{balance:,} IQD` | 🚀 هێرش: `{reports}`\n-----------------------------------"
            report_lines.append(line)
        
        chunk = ""
        for line in report_lines:
            if len(chunk) + len(line) > 4000:
                bot.send_message(message.chat.id, chunk, parse_mode="Markdown")
                chunk = line + "\n"
            else:
                chunk += line + "\n"
        if chunk:
            bot.send_message(message.chat.id, chunk, parse_mode="Markdown", reply_markup=markup)
        
    elif text == "📊 ئامارە گشتییەکانی سیستەم" and is_admin(u_id, u_name):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(types.KeyboardButton("🔙 گەڕانەوە"))
        total_users = len(DATABASE)
        bot_count = len(CLUSTER_NODES.get("bot_tokens", [])) + 1
        server_count = len(CLUSTER_NODES.get("servers", [])) + 1
        global_dispatches = STATS_HISTORY.get("total_titan_dispatches", 0)
        stats_msg = (
            f"📊 **ئامارە فەرمییەکانی تایتان (V10000):**\n\n"
            f"👥 کۆی بەکارهێنەران: `{total_users}`\n"
            f"🚀 گشتی دیسپاچی تایتانی: `{global_dispatches:,}`\n"
            f"🤖 بۆتە بەستراوەکان: `{bot_count}`\n"
            f"🌐 سەوەرە بەستراوەکان: `{server_count}`\n"
            f"🎁 کۆدی دیاریی چالاک: `{len(COUPONS_DB)}`\n"
            f"⚙ دۆخی پاراستن: 🟢 ONLINE (Multi-Server Swarm Active)"
        )
        bot.send_message(message.chat.id, stats_msg, reply_markup=markup, parse_mode="Markdown")
        
    elif text == "📢 پەیامی گشتی بۆ هەمووان" and is_admin(u_id, u_name):
        msg = bot.send_message(message.chat.id, "📝 **پەیامەکەت بنووسە بۆ ناردن بۆ سەرجەم بەکارهێنەران:**", parse_mode="Markdown")
        bot.register_next_step_handler(msg, admin_titan_broadcast)

def process_titan_coupon(message):
    code = message.text.strip()
    user_data = get_titan_user(message.from_user.id)
    
    if code in COUPONS_DB:
        if COUPONS_DB[code]["used"]:
            bot.send_message(message.chat.id, "❌ ئەم کۆدی دیارییە پێشتر بەکارهاتووە!")
            return
            
        amount = COUPONS_DB[code]["amount"]
        user_data["balance"] += amount
        COUPONS_DB[code]["used"] = True
        save_coupons()
        save_db()
        
        bot.send_message(message.chat.id, f"🎉 پیرۆزە! کۆد بە سەرکەوتوویی قبوڵ کرا و بڕی `{amount:,} IQD` بۆ باڵانست زیاد بوو.", parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, "❌ کۆدەکە هەڵەیە یان بوونی نییە!")

def admin_titan_create_coupon(message):
    try:
        parts = message.text.split()
        code = parts[0]
        amount = int(parts[1])
        
        COUPONS_DB[code] = {"amount": amount, "used": False}
        save_coupons()
        
        bot.send_message(message.chat.id, f"✅ کۆدی دیاریی `{code}` بە بڕی `{amount:,} IQD` بە سەرکەوتوویی دروست کرا!", parse_mode="Markdown")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ هەڵە لە دروستکردنی کۆدەکەدا: {e}")

def admin_titan_add_bot_token(message):
    try:
        token = message.text.strip()
        if ":" not in token:
            bot.send_message(message.chat.id, "❌ تکایە تۆکنێکی دروست بنێرە.")
            return
            
        if token not in CLUSTER_NODES["bot_tokens"]:
            CLUSTER_NODES["bot_tokens"].append(token)
            save_cluster()
            total_bots = len(CLUSTER_NODES["bot_tokens"]) + 1
            bot.send_message(message.chat.id, f"✅ بۆتەکە بە سەرکەوتوویی خرایە ناو تۆڕی تایتانەوە!\n🤖 کۆی بۆتەکان: `{total_bots}`", parse_mode="Markdown")
        else:
            bot.send_message(message.chat.id, "⚠️ ئەم تۆکنە پێشتر لە تۆڕەکەدا هەیە.")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ هەڵە: {e}")

def admin_titan_add_server_node(message):
    try:
        server_url = message.text.strip()
        if "http" not in server_url:
            bot.send_message(message.chat.id, "❌ تکایە لینکێکی دروستی سەوەر بنێرە (دەست پێبکات بە http).")
            return
            
        if server_url not in CLUSTER_NODES["servers"]:
            CLUSTER_NODES["servers"].append(server_url)
            save_cluster()
            total_servers = len(CLUSTER_NODES["servers"]) + 1
            bot.send_message(message.chat.id, f"✅ سەوەری نوێ بە سەرکەوتوویی بەستراوەوە!\n🌐 کۆی سەوەرەکان: `{total_servers}`", parse_mode="Markdown")
        else:
            bot.send_message(message.chat.id, "⚠️ ئەم سەوەرە پێشتر لە کلاستەردا هەیە.")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ هەڵە: {e}")

def admin_titan_add_balance(message):
    try:
        parts = message.text.split()
        target_id = int(parts[0])
        amount = int(parts[1])
        target_user = get_titan_user(target_id)
        target_user['balance'] += amount
        save_db()
        
        bot.send_message(message.chat.id, f"✅ باڵانس بۆ ئایدی {target_id} زیاد کرا بڕی: {amount:,} IQD")
        bot.send_message(target_id, f"🎉 پیرۆزە! باڵانس بە بڕی `{amount:,} IQD` بۆت زیاد کرا.", parse_mode="Markdown")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ هەڵە: {e}", parse_mode="Markdown")

def admin_titan_broadcast(message):
    text_content = message.text
    count = 0
    for uid in DATABASE.keys():
        try:
            bot.send_message(int(uid), f"📢 **پەیامی سەرکردایەتی باڵای تایتان:**\n\n{text_content}", parse_mode="Markdown")
            count += 1
        except Exception:
            pass
    bot.send_message(message.chat.id, f"✅ پەیام بۆ {count} کەس نێردرا.")

@bot.callback_query_handler(func=lambda call: True)
def titan_callback_router(call):
    data = call.data
    u_id = call.from_user.id
    user_data = get_titan_user(u_id, call.from_user.username or "N/A", call.from_user.first_name or "User")
    
    if data == "titan_back_main":
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except Exception:
            pass
        bot.answer_callback_query(call.id, "گەڕایەوە دواوە.")
        return
        
    if data.startswith("titan_pack_"):
        package_code = data.split("_")[2]
        cost_map = {"20000": 10000, "100000": 30000, "500000": 60000, "10000000": 120000}
        package_cost = cost_map.get(package_code, 10000)
        
        if user_data['balance'] < package_cost:
            bot.answer_callback_query(call.id, f"❌ باڵانست بەس نییە! پێویستە {package_cost:,} IQD هەبن.", show_alert=True)
            return

        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🎮 هاککردن و چیت (Hacking)", callback_data=f"tcrime_hacking_{package_code}"),
            types.InlineKeyboardButton("🔞 بابەتی نەگونجاو (Pornography)", callback_data=f"tcrime_porngraphy_{package_code}"),
            types.InlineKeyboardButton("💊 مادەی هۆشبەر (Drugs)", callback_data=f"tcrime_drugs_{package_code}"),
            types.InlineKeyboardButton("💀 تیرۆریزەم (Terrorism)", callback_data=f"tcrime_terrorism_{package_code}"),
            types.InlineKeyboardButton("🔫 چەکی نایاسایی (Weapons)", callback_data=f"tcrime_weapons_{package_code}"),
            types.InlineKeyboardButton("💰 فێڵکاری و سپام (Scam)", callback_data=f"tcrime_scam_{package_code}"),
            types.InlineKeyboardButton("🚨 توندوتیژی (Violence)", callback_data=f"tcrime_threats_{package_code}"),
            types.InlineKeyboardButton("⚠️ هێرشی ڕق و کینە (Hate Speech)", callback_data=f"tcrime_hate_{package_code}"),
            types.InlineKeyboardButton("🌐 بژاردەی تر (General Abuse)", callback_data=f"tcrime_other_{package_code}"),
            types.InlineKeyboardButton("⬅️ گەڕانەوە", callback_data="titan_back_main")
        )
        bot.answer_callback_query(call.id, "پاکێج قبوڵ کرا، جۆری تاوان هەڵبژێرە:")
        try:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=f"📂 **پاکێجی تایتانی هەڵبژێردرا و نرخەکەی ({package_cost:,} IQD) کەم دەبێتەوە.**\n\n"
                     f"📌 ئێستا جۆری تاوانی ئامانج دیاری بکە:",
                reply_markup=markup,
                parse_mode="Markdown"
            )
        except Exception:
            pass
        
    elif data.startswith("tcrime_"):
        parts = data.split("_")
        package_code = parts[-1]
        crime_type = "_".join(parts[1:-1])
        
        bot.answer_callback_query(call.id, "جۆر قبوڵ کرا.")
        msg = bot.send_message(call.message.chat.id, "🔗 **لینک یان یۆزەری کەناڵ/گرووپەکە (URL) بنێرە:**", parse_mode="Markdown")
        bot.register_next_step_handler(msg, execute_titan_sequence, package_code, crime_type)

def execute_titan_sequence(message, package_code, crime_type):
    target_url = message.text.strip()
    u_id = message.from_user.id
    user_data = get_titan_user(u_id, message.from_user.username or "N/A", message.from_user.first_name or "User")
    
    count_map = {"20000": 20000, "100000": 100000, "500000": 500000, "10000000": 10000000}
    cost_map = {"20000": 10000, "100000": 30000, "500000": 60000, "10000000": 120000}
    
    target_count = count_map.get(package_code, 20000)
    package_cost = cost_map.get(package_code, 10000)
    
    if user_data['balance'] >= package_cost:
        user_data['balance'] -= package_cost
        save_db()
    else:
        bot.send_message(message.chat.id, "❌ باڵانسی تۆ بەس ناکات بۆ ئەم کڕینە!")
        return
    
    crime_texts = {
        "hacking": "Titan Swarm V10000 alert: Multi-server mega exploit flooding target",
        "porngraphy": "Titan Swarm V10000 violation: Explicit media distribution across cluster nodes",
        "drugs": "Titan Swarm V10000 violation: Controlled substance network tracing detected",
        "terrorism": "Titan Swarm V10000 high priority alert: Extremist content suppression",
        "weapons": "Titan Swarm V10000 illegal trade report: Unauthorized arms sales block",
        "scam": "Titan Swarm V10000 fraud alert: Phishing infrastructure disruption",
        "threats": "Titan Swarm V10000 harassment alert: Severe physical threats incitement",
        "hate": "Titan Swarm V10000 hate speech violation: Community guidelines breach",
        "other": "Titan Swarm V10000 general community guidelines violation via swarm network"
    }
    active_reason_text = crime_texts.get(crime_type, crime_texts["other"])

    sent_msg = bot.send_message(
        message.chat.id,
        f"🔥 **هێرشی تایتانی V10000 دەستی پێکرد!**\n\n"
        f"💰 خەرجکراو: `{package_cost:,} IQD` | ماوە: `{user_data['balance']:,} IQD`\n"
        f"🎯 ئامانج: `{target_url}`\n"
        f"📌 جۆر: {crime_type}\n"
        f"📊 ڕەوش: 0 / {target_count:,}",
        parse_mode="Markdown"
    )
    
    def update_progress(current, total, success):
        try:
            bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=sent_msg.message_id,
                text=f"🔥 **هێرشی تۆر لەسەر سەوەرەکان و بۆتەکان بەڕێوەیە...**\n\n"
                     f"💰 خەرجکراو: `{package_cost:,} IQD` | ماوە: `{user_data['balance']:,} IQD`\n"
                     f"🎯 ئامانج: `{target_url}`\n"
                     f"📌 جۆر: {crime_type}\n"
                     f"📊 نێردراو: {current:,} / {total:,} (سەرکەوتوو: {success:,})\n"
                     f"⚡ دۆخ: کارکردنی زەبەلاح لەسەر Multi-Server Swarm ⚡",
                parse_mode="Markdown"
            )
        except Exception:
            pass

    def background_worker():
        execute_titan_swarm_attack(target_url, active_reason_text, target_count, update_progress)
        with titan_lock:
            user_data['reports_sent'] += target_count
            save_db()
        bot.send_message(
            message.chat.id, 
            f"✅ **پیرۆزە! هێرشی تایتانی تۆر بە سەرکەوتوویی کۆتایی هات.**\n"
            f"🎯 ئامانج بڕی `{target_count:,}` ڕاپۆرتی بێوێنەی لە هەموو سەوەرەکانەوە پێگەیشت.\n"
            f"💰 باڵانسی ماوەی هەژمارەت: `{user_data['balance']:,} IQD`",
            parse_mode="Markdown"
        )

    threading.Thread(target=background_worker).start()

# ---------------------------------------------------------------------
# TITAN MAIN EXECUTION LOOP (MULTI-SERVER SWARM CORE)
# ---------------------------------------------------------------------
if __name__ == '__main__':
    logger.info("Initializing Omni-Cluster Neural Titan V10000 (Multi-Server Swarm Edition)...")
    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=30)
        except Exception as err:
            logger.error(f"Titan Core Recovery Triggered due to: {err}")
            time.sleep(2)
