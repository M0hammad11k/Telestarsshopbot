import telebot
from telebot import types

# توکن ربات
TOKEN = '8090137916:AAGIxEJJ0YyUkzFwXyxbJ_9iEkmCutT-CNo'
bot = telebot.TeleBot(TOKEN)

# آیدی عددی محمد (ادمین)
ADMIN_ID = 128473145

# توابع کمکی
def get_next_config():
    try:
        with open("configs.txt", "r") as file:
            lines = file.readlines()

        if not lines:
            return "❌ کانفیگی باقی نمونده! لطفاً کانفیگ جدید وارد کن."

        config = lines[0].strip()
        with open("configs.txt", "w") as file:
            file.writelines(lines[1:])  # حذف کانفیگ فرستاده‌شده

        return f"✅ کانفیگ شما:\n{config}\n\nلطفاً بدون اجازه به کسی ندید."
    except:
        return "❌ خطا در خواندن فایل کانفیگ."

# منوی شروع
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("پلن ۱۰ گیگ", "پلن ۲۵ گیگ")
    markup.add("پلن ۴۰ گیگ", "پلن ۷۵ گیگ")
    markup.add("پلن ۱۰۰ گیگ", "پشتیبانی")
    bot.send_message(message.chat.id, "سلام! یکی از پلن‌ها رو انتخاب کن:", reply_markup=markup)

# هر پلن پیام مخصوص خود را می‌فرستد
def send_plan_info(message, price):
    bot.send_message(message.chat.id,
        f"✅ مبلغ این پلن: {price:,} تومان\n"
        f"💳 شماره کارت:\n6104-3376-8005-5348\n"
        f"به نام *محمد کریم‌پور*\n\n"
        f"لطفاً بعد از پرداخت، عکس رسید رو برام بفرست.",
        parse_mode="Markdown")

@bot.message_handler(func=lambda msg: msg.text == "پلن ۱۰ گیگ")
def plan_10(msg): send_plan_info(msg, 50000)

@bot.message_handler(func=lambda msg: msg.text == "پلن ۲۵ گیگ")
def plan_25(msg): send_plan_info(msg, 80000)

@bot.message_handler(func=lambda msg: msg.text == "پلن ۴۰ گیگ")
def plan_40(msg): send_plan_info(msg, 105000)

@bot.message_handler(func=lambda msg: msg.text == "پلن ۷۵ گیگ")
def plan_75(msg): send_plan_info(msg, 180000)

@bot.message_handler(func=lambda msg: msg.text == "پلن ۱۰۰ گیگ")
def plan_100(msg): send_plan_info(msg, 240000)

# پشتیبانی
@bot.message_handler(func=lambda msg: msg.text == "پشتیبانی")
def support(msg):
    bot.send_message(msg.chat.id, "برای پشتیبانی پیام بده به: @Haj_support")

# رسید پرداخت (عکس) => ارسال برای محمد
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    bot.send_message(message.chat.id, "رسید شما دریافت شد. پس از بررسی، کانفیگ برات ارسال می‌شه.")

# ادمین /ok [user_id] وارد می‌کند => ارسال کانفیگ
@bot.message_handler(commands=['ok'])
def confirm_payment(message):
    if message.from_user.id != ADMIN_ID:
        return

    try:
        chat_id = int(message.text.split()[1])
        config_text = get_next_config()
        bot.send_message(chat_id, config_text)
        bot.send_message(message.chat.id, "کانفیگ برای کاربر ارسال شد.")
    except:
        bot.send_message(message.chat.id, "❌ دستور درست نیست. مثال:\n/ok 123456789")

# اجرای ربات
bot.infinity_polling()
