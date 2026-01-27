from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import random


TOKEN = os.getenv("BOT_TOKEN")  # ✅ CORRIGÉ
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")

if not GROUP_CHAT_ID:
    raise RuntimeError("GROUP_CHAT_ID manquant")

GROUP_CHAT_ID = int(GROUP_CHAT_ID)


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

async def chatid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Chat ID = {update.effective_chat.id}"
    )

async def auto_signal(context: ContextTypes.DEFAULT_TYPE):
    rsi = random.randint(10, 90)

    if rsi < 30:
        decision = "🟢 BUY"
    elif rsi > 70:
        decision = "🔴 SELL"
    else:
        decision = "🟡 HOLD"

    message = (
        f"📊 SIGNAL AUTOMATIQUE\n"
        f"RSI : {rsi}\n"
        f"Décision : {decision}"
    )

    await context.bot.send_message(
        chat_id=GROUP_CHAT_ID,
        text=message
    )

async def debug(update, context):
    chat = update.effective_chat
    await update.message.reply_text(
        f"Chat type: {chat.type}\nChat ID: {chat.id}"
    )



def main():
    if not TOKEN or not GROUP_CHAT_ID:
        raise RuntimeError("Variables manquantes")

    app = ApplicationBuilder().token(TOKEN).build()

    # commande manuelle (optionnelle)
    app.add_handler(CommandHandler("signal", signal))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("chatid", chatid))
    app.add_handler(MessageHandler(filters.ALL, debug))


    # ⏱️ AUTOMATISATION : toutes les 15 minutes
    app.job_queue.run_repeating(
        auto_signal,
        interval=7200,  # 7200 secondes = 2 heures
        first=10       # démarre après 10 secondes
    )

    print("🤖 Bot démarré avec automatisation")
    app.run_polling()


if __name__ == "__main__":
    main()











