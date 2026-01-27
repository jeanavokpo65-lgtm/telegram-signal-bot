from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import random


TOKEN = os.getenv("BOT_TOKEN")  # ✅ CORRIGÉ

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot en ligne 🚀")

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rsi = random.randint(10, 90)

    if rsi < 30:
        decision = "🟢 BUY"
    elif rsi > 70:
        decision = "🔴 SELL"
    else:
        decision = "🟡 HOLD"

    message = (
        f"📊 Signal Trading\n"
        f"RSI : {rsi}\n"
        f"Décision : {decision}"
    )

    await update.message.reply_text(message)


def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN manquant")

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))

    print("Bot démarré")
    app.run_polling()

if __name__ == "__main__":
    main()



