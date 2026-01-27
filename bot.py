import os
import pandas as pd
import requests
from datetime import datetime, timezone

from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
)
from telegram import Update

from strategy import check_signal, get_tp_sl

# =========================
# VARIABLES D’ENVIRONNEMENT
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
MODE = os.getenv("MODE", "LIVE")  # PAPER ou LIVE

SYMBOL = "BTCUSDT"
TIMEFRAME = "5m"   # 1m ou 5m
INTERVAL_SECONDS = 300  # 5 minutes

BINANCE_URL = "https://api.binance.com/api/v3/klines"

# =========================
# ÉTAT GLOBAL
# =========================

last_signal_time = None  # évite les doublons


# =========================
# DATA BINANCE
# =========================

def fetch_ohlcv(symbol=SYMBOL, interval=TIMEFRAME, limit=200):
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    response = requests.get(BINANCE_URL, params=params, timeout=10)
    data = response.json()

    df = pd.DataFrame(data, columns=[
        "time", "open", "high", "low", "close", "volume",
        "_", "_", "_", "_", "_", "_"
    ])

    df = df[["time", "open", "high", "low", "close", "volume"]]

    df["time"] = pd.to_datetime(df["time"], unit="ms", utc=True)
    df[["open", "high", "low", "close", "volume"]] = df[
        ["open", "high", "low", "close", "volume"]
    ].astype(float)

    return df


# =========================
# ENVOI SIGNAL CANAL
# =========================

async def send_signal(context, signal, entry, tp, sl, timestamp):
    session = "London / NY"
    emoji = "🟢 BUY" if signal == "BUY" else "🔴 SELL"

    message = (
        f"🚨 SIGNAL LIVE\n\n"
        f"{SYMBOL}\n"
        f"{emoji}\n\n"
        f"Entry: {entry:.2f}\n"
        f"TP: {tp:.2f}\n"
        f"SL: {sl:.2f}\n\n"
        f"Session: {session}\n"
        f"TF: {TIMEFRAME}\n"
        f"Time: {timestamp.strftime('%Y-%m-%d %H:%M UTC')}\n\n"
        f"Strategy: EMA20 EMA50 VWAP\n"
        f"Filters: Volume + ATR"
    )

    if MODE == "LIVE":
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=message
        )


# =========================
# JOB PRINCIPAL
# =========================

async def trading_job(context: ContextTypes.DEFAULT_TYPE):
    global last_signal_time

    try:
        df = fetch_ohlcv()
        signal = check_signal(df)

        if signal in ["BUY", "SELL"]:
            last_candle_time = df.iloc[-1]["time"]

            # évite doublon sur même bougie
            if last_signal_time == last_candle_time:
                return

            entry = df.iloc[-1]["close"]
            tp, sl = get_tp_sl(entry, signal)

            await send_signal(
                context,
                signal,
                entry,
                tp,
                sl,
                last_candle_time
            )

            last_signal_time = last_candle_time

    except Exception as e:
        print(f"[ERROR] {e}")


# =========================
# MAIN
# =========================

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.job_queue.run_repeating(
        trading_job,
        interval=INTERVAL_SECONDS,
        first=10
    )

    print("🤖 Bot lancé en mode:", MODE)
    app.run_polling()


if __name__ == "__main__":
    main()
