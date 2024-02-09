import asyncio
import logging
from core.ai import chat, audio_chat, bhashini_text_chat, bhashini_audio_chat
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
import tempfile
import time
#from tqdm import tqdm
import base64

dotenv.load_dotenv("ops/.env")

token = os.getenv('TELEGRAM_BOT_TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# async def progress_bar(context, chat_id, start_time, update_interval=15, max_duration=90):
#     while True:
#         await asyncio.sleep(update_interval)
#         wait_time = time.time() - start_time
#         if wait_time > max_duration:
#             break
#         await context.bot.send_message(caht_id=chat_id, text="Thank you for your patience. We're wokring on it.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=chat_id, text="Hello I am Mr. Nags, start raising a complaint with me")

async def talk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    chat_id = update.effective_chat.id
    text = update.message.text
    
    # await context.bot.send_message(chat_id=chat_id, text="We're starting the compliant process. Please wait...")
    #update_task = asyncio.create_task(progress_bar(context, chat_id, start_time))

    response, history = bhashini_text_chat(chat_id,text)
    
    # await context.bot.send_message(chat_id=chat_id, text="Thank you for your patience.")
    
    #update_task.cancel()
    await context.bot.send_message(chat_id=chat_id, text=response)
    #end_time = time.time()
    #print(f"history status is {history.get('status')}")
    #print(f"Time taken: {end_time - start_time}")

async def talk__audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Choose a language for audio:\n1. English\n2. Hindi\n3. Punjabi"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    # Handle user's language selection
    async def handle_language_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        selected_language = update.message.text
        if selected_language == "1":
            language = "English"
        elif selected_language == "2":
            language = "Hindi"
        elif selected_language == "3":
            language = "Punjabi"
        else:
            await context.bot.send_message(chat_id=chat_id, text="Invalid selection. Please try again.")
            return

        await context.bot.send_message(chat_id=chat_id, text=f"You selected {language} language.")
    
    
    # getting audio file
    audio_file = await context.bot.get_file(update.message.voice.file_id)

    # Use a temporary file
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=True) as temp_audio_file:
        await audio_file.download_to_drive(custom_path=temp_audio_file.name)
        chat_id = update.effective_chat.id
        print(chat_id)

        # Convert audio file to base64 encoded string
        with open(temp_audio_file.name, "rb") as file:
            audio_data = file.read()
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')

        response, history = bhashini_audio_chat(chat_id, audio_file=audio_base64)
        
        await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

# for getting location,we can use this 
'''async def location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the location and asks for some info about the user."""
    user = update.message.from_user
    user_location = update.message.location
    logger.info(
        "Location of %s: %f / %f", user.first_name, user_location.latitude, user_location.longitude
    )
    await update.message.reply_text(
        "Since you're filing the complaint form your location, we're recording it."
    )'''

async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_time = time.time()
    text = update.message.text
    chat_id = update.effective_chat.id
    wait_message = get_random_wait_messages(
        not_always=True
    )
    if wait_message:
        await context.bot.send_message(chat_id=chat_id, text=wait_message)
    response, history = chat(chat_id, text)
    end_time = time.time()
    print(f"history status is {history.get('status')}")
    print(f"Time taken: {end_time - start_time}")
    await context.bot.send_message(chat_id=chat_id, text=response)



async def respond_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    audio_file = await context.bot.get_file(update.message.voice.file_id)

    # Use a temporary file
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=True) as temp_audio_file:
        await audio_file.download_to_drive(custom_path=temp_audio_file.name)
        chat_id = update.effective_chat.id
        wait_message = get_random_wait_messages(
            not_always=True
        )
        if wait_message:
            await context.bot.send_message(chat_id=chat_id, text=wait_message)
        response_audio, history = audio_chat(
            chat_id, audio_file=open(temp_audio_file.name, "rb")
        )
        response_audio.stream_to_file(temp_audio_file.name)
        duration = get_duration_pydub(temp_audio_file.name)
        await context.bot.send_audio(
            chat_id=chat_id, 
            audio=open(temp_audio_file.name, "rb"), 
            duration=duration, 
            filename="response.wav",
            performer="Mr. Nags",
        )

if __name__ == '__main__':
    application = ApplicationBuilder().token(token).read_timeout(30).write_timeout(30).build()
    start_handler = CommandHandler('start', start)
    # choose language -> then use Bhashini
    response_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), talk)
    audio_handler = MessageHandler(filters.VOICE & (~filters.COMMAND), talk__audio)
    #language_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_language_selection)
    # application.add_handler(language_handler)
    application.add_handler(response_handler)
    application.add_handler(start_handler)
    application.add_handler(audio_handler)
    application.run_polling()