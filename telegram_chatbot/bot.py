import os

from telegram.ext import Application, CommandHandler, MessageHandler, filters

from handlers.commands import start, help_command, ask
from handlers.mention import handle_mention
from handlers.conversation import conv_handler
from handlers.conv_engine import question_handler

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    # application.add_handler(CommandHandler("ask", ask))
    application.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUP, handle_mention))
    application.add_handler(conv_handler)
    application.add_handler(question_handler)
    application.run_polling()

if __name__ == '__main__':
    main()