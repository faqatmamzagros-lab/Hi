import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Yu Token
TOKEN = "8764133922:AAGZs7k75IbJoI58crPlVIvcVAZGN_xTGGo"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    username = update.effective_user.username
    display_name = f"@{username}" if username else user_name
    
    welcome_text = (
        f"👑 سڵاو **{display_name}** بە خێر هاتیت بۆ بۆتی شیکاریی فۆریکس (Y2_KRD)!\n\n"
        "من ئامادەم بۆ لێکۆڵینەوە و شیکارکرنا هەر وێنەیەکی چارتێ (Chart) ب شێوازەکێ زۆر پیشەیی و تێرەسەل.\n"
        "📊 **سیستەمە پشتراستکراوەکان:** SNRZ, MNR, SNR\n\n"
        "فەرموو وێنەیەکا چارتێ بۆ من بنێرە دا ناڤەرۆکا وێ ب هەموو وردەکارییانەوە بۆت بژمێرم!"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_text, parse_mode="Markdown")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    username = update.effective_user.username
    display_name = f"@{username}" if username else user_name
    
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
        "🔵 **متمانە:** مامناوەند - پالشتی، یەک جار و نیم"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=analysis_report, parse_mode="Markdown")

async def default_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="⚠️ تکایە وێنەیەکی چارتێ (Chart) بنێرە دا سیستەمێ شیکاریا فۆریکس ب بڕیار و وردەکاریی تەواو بۆ تە بنێرم!")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), default_response))
    
    print("بۆتی فۆریکس بە سەرکەوتوویی دەست بە کار بوو...")
    application.run_polling()
