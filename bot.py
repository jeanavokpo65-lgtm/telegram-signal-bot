import os
import logging
from telegram.ext import ApplicationBuilder, CommandHandler

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN manquant")

async def start(update, context):
    await update.message.reply_text("✅ Bot Railway OK")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    logging.info("Bot lancé, attente polling...")
    app.run_polling(
        close_loop=False,
        stop_signals=None
    )

if name == "main":
    main()


