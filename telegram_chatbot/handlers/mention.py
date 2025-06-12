def handle_mention(update, context):
    if context.bot.username.lower() in update.message.text.lower():
        update.message.reply_text("👋 你 @ 了我，有问题可以使用 /ask 提问哦！")
