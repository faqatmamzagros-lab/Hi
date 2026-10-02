import os
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

# وەرگرتنا توکنی بۆتی ژ ژینگەها سێرڤەری (Railway Variables)
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
  raise ValueError("8868899334:AAFcfBbSYHDA5_r4iGO3rTycTNaH_yqQPOo")

bot = telebot.TeleBot(TOKEN)

# ناوی کەناڵ و بەستەری کەناڵ بۆ پشکنینی پشتگیری (Force Subscribe)
CHANNEL_USERNAME = "@Tikinfo_krd"  # یان ئایدی/یۆزەری کەناڵەکەت
CHANNEL_LINK = "https://t.me/Tikinfo_krd"

# دیارکرنا خاوەنێن بۆتی
OWNERS = ["@YUSEEF_SURCHI", "@B4llam"]


# فەنکشن بۆ پشکنینی ئایا بەکارهێنەر لە کەناڵدا هەیە یان نا
def check_user_subscription(user_id):
  try:
    member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
    # ئەگەر بەکارهێنەر لە کەناڵدا بێت یان بەڕێوەبەر بێت
    if member.status in ["member", "administrator", "creator"]:
      return True
    return False
  except Exception as e:
    print(f"Error checking subscription: {e}")
    # ئەگەر کێشەیەک هەبوو لە پشکنینەکەدا، دەتوانین ڕێگە بدەین یان بلۆکی بکەین (لێرە بۆ پارێزراوی True دانراوە یان دەتوانرێت بگەڕێتەوە)
    return True


# فەرمانا /start
@bot.message_handler(commands=["start"])
def send_welcome(message):
  user_id = message.from_user.id

  # پشکنینا پشتگیرییا کەناڵی
  if not check_user_subscription(user_id):
    # ئەگەر Join نەبوو، کیبۆردەکەی بۆ دروست دەکەین بۆ داوای Join کردن
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("📢 بەشداریکردن لە کەناڵ (Join)", url=CHANNEL_LINK)
    )
    markup.add(
        InlineKeyboardButton("✅ پشکنینی بەشداریکردن", callback_data="check_sub")
    )

    not_joined_text = (
        "⚠️ **بۆرای بەکارئینانی بۆتەکە، سەرەتا دەبیت لە کەناڵەکەمان ئەندام"
        " ببیت!**\n\nتکایە سەرەتا سەردانی کەناڵی خوارەوە بکە و Join بە، پاشان"
        " کلیک لە دوگمەی پشکنین بکە 👇\n\n🔗 " + CHANNEL_LINK
    )
    bot.send_message(
        message.chat.id,
        not_joined_text,
        parse_mode="Markdown",
        reply_markup=markup,
    )
    return

  # ئەگەر Join بوو، پەیامی سەرەکی نیشان دەدەین
  show_main_menu(message.chat.id)


# فەنکشنی نیشاندانی مێنوی سەرەکی
def show_main_menu(chat_id):
  markup = InlineKeyboardMarkup()
  markup.add(
      InlineKeyboardButton(
          "👨🏼‍💻 خاوەنێن بۆت (Owners)", callback_data="show_owners"
      )
  )
  markup.add(
      InlineKeyboardButton("📊 زانیارییە پێشکەفتییەکان", callback_data="advanced_info")
  )

  welcome_text = (
      "👋🏻 بە خێر هاتیت بۆ بۆتی زانیاریی تیکتۆک!\n\n"
      "👨🏼‍💻 ئەم بۆتە یەکەم بۆتە لە جیهاندا کە هەموو تایبەتمەندییەکی تێدایە. "
      "دەتوانیت هەموو زانیارییەکانی خاوەنی حساپ بدۆزیتەوە وەکو:\n\n"
      "🔹 ناوی حساپ\n"
      "🔸 یۆزەری حساپ\n"
      "✅ تومارکردن (توثیق)\n"
      "📆 مێژووی دروستکردنی حساپ\n"
      "⌚️ مێژووی گۆڕینی ناڤ\n"
      "🥇 ئاستی پشتتیوانی لە لایڤەکان\n"
      "💭 بایۆ\n"
      "📍 وەڵاتی حساپ\n"
      "💬 زمانی حساپ\n"
      "👫 ژمارەی هەڤالان\n"
      "👤 ژمارەی فۆڵۆوەرەکان\n"
      "👥 ژمارەی ئەو کەسانەی زیادکرون\n"
      "👍 ژمارەی لایکەکان\n"
      "📺 ژمارەی ڤیدیۆکان\n"
      "🔴 لایڤ (بث مباشر)\n"
      "📛 ئایدیی حساپ\n"
      "🔑 ئایدیی دووەم (ثانوي)\n\n"
      "🚀 **تایبەتمەندییە پێشکەفتییەکان:**\n"
      "• 🌐 دۆزینەوەی حساپە قەدەغەکراوەکان (محظور)\n"
      "• 🙂 زانینی وەڵاتی ڕاستەقینە + شوێنی ئێستای حساپ (ئەگەر VPN بەکاربێنێت)\n"
      "• 🎵 زانینی ئایا حساپەکە مۆسیقییە یان نە\n"
      "• ▶️️ یوتوب و اینستاگرام و ستۆرییەکان\n\n"
      "✅ ئێستا یۆزەر، ئایدی، یان لینکێ ڤیدیۆ/لایڤ بنێرە بۆ وەرگرتنی زانیارییان! 📊"
  )

  bot.send_message(
      chat_id, welcome_text, parse_mode="Markdown", reply_markup=markup
  )


