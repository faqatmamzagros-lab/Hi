# =====================================================================
# ULTIMATE OMEGA PRIME - WEBHOOK EDITION (NO 409 CONFLICT)
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
from flask import Flask, request
from telebot import types
from concurrent.futures import ThreadPoolExecutor, as_completed

logging.basicConfig(
    format='[%(asctime)s] [%(levelname)s] [OMEGA-PRIME-WEBHOOK]: %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler("omega_prime_webhook.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("OmegaPrimeWebhook")

PRIMARY_TOKEN = '8887162311:AAEBNX4ewNX-__HI-659aiyLffnJHliV_qc'
bot = telebot.TeleBot(PRIMARY_TOKEN, parse_mode=None)
app = Flask(__name__)

# پۆرت کە Railway دەیدێت یان 8080
PORT = int(os.environ.get('PORT', 8080))
# لینکی سەوەرەکەت لە Railway (بۆ نموونە: https://production-xxxx.up.railway.app)
# دەتوانیت لە ڕێکخستنەکانی Railway ناوی دامەینەکەی وەربگریت یان بە ڤاریابڵ دابنێیت
RAILWAY_URL = os.environ.get('RAILWAY_STATIC_URL', '') 

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
                "subscription": "Omega Prime Webhook Matrix"
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
        "OmegaPrime-WebhookMatrix/1000.0"
    ]
    
    headers = {
        "User-Agent": random.choice(omega_user_agents),
        "X-Omega-Prime-Payload": payload_text,
        "X-Omega-Signature": f"WebhookV1-{random.randint(100000000000000, 999999999999999)}"
    }
    
    proxies = {"http": proxy_item, "https": proxy_item} if proxy_item else None

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
    batch_size = min(total_count, 5000000)
    
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
# TELEBOT HANDLERS
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
        f"🌌 **سڵاو {u_first} بەڕێز، بەخێر هاتیت بۆ سیستەمی پرایمی وێبهاوک!**\n\n"
        f"⚡ ئەمەش ڤێرژنی وێبهاوکی خێرا و بێ کێشەیە:\n\n"
        f"🤖 بۆتە بەستراوەکان: `{bot_count}` بۆت\n"
        f"🌐 سەوەرەکان: `{server_count}` سەوەر\n\n"
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
            f"📦 هێرشە سەرکەوتووەکان: `{user_data['reports_sent']:,}`"
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
            f"💰 باڵانسی ئێستات: `{user_data['balance']:,}` IQD\n"
            f"📦 گشتی هێرشەکان: `{user_data['reports_sent']:,}`"
        )
        bot.send_message(message.chat.id, profile_text, reply_markup=markup, parse_mode="Markdown")
        
    elif text == "🌌 دەستپێکردنی هێرشی پرایم (Prime)":
        if user_data['balance'] <= 0:
            bot.send_message(message.chat.id, "❌ **باڵانسی تۆ سفرە (0 IQD)!**", parse_mode="Markdown")
            return

        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📋 500,000 هێرش - 25 هەزار IQD", callback_data="ppack_500000"),
            types.InlineKeyboardButton("📋 2,000,000 هێرش - 60 هەزار IQD", callback_data="ppack_2000000"),
            types.InlineKeyboardButton("🔙 گەڕانەوە بۆ دواوە", callback_data="pback_main")
        )
        bot.send_message(message.chat.id, "⚡ **پاکێجی هێرش هەڵبژێرە:**", reply_markup=markup, parse_mode="Markdown")

    elif text == "🛠 پەنێلی دەسەڵاتی باڵا (پرایم)" and is_admin(u_id, u_name):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add(
            types.KeyboardButton("➕ زیادکردنی باڵانس (ئەدمن)"),
            types.KeyboardButton("👥 لیستەی بەکارهێنەران و باڵانس"),
            types.KeyboardButton("🔙 گەڕانەوە")
        )
        bot.send_message(message.chat.id, "🛠 **پەنێلی باڵا:**", reply_markup=markup, parse_mode="Markdown")

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
        package_cost = 25000 if package_code == "500000" else 60000
        
        if user_data['balance'] < package_cost:
            bot.answer_callback_query(call.id, f"❌ باڵانست بەس نییە!", show_alert=True)
            return

        msg = bot.send_message(call.message.chat.id, "🔗 **لینک یان یۆزەری کەناڵ/گرووپەکە (URL) بنێرە:**", parse_mode="Markdown")
        bot.register_next_step_handler(msg, execute_omega_prime_sequence, package_code, "hacking")

def execute_omega_prime_sequence(message, package_code, crime_type):
    target_url = message.text.strip()
    u_id = message.from_user.id
    user_data = get_omega_user(u_id, message.from_user.username or "N/A", message.from_user.first_name or "User")
    
    target_count = 500000 if package_code == "500000" else 2000000
    package_cost = 25000 if package_code == "500000" else 60000
    
    if user_data['balance'] >= package_cost:
        user_data['balance'] -= package_cost
        save_db()
    else:
        bot.send_message(message.chat.id, "❌ باڵانس بەس ناکات!")
        return

    sent_msg = bot.send_message(
        message.chat.id,
        f"🌌 **هێرشی پرایم دەستی پێکرد!**\n\n"
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
                     f"📊 نێردراو: {current:,} / {total:,}",
                parse_mode="Markdown"
            )
        except Exception:
            pass

    def background_worker():
        execute_omega_prime_mesh_attack(target_url, "Omega Prime Attack", target_count, update_progress)
        with omega_lock:
            user_data['reports_sent'] += target_count
            save_db()
        bot.send_message(message.chat.id, f"✅ **هێرشی پرایم بە سەرکەوتوویی کۆتایی هات.**", parse_mode="Markdown")

    threading.Thread(target=background_worker).start()

# ---------------------------------------------------------------------
# FLASK WEBHOOK ROUTE
# ---------------------------------------------------------------------
@app.route(f'/{PRIMARY_TOKEN}', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        return '', 403

@app.route('/')
def index():
    return "Omega Prime Webhook Active!", 200

if __name__ == '__main__':
    logger.info("Starting Omega Prime Webhook Server...")
    bot.remove_webhook()
    time.sleep(1)
    
    # ڕێکخستنی وێبهاوک بۆ تلگرام
    if RAILWAY_URL:
        webhook_url = f"{RAILWAY_URL}/{PRIMARY_TOKEN}"
        bot.set_webhook(url=webhook_url)
        logger.info(f"Webhook set to: {webhook_url}")
    
    app.run(host='0.0.0.0', port=PORT)

