import requests
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Включаем логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===== НАСТРОЙКИ =====
TELEGRAM_TOKEN = "8219806591:AAHfQIwwwlO2BsGwLAV9THXYXZ8NL6t7hDs"
DIFY_API_KEY = "app-ACJxJNj518KMxGeQ76BfgPl1"
DIFY_URL = "https://api.dify.ai/v1/chat-messages"
# ====================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    user_message = update.message.text.strip()

    if not user_message:
        return

    logger.info(f"Сообщение от {user_name} (ID: {user_id}): {user_message}")

    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "inputs": {
            "current_date": "09.04.2026",
            "user_name": user_name,
            "user_id": str(user_id),
            "user_message": user_message
        },
        "query": user_message,
        "user": str(user_id),
        "response_mode": "blocking"
    }
    
    try:
        logger.info(f"Отправка запроса в Dify...")
        response = requests.post(DIFY_URL, headers=headers, json=payload, timeout=30)
        logger.info(f"Статус ответа Dify: {response.status_code}")
        
        if response.status_code != 200:
            logger.error(f"Ошибка Dify: {response.text}")
            await update.message.reply_text(f"Ошибка API: {response.status_code}")
            return
            
        result = response.json()
        reply = result.get("answer", "Не поняла ответ от Dify")
        logger.info(f"Ответ Ани: {reply[:100]}...")
        await update.message.reply_text(reply)
        
    except requests.exceptions.Timeout:
        logger.error("Таймаут подключения к Dify")
        await update.message.reply_text("Dify не отвечает, попробуй позже 😕")
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await update.message.reply_text(f"Ошибка: {str(e)[:100]}")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Аня запущена через Dify Cloud! Ожидаю сообщения...")
    app.run_polling()

if __name__ == "__main__":
    main()
