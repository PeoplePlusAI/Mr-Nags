import logging
from core.ai import chat
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes, 
    MessageHandler,
    CommandHandler, 
    filters,
)
import os
import dotenv

dotenv.load_dotenv("ops/.env")

token = os.getenv('TELEGRAM_BOT_TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=chat_id, text="Hello I am Mr. Nags, start raising a complaint with hello I have a complaint")

async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat_id = update.effective_chat.id
    print(chat_id)
    response, history = chat(chat_id, text)
    
    await context.bot.send_message(chat_id=chat_id, text=response)


if __name__ == '__main__':
    application = ApplicationBuilder().token(token).read_timeout(30).write_timeout(30).build()
    start_handler = CommandHandler('start', start)
    response_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), respond)
    application.add_handler(response_handler)
    application.add_handler(start_handler)
    application.run_polling()