import json
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# تنظیمات ربات
TOKEN = "7257981637:AAEUnlnGWsWSBS17WkP_cWvuyQMRvp3ir2I"  # توکن ربات رو جایگزین کن
JSON_FILE = "data_cleaned.json"  # نام فایل JSON

# تابع خواندن داده‌ها از JSON
def load_data():
    with open(JSON_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

# تابع جستجو در JSON
def search_personnel(code):
    data = load_data()  # هر بار داده‌ها را از فایل بخونه
    for record in data:
        if record["کدپرسنلی"] == code:  # تصحیح نام کلید
            return (
                f"🔹 نام: {record['نام']} {record['نام خانوادگی']}\n"
                f"🔹 مجموع: {record['مجموع']}\n"
                f"🔹 سود عضویت: {record['سود عضویت']}\n"
                f"🔹 سود فروش 1401: {record['سود فروش 1401']}\n"
                f"🔹 سرمایه سال 1401: {record['سرمایه سال 1401']}"
            )
    return "❌ کد پرسنلی یافت نشد!"

# پاسخ به پیام‌های کاربر
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text.strip()
    print(f"📩 پیام دریافت شد: {user_input}")  # پیام دریافتی را در کنسول نمایش بده
    
    response = search_personnel(user_input)  # جستجو در JSON
    print(f"📤 پاسخ ارسال شد: {response}")  # نمایش پیام ارسال‌شده در کنسول

    await update.message.reply_text(response)

# راه‌اندازی ربات
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("👋 سلام! کد پرسنلی رو بفرست تا اطلاعات نمایش داده بشه.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()