# مامەلەکرن دگەل دوگمەیێن شاشەیی (Callback Query)
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
  user_id = call.from_user.id

  if call.data == "check_sub":
    if check_user_subscription(user_id):
      bot.answer_callback_query(
          call.id,
          "🎉 پیرۆزە! ئێستا دەتوانیت بۆتەکە بەکاربێنیت.",
          show_alert=True,
      )
      # سڕینەوەی پەیامی داوای بەشداریکردن و نیشاندانی مێنوی سەرەکی
      try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
      except:
        pass
      show_main_menu(call.message.chat.id)
    else:
      bot.answer_callback_query(
          call.id,
          "❌ تۆ هێشتا بەشداری کەناڵ نەکردووە! تکایە سەردانی کەناڵ بکە.",
          show_alert=True,
      )

  elif call.data == "show_owners":
    owners_text = (
        f"👨🏼‍💻 **خاوەن و گەشەپێدەرانی بۆتەکە:**\n\n"
        f"1️⃣ {OWNERS[0]}\n"
        f"2️⃣ {OWNERS[1]}"
    )
    bot.answer_callback_query(call.id, "خاوەنەکانی بۆت دیار کران!")
    bot.send_message(call.message.chat.id, owners_text, parse_mode="Markdown")

  elif call.data == "advanced_info":
    adv_text = (
        "🚀 **تایبەتمەندییە پێشکەفتییەکانی بۆت:**\n\n"
        "• پشکنینی VPN و دیارکرنی وەڵاتی ڕاستەقینە.\n"
        "• دۆزینەوەی ئایا حساپ هکت کراوە یان سۆشیال مێدیای تری بەستووە.\n"
        "• هێنانی تەواوی مێژووی چۆنیەتیی دروستبوون بێ کێشە."
    )
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, adv_text, parse_mode="Markdown")


# وەرگرتنا یۆزەر یان لینک ژ بەکارهێنەری و پشکنینی ئەندامبوون
@bot.message_handler(func=lambda message: True)
def get_tiktok_data(message):
  user_id = message.from_user.id

  # پێش وەرگرتنی هەر داواکارییەک، پشکنین دەکەین کە ئایا لە کەناڵ هەیە یان نا
  if not check_user_subscription(user_id):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("📢 بەشداریکردن لە کەناڵ (Join)", url=CHANNEL_LINK)
    )
    markup.add(
        InlineKeyboardButton("✅ پشکنینی بەشداریکردن", callback_data="check_sub")
    )
    bot.reply_to(
        message,
        "⚠️ **بۆ بەکارئینانی بۆتەکە، تکایە سەرەتا لە کەناڵەکەمان ئەندام"
        " ببە:**\n\n🔗 " + CHANNEL_LINK,
        reply_markup=markup,
    )
    return

  user_input = message.text.strip()
  if user_input.startswith("/"):
    return

  loading_msg = bot.reply_to(
      message,
      f"🔍 خەریکی پشکنینی `{user_input}` هستم...\nچەند چرکەیەک چاوەڕوان بە ⏳",
      parse_mode="Markdown",
  )

  # لێرەدا دەتوانیت API یان سکریپتی تایبەتی خۆت دابنێیت
  result_text = (
      f"✅ **ئەنجامی پشکنین بۆ:** `{user_input}`\n\n"
      "🔹 **ناوی حساپ:** (نموونە)\n"
      "🔸 **یۆزەر:** `{user_input}`\n"
      "📍 **وەڵات:** عێراق\n"
      "👤 **فۆڵۆوەر:** ١٢.٥ هەزار\n"
      "👍 **لایک:** ٥٠ هەزار\n\n"
      "⚠️ *(تێبینی: بۆ چالاککرنی زانیارییە ڕاستەقینەکان، دەتوانیت API یان سکریپتی"
      " تایبەت لێرە ببەستیت)*"
  )

  bot.edit_message_text(
      chat_id=message.chat.id,
      message_id=loading_msg.message_id,
      text=result_text,
      parse_mode="Markdown",
  )


# دەستپێکرنا بۆتی بە شێوەیەکی بەردەوام
if __name__ == "__main__":
  print("Bot with Force Subscribe is running successfully...")
  bot.infinity_polling(skip_pending=True)
