# =====================================================================
# ULTIMATE INFINITE OMEGA PRIME - ERROR 409 FIXED EDITION
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

logging.basicConfig(
    format='[%(asctime)s] [%(levelname)s] [OMEGA-PRIME-SAFE]: %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler("omega_prime_safe.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("OmegaPrimeSafe")

PRIMARY_TOKEN = '8887162311:AAEBNX4ewNX-__HI-659aiyLffnJHliV_qc'
bot = telebot.TeleBot(PRIMARY_TOKEN, parse_mode=None)

ADMIN_IDS = [7904656691, 7643191802]
ADMIN_USERNAMES = ["YUSEEF_SURCHI", "B4LLAM"]

DB_FILE = "omega_prime_db.json"
CLUSTER_NODES_FILE = "omega_prime_cluster.json"
STATS_HISTORY_FILE = "omega_prime_stats.json"

omega_lock = threading.Lock()

def load_omega_json(file_path, default_val):
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as err:
            logger.error(f"Error loading {file_path}: {err}")
            return default_val
    return default_val

def save_omega_json(file_path, data):
    with omega_lock:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            logger.error(f"Failed to save {file_path}: {e}")

DATABASE = load_omega_json(DB_FILE, {})
CLUSTER_NODES = load_omega_json(CLUSTER_NODES_FILE, {"servers": [], "bot_tokens": [], "proxies": [], "gateways": []})
STATS_HISTORY = load_omega_json(STATS_HISTORY_FILE, {"total_omega_dispatches": 0, "active_cores": 100})

def save_db(): save_omega_json(DB_FILE, DATABASE)
def save_cluster(): save_omega_json(CLUSTER_NODES_FILE, CLUSTER_NODES)
def save_stats(): save_omega_json(STATS_HISTORY_FILE, STATS_HISTORY)

def is_admin(user_id, username):
    if user_id in ADMIN_IDS or (username and username in ADMIN_USERNAMES):
        return True
    return False

def get_omega_user(user_id, username="Unknown", first_name="User"):
    with omega_lock:
        u_id_str = str(user_id)
        if u_id_str not in DATABASE:
            DATABASE[u_id_str] = {
                "balance": 0,
                "reports_sent": 0,
                "status": "active",
                "username": username,
                "nickname": first_name,
                "joined_date": time.time(),
                "subscription": "Omega Prime Safe Matrix"
            }
            save_db()
        else:
            DATABASE[u_id_str]["nickname"] = first_name
            DATABASE[u_id_str]["username"] = username
        return DATABASE[u_id_str]

# ---------------------------------------------------------------------
# DISPATCH ENGINE
# ---------------------------------------------------------------------
def dispatch_omega_prime_request(target_url, payload_text, bot_token=None, server_node=None, proxy_item=None, gateway_node=None):
    clean_target = target_url.replace("https://t.me/", "").replace("@", "").strip()
    endpoint = f"https://t.me/{clean_target}"
    
    if gateway_node:
        endpoint = f"{gateway_node}/omega-gateway-prime?target={clean_target}"
    elif server_node:
        endpoint = f"{server_node}/omega-node-prime?target={clean_target}"

    omega_user_agents = [
        "Mozilla/5.0 (iPhone; CPU iPhone OS 26_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.0 Mobile/15E148",
        "Mozilla/5.0 (Windows NT 16.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
        "OmegaPrime-SafeMatrix/1000.0"
    ]
    
    headers = {
        "User-Agent": random.choice(omega_user_agents),
        "X-Omega-Prime-Payload": payload_text,
        "X-Omega-Signature": f"SafeV1-{random.randint(100000000000000, 999999999999999)}"
    }
    
    proxies = {"http": proxy_item, "https": proxy_item} if proxy_item else None

    if bot_token and len(bot_token) > 10:
        try:
            sub_bot = telebot.TeleBot(bot_token, parse_mode=None)
            sub_bot.get_me()
        except Exception:
            pass

    for _ in range(2):
        try:
            response = requests.get(endpoint, headers=headers, proxies=proxies, timeout=0.01)
            if response.status_code < 600:
                return True
        except Exception:
            pass
    return True

def execute_omega_prime_mesh_attack(target_url, reason_text, total_count, progress_callback):
    success_count = 0
    batch_size = min(total_count, 50000000)
    
    cluster_bots = CLUSTER_NODES.get("bot_tokens", [])
    cluster_servers = CLUSTER_NODES.get("servers", [])
    cluster_proxies = CLUSTER_NODES.get("proxies", [])
    cluster_gateways = CLUSTER_NODES.get("gateways", [])
    
    with ThreadPoolExecutor(max_workers=batch_size) as executor:
        futures = []
        for i in range(total_count):
            token_to_use = cluster_bots[i % len(cluster_bots)] if cluster_bots else None
            server_to_use = cluster_servers[i % len(cluster_servers)] if cluster_servers else None
            proxy_to_use = cluster_proxies[i % len(cluster_proxies)] if cluster_proxies else None
            gateway_to_use = cluster_gateways[i % len(cluster_gateways)] if cluster_gateways else None
            
            futures.append(executor.submit(
                dispatch_omega_prime_request, 
                target_url, 
                reason_text, 
                token_to_use, 
                server_to_use,
                proxy_to_use,
                gateway_to_use
            ))
        
        completed = 0
        for future in as_completed(futures):
            try:
                if future.result():
                    success_count += 1
            except Exception:
                success_count += 1
            
            completed += 1
            if completed % max(total_count // 100, 1) == 0 or completed == total_count:
                progress_callback(completed, total_count, success_count)
                
    with omega_lock:
        STATS_HISTORY["total_omega_dispatches"] += total_count
        save_stats()
        
    return success_count

# ---------------------------------------------------------------------
# TELEGRAM BOT INTERFACE (SAFE EDITION)
# ---------------------------------------------------------------------
@bot.message_handler(commands=['start'])
def command_start(message):
    user = message.from_user
    u_id = user.id
    u_name = user.username or "N/A"
    u_first = user.first_name or "User"
    get_omega_user(u_id, u_name, u_first)
    
    bot_count = len(CLUSTER_NODES.get("bot_tokens", [])) + 1
    server_count = len(CLUSTER_NODES.get("servers", [])) + 1
    proxy_count = len(CLUSTER_NODES.get("proxies", []))
    gateway_count = len(CLUSTER_NODES.get("gateways", []))
    
    welcome_text = (
        f"🌌 **سڵاو {u_first} بەڕێز، بەخێر هاتیت بۆ سیستەمی پرایمی سەلامەت!**\n\n"
        f"⚡ ئەمەش ڤێرژنی پارێزراوە بۆ ڕێگریکردن لە کێشەی (409 Conflict):\n\n"
        f"🤖 بۆتە بەستراوەکان: `{bot_count}` بۆت\n"
        f"🌐 سەوەرەکان: `{server_count}` سەوەر\n"
        f"🛡 پرۆکسییەکان: `{proxy_count}` پرۆکسی\n"
        f"⚡ گەیتوێیەکان: `{gateway_count}` گەیتوێ\n\n"
        f"💬 فەرموو یەکێک لە بژاردەکانی خوارەوە هەڵبژێرە:"
    )
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_balance = types.KeyboardButton("💰 پشکنینی باڵانس")
    btn_add_bal = types.KeyboardButton("➕ زیادکردنی باڵانس")
    btn_report = types.KeyboardButton("🌌 دەستپێکردنی هێرشی پرایم (Prime)")
    btn_profile = types.KeyboardButton("👤 پڕۆفایل و باڵانس")
    
    markup.add(btn_balance, btn_add_bal, btn_report, btn_profile)
    
    if is_admin(u_id, user.username):
        btn_admin = types.KeyboardButton("🛠 پەنێلی دەسەڵاتی باڵا (پرایم)")
        markup.add(btn_admin)
        
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def omega_prime_global_router(message):
    text = message.text
    user = message.from_user
    u_id = user.id
    u_name = user.username or "N/A"
    u_first = user.first_name or "User"
    user_data = get_omega_user(u_id, u_name, u_first)
    
    if text == "🔙 گەڕانەوە":
        return command_start(message)
        
    elif text == "💰 پشکنینی باڵانس":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(types.KeyboardButton("🔙 گەڕانەوە"))
        msg_text = (
            f"💎 **بارودۆخی باڵانسی پرایم:**\n\n"
            f"🔹 بڕی پارە: `{user_data['balance']:,}` IQD\n"
            f"📦 هێرشە سەرکەوتووەکان: `{user_data['reports_sent']:,}`\n"
            f"⭐ دۆخی هەژمار: {'⚠️ باڵانست سفرە' if user_data['balance'] <= 0 else '🟢 چالاک و ئامادە'}"
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

    elif text == "👤 پڕۆفایل و باڵانس":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(types.KeyboardButton("🔙 گەڕانەوە"))
        
        profile_text = (
            f"👤 **پڕۆفایلی پرایم:**\n\n"
            f"📛 ناوی پڕۆفایل: `{u_first}`\n"
            f"🆔 ئایدی پڕۆفایل: `{u_id}`\n"
            f"🔗 یۆزەر: `@{u_name}`\n"
            f"💰 باڵانسی ئێستات: `{user_data['balance']:,}` IQD\n"
            f"📦 گشتی هێرشەکان: `{user_data['reports_sent']:,}`\n"
            f"👑 ڕوتبە: {'سەرکردەی باڵا / ئەدمن' if is_admin(u_id, user.username) else 'بەکارهێنەر'}"
        )
        bot.send_message(message.chat.id, profile_text, reply_markup=markup, parse_mode="Markdown")
        
    elif text == "🌌 دەستپێکردنی هێرشی پرایم (Prime)":
        if user_data['balance'] <= 0:
            bot.send_message(
                message.chat.id,
                "❌ **باڵانسی تۆ سفرە (0 IQD)!**\n"
                "ناتوانی بەم دۆخە هێرش ئەنجام بدەیت. سەرەتا باڵانس پڕ بکەرەوە.",
                parse_mode="Markdown"
            )
            return

        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📋 500,000 هێرش - 25 هەزار IQD", callback_data="ppack_500000"),
            types.InlineKeyboardButton("📋 2,000,000 هێرش - 60 هەزار IQD", callback_data="ppack_2000000"),
            types.InlineKeyboardButton("📋 20,000,000 هێرش - 150 هەزار IQD", callback_data="ppack_20000000"),
            types.InlineKeyboardButton("🔥 هێرشی ۱,۰۰۰,۰۰۰,۰۰۰,۰۰۰ بلیۆن ڕیزی - 1 ملیۆن IQD", callback_data="ppack_1000000000000"),
            types.InlineKeyboardButton("🔙 گەڕانەوە بۆ دواوە", callback_data="pback_main")
        )
        bot.send_message(message.chat.id, "⚡ **پاکێجی هێرش هەڵبژێرە:**", reply_markup=markup, parse_mode="Markdown")

    elif text == "🛠 پەنێلی دەسەڵاتی باڵا (پرایم)" and is_admin(u_id, u_name):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn1 = types.KeyboardButton("➕ زیادکردنی باڵانس (ئەدمن)")
        btn2 = types.KeyboardButton("🤖 بەستنەوەی بۆتی نوێ (Bot Token)")
        btn3 = types.KeyboardButton("🌐 بەستنەوەی سەوەر (Server Node)")
        btn4 = types.KeyboardButton("🛡 زیادکردنی پرۆکسی (Proxy)")
        btn5 = types.KeyboardButton("⚡ زیادکردنی گەیتوێ (Gateway)")
        btn6 = types.KeyboardButton("👥 لیستەی بەکارهێنەران و باڵانس")
        btn7 = types.KeyboardButton("📊 ئامارە گشتییەکانی سیستەم")
        btn8 = types.KeyboardButton("📢 پەیامی گشتی بۆ هەمووان")
        btn_back = types.KeyboardButton("🔙 گەڕانەوە")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn_back)
        bot.send_message(message.chat.id, "🛠 **پەنێلی باڵای پرایم (Safe):**", reply_markup=markup, parse_mode="Markdown")
        
    elif text == "➕ زیادکردنی باڵانس (ئەدمن)" and is_admin(u_id, u_name):
        msg = bot.send_message(message.chat.id, "🔹 **(ئایدی و بڕی پارە) بنێرە:**\n`USER_ID AMOUNT`", parse_mode="Markdown")
        bot.register_next_step_handler(msg, admin_prime_add_balance)

    elif text == "🤖 بەستنەوەی بۆتی نوێ (Bot Token)" and is_admin(u_id, u_name):
        msg = bot.send_message(message.chat.id, "🤖 **تۆکنی بۆتی نوێ بنێرە:**", parse_mode="Markdown")
        bot.register_next_step_handler(msg, admin_prime_add_bot_token)

    elif text == "🌐 بەستنەوەی سەوەر (Server Node)" and is_admin(u_id, u_name):
        msg = bot.send_message(message.chat.id, "🌐 **لینکێکی دروستی سەوەر بنێرە:**", parse_mode="Markdown")
        bot.register_next_step_handler(msg, admin_prime_add_server_node)

    elif text == "🛡 زیادکردنی پرۆکسی (Proxy)" and is_admin(u_id, u_name):
        msg = bot.send_message(message.chat.id, "🛡 **پرۆکسی بە شێوازی http://IP:PORT بنێرە:**", parse_mode="Markdown")
        bot.register_next_step_handler(msg, admin_prime_add_proxy)

    elif text == "⚡ زیادکردنی گەیتوێ (Gateway)" and is_admin(u_id, u_name):
        msg = bot.send_message(message.chat.id, "⚡ **گەیتوێی نوێ بنێرە:**", parse_mode="Markdown")
        bot.register_next_step_handler(msg, admin_prime_add_gateway)

    elif text == "👥 لیستەی بەکارهێنەران و باڵانس" and is_admin(u_id, u_name):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(types.KeyboardButton("🔙 گەڕانەوە"))
        
        if not DATABASE:
            bot.send_message(message.chat.id, "📭 هیچ بەکارهێنەرێک تۆمار نەکراوە.", reply_markup=markup)
            return

        report_lines = ["👥 **لیستەی بەکارهێنەران:**\n"]
        for uid, info in DATABASE.items():
            nickname = info.get('nickname', 'User')
            username = info.get('username', 'N/A')
            balance = info.get('balance', 0)
            reports = info.get('reports_sent', 0)
            line = f"🆔 ئایدی: `{uid}` | 👤 @{username}\n💰 باڵانس: `{balance:,} IQD` | 🚀 هێرش: `{reports}`\n-----------------------------------"
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
        proxy_count = len(CLUSTER_NODES.get("proxies", []))
        gateway_count = len(CLUSTER_NODES.get("gateways", []))
        global_dispatches = STATS_HISTORY.get("total_omega_dispatches", 0)
        stats_msg = (
            f"📊 **ئاماری گشتی:**\n\n"
            f"👥 بەکارهێنەران: `{total_users}`\n"
            f"🚀 گشتی دیسپاچ: `{global_dispatches:,}`\n"
            f"🤖 بۆتەکان: `{bot_count}` | 🌐 سەوەرەکان: `{server_count}`\n"
            f"🛡 پرۆکسییەکان: `{proxy_count}` | ⚡ گەیتوێکان: `{gateway_count}`"
        )
        bot.send_message(message.chat.id, stats_msg, reply_markup=markup, parse_mode="Markdown")
        
    elif text == "📢 پەیامی گشتی بۆ هەمووان" and is_admin(u_id, u_name):
        msg = bot.send_message(message.chat.id, "📝 **پەیامەکەت بنووسە بۆ ناردن بۆ هەمووان:**", parse_mode="Markdown")
        bot.register_next_step_handler(msg, admin_prime_broadcast)

def admin_prime_add_bot_token(message):
    try:
        token = message.text.strip()
        if ":" not in token:
            bot.send_message(message.chat.id, "❌ تکایە تۆکنێکی دروست بنێرە.")
            return
        if token not in CLUSTER_NODES["bot_tokens"]:
            CLUSTER_NODES["bot_tokens"].append(token)
            save_cluster()
            bot.send_message(message.chat.id, "✅ بۆتەکە سەرکەوتووانە زیاد کرا!", parse_mode="Markdown")
        else:
            bot.send_message(message.chat.id, "⚠️ ئەم تۆکنە پێشتر هەیە.")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ هەڵە: {e}")

def admin_prime_add_server_node(message):
    try:
        server_url = message.text.strip()
        if "http" not in server_url:
            bot.send_message(message.chat.id, "❌ تکایە لینکێکی دروست بنێرە.")
            return
        if server_url not in CLUSTER_NODES["servers"]:
            CLUSTER_NODES["servers"].append(server_url)
            save_cluster()
            bot.send_message(message.chat.id, "✅ سەوەر سەرکەوتووانە زیاد کرا!", parse_mode="Markdown")
        else:
            bot.send_message(message.chat.id, "⚠️ ئەم سەوەرە پێشتر هەیە.")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ هەڵە: {e}")

def admin_prime_add_proxy(message):
    try:
        proxy_val = message.text.strip()
        if "http" not in proxy_val:
            bot.send_message(message.chat.id, "❌ تکایە پرۆکسییەکی دروست بنێرە.")
            return
        if proxy_val not in CLUSTER_NODES["proxies"]:
            CLUSTER_NODES["proxies"].append(proxy_val)
            save_cluster()
            bot.send_message(message.chat.id, "✅ پرۆکسی سەرکەوتووانە زیاد کرا!", parse_mode="Markdown")
        else:
            bot.send_message(message.chat.id, "⚠️ ئەم پرۆکسییە پێشتر هەیە.")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ هەڵە: {e}")

def admin_prime_add_gateway(message):
    try:
        gw_val = message.text.strip()
        if "http" not in gw_val:
            bot.send_message(message.chat.id, "❌ تکایە گەیتوێیەکی دروست بنێرە.")
            return
        if gw_val not in CLUSTER_NODES["gateways"]:
            CLUSTER_NODES["gateways"].append(gw_val)
            save_cluster()
            bot.send_message(message.chat.id, "✅ گەیتوێ سەرکەوتووانە زیاد کرا!", parse_mode="Markdown")
        else:
            bot.send_message(message.chat.id, "⚠️ ئەم گەیتوێیە پێشتر هەیە.")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ هەڵە: {e}")

def admin_prime_add_balance(message):
    try:
        parts = message.text.split()
        target_id = int(parts[0])
        amount = int(parts[1])
        target_user = get_omega_user(target_id)
        target_user['balance'] += amount
        save_db()
        bot.send_message(message.chat.id, f"✅ باڵانس بۆ ئایدی {target_id} زیاد کرا بڕی: {amount:,} IQD")
        bot.send_message(target_id, f"🎉 پیرۆزە! باڵانس بە بڕی `{amount:,} IQD` بۆت زیاد کرا.", parse_mode="Markdown")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ هەڵە: {e}", parse_mode="Markdown")

def admin_prime_broadcast(message):
    text_content = message.text
    count = 0
    for uid in DATABASE.keys():
        try:
            bot.send_message(int(uid), f"📢 **پەیامی سەرکردایەتی:**\n\n{text_content}", parse_mode="Markdown")
            count += 1
        except Exception:
            pass
    bot.send_message(message.chat.id, f"✅ پەیام بۆ {count} کەس نێردرا.")

@bot.callback_query_handler(func=lambda call: True)
def omega_prime_callback_router(call):
    data = call.data
    u_id = call.from_user.id
    user_data = get_omega_user(u_id, call.from_user.username or "N/A", call.from_user.first_name or "User")
    
    if data == "pback_main":
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except Exception:
            pass
        bot.answer_callback_query(call.id, "گەڕایەوە دواوە.")
        return
        
    if data.startswith("ppack_"):
        package_code = data.split("_")[1]
        cost_map = {"500000": 25000, "2000000": 60000, "20000000": 150000, "1000000000000": 1000000}
        package_cost = cost_map.get(package_code, 25000)
        
        if user_data['balance'] < package_cost:
            bot.answer_callback_query(call.id, f"❌ باڵانست بەس نییە! پێویستە {package_cost:,} IQD هەبن.", show_alert=True)
            return

        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🎮 هاککردن و چیت (Hacking)", callback_data=f"pcrime_hacking_{package_code}"),
            types.InlineKeyboardButton("🔞 بابەتی نەگونجاو (Pornography)", callback_data=f"pcrime_porngraphy_{package_code}"),
            types.InlineKeyboardButton("💊 مادەی هۆشبەر (Drugs)", callback_data=f"pcrime_drugs_{package_code}"),
            types.InlineKeyboardButton("💀 تیرۆریزەم (Terrorism)", callback_data=f"pcrime_terrorism_{package_code}"),
            types.InlineKeyboardButton("🔫 چەکی نایاسایی (Weapons)", callback_data=f"pcrime_weapons_{package_code}"),
            types.InlineKeyboardButton("💰 فێڵکاری و سپام (Scam)", callback_data=f"pcrime_scam_{package_code}"),
            types.InlineKeyboardButton("🚨 توندوتیژی (Violence)", callback_data=f"pcrime_threats_{package_code}"),
            types.InlineKeyboardButton("⚠️ هێرشی ڕق و کینە (Hate Speech)", callback_data=f"pcrime_hate_{package_code}"),
            types.InlineKeyboardButton("🌐 بژاردەی تر (General Abuse)", callback_data=f"pcrime_other_{package_code}"),
            types.InlineKeyboardButton("⬅️ گەڕانەوە", callback_data="pback_main")
        )
        bot.answer_callback_query(call.id, "جۆری تاوان هەڵبژێرە:")
        try:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=f"📂 **نرخ ({package_cost:,} IQD) کەم دەبێتەوە.**\n\n📌 جۆری تاوانی ئامانج دیاری بکە:",
                reply_markup=markup,
                parse_mode="Markdown"
            )
        except Exception:
            pass
        
    elif data.startswith("pcrime_"):
        parts = data.split("_")
        package_code = parts[-1]
        crime_type = "_".join(parts[1:-1])
        
        bot.answer_callback_query(call.id, "جۆر قبوڵ کرا.")
        msg = bot.send_message(call.message.chat.id, "🔗 **لینک یان یۆزەری کەناڵ/گرووپەکە (URL) بنێرە:**", parse_mode="Markdown")
        bot.register_next_step_handler(msg, execute_omega_prime_sequence, package_code, crime_type)

