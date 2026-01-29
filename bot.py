from telegram.ext import ApplicationBuilder, ContextTypes
import os

TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = "signal24_1"  # ou -100xxxx

async def send_message(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=CHAT_ID,
        text="📢 Message automatique dans le canal"
    )

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.job_queue.run_repeating(
        send_message,
        interval=60,
        first=0,
        name="canal_job"
    )

    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()

