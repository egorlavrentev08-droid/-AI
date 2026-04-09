import requests
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = "8219806591:AAHfQIwwwlO2BsGwLAV9THXYXZ8NL6t7hDs"
DIFY_API_KEY = "app-ACJxJNj518KMxGeQ76BfgPl1"
DIFY_URL = "https://api.dify.ai/v1/chat-messages"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text.strip()

    if not user_message:
        return

    logger.info(f"Сообщение: {user_message}")

    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "query": user_message,
        "user": str(user_id),
        "response_mode": "blocking"
    }
    
    try:
        response = requests.post(DIFY_URL, headers=headers, json=payload, timeout=30)
        logger.info(f"Статус: {response.status_code}")
        
        if response.status_code != 200:
            logger.error(f"Ошибка: {response.text}")
            await update.message.reply_text("Ошибка подключения к Dify")
            return
            
        result = response.json()
        reply = result.get("answer", "Не поняла")
        await update.message.reply_text(reply)
        
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await update.message.reply_text("Ошибка, попробуй позже 😕")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Аня запущена!")
    app.run_polling()

if __name__ == "__main__":
    main()
