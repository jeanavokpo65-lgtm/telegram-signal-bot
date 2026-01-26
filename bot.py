import os
from telegram.ext import Application, CommandHandler

TOKEN = os.environ.get("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN manquant")

async def start(update, context):
    await update.message.reply_text("Bot en ligne ✅")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

print("Bot démarré...")
app.run_polling()
