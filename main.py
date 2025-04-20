import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# توکن ربات تلگرام که از BotFather گرفتی
TOKEN = 'توکن_خودت_اینجا_بذار7439586033:AAGiDXyswJqwvmXeYVHLSnFe6_vvlkRfeKY'

# گرفتن قیمت‌های لحظه‌ای از نوبیتکس
def get_nobitex_prices():
    try:
        response = requests.get("https://api.nobitex.ir/market/stats")
        data = response.json()

        x = float(data['stats']['usdt-irt']['latest'])     # IRT/USDT
        y = float(data['stats']['btc-usdt']['latest'])     # BTC/USDT
        z = float(data['stats']['btc-irt']['latest'])      # IRT/BTC

        return x, y, z
    except Exception as e:
        print("خطا در دریافت اطلاعات:", e)
        return None, None, None

# انجام محاسبه
def calculate(x, y, z):
    if x is None or y is None or z is None:
        return None
    result = (((y * x) - z) / z) * 100
    return result

# تابع پاسخ‌دهی به دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    x, y, z = get_nobitex_prices()
    result = calculate(x, y, z)

    if result is None:
        message = "خطا در دریافت داده‌ها. لطفاً دوباره تلاش کنید."
    else:
        message = f"""قیمت‌های لحظه‌ای:
IRT/USDT = {x}
BTC/USDT = {y}
IRT/BTC = {z}

نتیجه محاسبه:
{result:.2f} درصد
"""

    await update.message.reply_text(message)

# اجرای ربات
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("ربات در حال اجراست...")
    app.run_polling()
