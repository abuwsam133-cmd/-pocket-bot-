import time
import requests
import pandas as pd
import pandas_ta as ta
import yfinance as yf

# بيانات البوت
TELEGRAM_BOT_TOKEN = "8782291501:AAHJwkEFKjIrsNveuU6xb1kPJqsb04t8n-k"
TELEGRAM_CHAT_ID = "857751557"
SYMBOL = "EURUSD=X"
TIMEFRAME = "1m"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"حدث خطأ أثناء إرسال الرسالة: {e}")

def check_signals():
    data = yf.download(tickers=SYMBOL, period="1d", interval=TIMEFRAME, progress=False)
    if data.empty:
        return
    
    df = data.copy()
    df['ema9'] = ta.ema(df['Close'], length=9)
    df['ema21'] = ta.ema(df['Close'], length=21)
    df['rsi'] = ta.rsi(df['Close'], length=14)
    
    last_candle = df.iloc[-2]
    prev_candle = df.iloc[-3]
    
    # شرط صعود CALL
    if (prev_candle['ema9'] <= prev_candle['ema21']) and (last_candle['ema9'] > last_candle['ema21']) and (last_candle['rsi'] <= 70):
        msg = f"🟢 **إشارة POCKET OPTION**\n\nالزوج: {SYMBOL}\n الاتجاه: **صعود (CALL / HIGHER)** ⬆️\n المدة: **1 دقيقة**\n RSI: {round(float(last_candle['rsi']), 2)}"
        send_telegram(msg)
        
    # شرط هبوط PUT
    elif (prev_candle['ema9'] >= prev_candle['ema21']) and (last_candle['ema9'] < last_candle['ema21']) and (last_candle['rsi'] >= 30):
        msg = f"🔴 **إشارة POCKET OPTION**\n\nالزوج: {SYMBOL}\n الاتجاه: **هبوط (PUT / LOWER)** ⬇️\n المدة: **1 دقيقة**\n RSI: {round(float(last_candle['rsi']), 2)}"
        send_telegram(msg)

if __name__ == "__main__":
    print("تم تشغيل بوت التوصيات...")
    send_telegram("🚀 **تم تشغيل البوت بنجاح على سيرفر Render المجاني!**")
    
    while True:
        try:
            check_signals()
        except Exception as e:
            print(f"خطأ في التنفيذ: {e}")
        time.sleep(60)
