from handlers.gpt import ask_gpt




async def start(update, context):
    await update.message.reply_text("🤖 欢迎使用 GPT-4 群聊机器人！")

async def help_command(update, context):
    await update.message.reply_text("📌 命令列表：/start /help /ask")

async def ask(update, context):
    user_input = ' '.join(context.args)
    if not user_input:
        await update.message.reply_text("请在 /ask 后输入你的问题，例如：/ask 什么是人工智能？")
        return
    reply = ask_gpt(user_input)
    await update.message.reply_text(reply)