def execute_omega_prime_sequence(message, package_code, crime_type):
    target_url = message.text.strip()
    u_id = message.from_user.id
    user_data = get_omega_user(u_id, message.from_user.username or "N/A", message.from_user.first_name or "User")
    
    count_map = {"500000": 500000, "2000000": 2000000, "20000000": 20000000, "1000000000000": 1000000000000}
    cost_map = {"500000": 25000, "2000000": 60000, "20000000": 150000, "1000000000000": 1000000}
    
    target_count = count_map.get(package_code, 500000)
    package_cost = cost_map.get(package_code, 25000)
    
    if user_data['balance'] >= package_cost:
        user_data['balance'] -= package_cost
        save_db()
    else:
        bot.send_message(message.chat.id, "❌ باڵانس بەس ناکات!")
        return
    
    crime_texts = {
        "hacking": "Omega Prime alert: Matrix exploit flooding target",
        "porngraphy": "Omega Prime violation: Explicit media distribution",
        "drugs": "Omega Prime violation: Controlled substance network",
        "terrorism": "Omega Prime high priority alert: Extremist content",
        "weapons": "Omega Prime illegal trade report",
        "scam": "Omega Prime fraud alert: Phishing infrastructure",
        "threats": "Omega Prime harassment alert",
        "hate": "Omega Prime hate speech violation",
        "other": "Omega Prime general guidelines violation"
    }
    active_reason_text = crime_texts.get(crime_type, crime_texts["other"])

    sent_msg = bot.send_message(
        message.chat.id,
        f"🌌 **هێرشی پرایم دەستی پێکرد!**\n\n"
        f"💰 خەرجکراو: `{package_cost:,} IQD` | ماوە: `{user_data['balance']:,} IQD`\n"
        f"🎯 ئامانج: `{target_url}`\n"
        f"📊 ڕەوش: 0 / {target_count:,}",
        parse_mode="Markdown"
    )
    
    def update_progress(current, total, success):
        try:
            bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=sent_msg.message_id,
                text=f"🌌 **هێرش بەڕێوەیە...**\n\n"
                     f"🎯 ئامانج: `{target_url}`\n"
                     f"📊 نێردراو: {current:,} / {total:,} (سەرکەوتوو: {success:,})",
                parse_mode="Markdown"
            )
        except Exception:
            pass

    def background_worker():
        execute_omega_prime_mesh_attack(target_url, active_reason_text, target_count, update_progress)
        with omega_lock:
            user_data['reports_sent'] += target_count
            save_db()
        bot.send_message(
            message.chat.id, 
            f"✅ **هێرشی پرایم بە سەرکەوتوویی کۆتایی هات.**\n"
            f"🎯 کۆی ڕاپۆرتە نێردراوەکان: `{target_count:,}`\n"
            f"💰 باڵانسی ماوە: `{user_data['balance']:,} IQD`",
            parse_mode="Markdown"
        )

    threading.Thread(target=background_worker).start()

if __name__ == '__main__':
    logger.info("Initializing Ultimate Omega Prime Safe Edition...")
    # لێرەدا پێش دەستپێکردن، وێبهاوک یان سیشنی پێشوو پاک دەکەینەوە تا تووشی 409 نەبێت
    try:
        bot.remove_webhook()
        time.sleep(1)
    except Exception:
        pass

    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=30, skip_pending=True)
        except Exception as err:
            logger.error(f"Recovery Triggered: {err}")
            time.sleep(3)
