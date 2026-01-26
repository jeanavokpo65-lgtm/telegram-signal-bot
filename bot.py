from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")  # ✅ CORRIGÉ

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot en ligne 🚀")

def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN manquant")

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    print("Bot démarré")
    app.run_polling()

if __name__ == "__main__":
    main()


