import logging

from telegram import Update
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(level=logging.INFO)
ASK_NAME, ASK_AGE = range(2)

async def conv_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Hi! What's your name?")
    return ASK_NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["name"] = update.message.text
    await update.message.reply_text("How old are you?")
    return ASK_AGE

async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    name = context.user_data["name"]
    age = update.message.text
    await update.message.reply_text(f"Nice to meet you, {name}. You're {age} years old!")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Conversation cancelled.")
    return ConversationHandler.END

conv_handler = ConversationHandler(
        entry_points=[CommandHandler("conv", conv_start)],
        states={
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            ASK_AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )