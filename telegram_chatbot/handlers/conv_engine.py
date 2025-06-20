import logging
import requests
import json

from telegram import Update
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(level=logging.INFO)
# conv_api = "http://127.0.0.1:5000/api/chat"
conv_api = "http://management_platform:5000/api/chat"

Prompt = 1

async def conv_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Hi! May I help you with any questions related to food donation or pick up arrangement?")
    return Prompt

async def get_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['prompt'] = update.message.text  # Store the user's message in user_data
    # Prepare the data payload
    data = {
        "message": context.user_data['prompt']  # Use the user's message as the input
    }
    print(data.get('message'))
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    try:
        # Make the API request
        res = requests.post(url=conv_api, json=data, headers=headers, timeout=10)

        # Check if the response status is OK
        if res.status_code == 200:
            reply = res.json().get('reply', "Sorry, I couldn't understand the response.")
            await update.message.reply_text(reply)
        else:
            await update.message.reply_text(f"API returned an error: {res.status_code}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error making API request: {e}")
        await update.message.reply_text("There was an error connecting to the service. Please try again later.")
    except ValueError as e:
        logging.error(f"Error parsing JSON response: {e}")
        await update.message.reply_text("There was an error processing the response. Please try again later.")
    return ConversationHandler.END
#
# async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     name = context.user_data["name"]
#     age = update.message.text
#     await update.message.reply_text(f"Nice to meet you, {name}. You're {age} years old!")
#     return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Conversation cancelled.")
    return ConversationHandler.END

question_handler = ConversationHandler(
        entry_points=[CommandHandler("ask2", conv_start)],
        states={
            Prompt: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_prompt)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )