import os
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")  # Токен из переменных окружения

async def sleepy_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("У меня технические работы, сорян. ")

def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN не задан! Укажи токен в переменных окружения.")
    
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, sleepy_reply))
    print("Бот запущен...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()