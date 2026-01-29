from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
)
import os

TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = int(os.environ["CHANNEL_ID"])

async def send_auto_message(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=CHAT_ID,
        text="📢 Message automatique toutes les 3 minutes"
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Lance le job toutes les 3 minutes
    context.job_queue.run_repeating(
        send_auto_message,
        interval=60,
        first=0,
        name="auto_message"
    )
    await update.message.reply_text("✅ Envoi automatique démarré")

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jobs = context.job_queue.get_jobs_by_name("auto_message")
    for job in jobs:
        job.schedule_removal()
    await update.message.reply_text("⛔ Envoi automatique arrêté")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))

    app.run_polling()

if __name__ == "__main__":
    main()
