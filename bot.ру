import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

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

    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "inputs": {
            "current_date": "09.04.2026",
            "user_name": user_name
        },
        "query": user_message,
        "user": str(user_id),
        "response_mode": "blocking"
    }
    
    try:
        response = requests.post(DIFY_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        reply = response.json()["answer"]
        await update.message.reply_text(reply)
    except Exception as e:
        print(f"Ошибка: {e}")
        await update.message.reply_text("Ой, что-то я зависла... Попробуй ещё 😕")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Аня запущена через Dify Cloud! Ожидаю сообщения...")
    app.run_polling()

if __name__ == "__main__":
    main()
