import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')

if not GEMINI_API_KEY or not TELEGRAM_TOKEN:
    print("CRITICAL ERROR: API keys not found in environment variables.")
    exit()

try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    print("Gemini Model configured successfully!")
except Exception as e:
    print(f"Error configuring Gemini: {e}")
    exit()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_name = update.effective_user.first_name
    await update.message.reply_text(f"أهلاً بك يا {user_name}! أنا بوت مدعوم بـ Gemini. أرسل لي أي سؤال.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    user_message = update.message.text
    await context.bot.send_chat_action(chat_id=chat_id, action='typing')
    try:
        response = model.generate_content(user_message)
        await update.message.reply_text(response.text)
    except Exception as e:
        print(f"Error handling message: {e}")
        await update.message.reply_text("عذرًا، حدث خطأ. الرجاء المحاولة مرة أخرى.")

def main() -> None:
    print("Starting bot...")
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
