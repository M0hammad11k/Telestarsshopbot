import telebot
from telebot import types

# توکن ربات
BOT_TOKEN = "8090137916:AAGIxEJJ0YyUkzFwXyxbJ_9iEkmCutT-CNo"
bot = telebot.TeleBot(BOT_TOKEN)

# آیدی عددی ادمین
ADMIN_ID = 128473145

# شماره کارت و نام
CARD_NUMBER = "6104-3376-8005-5348"
CARD_NAME = "محمد کریم پور"

# پلن‌ها و قیمت‌ها
plans = {
    "10 گیگ - 30 روزه": "50,000 تومان",
    "25 گیگ - 30 روزه": "80,000 تومان",
    "40 گیگ - 30 روزه": "105,000 تومان",
    "75 گیگ - 30 روزه": "180,000 تومان",
    "100 گیگ - 30 روزه": "240,000 تومان"
}

# ذخیره آی‌دی کاربر و انتخابش برای استفاده بعدی
user_choices = {}

# خواندن کانفیگ از فایل
def get_next_config():
    try:
        with open("configs.txt", "r") as file:
            lines = file.readlines()
        if not lines:
            return None
        config = lines[0].strip()
        with open("configs.txt", "w") as file:
            file.writelines(lines[1:])
        return config
    except Exception as e:
        print("Error reading configs.txt:", e)
        return None

# استارت
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    for title in plans.keys():
        markup.add(types.InlineKeyboardButton(text=title, callback_data=title))
    bot.send_message(message.chat.id, "لطفاً یکی از پلن‌های زیر را انتخاب کنید:", reply_markup=markup)

# انتخاب پلن
@bot.callback_query_handler(func=lambda call: call.data in plans)
def handle_plan_selection(call):
    user_choices[call.from_user.id] = call.data
    price = plans[call.data]
    msg = f"پلن انتخابی شما:\n{call.data}\nقیمت: {price}\n\nلطفاً مبلغ را به کارت زیر واریز کرده و رسید را ارسال کنید:\n\nشماره کارت: {CARD_NUMBER}\nبه نام: {CARD_NAME}"
    bot.send_message(call.from_user.id, msg)

# دریافت عکس رسید
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    if message.from_user.id not in user_choices:
        bot.send_message(message.chat.id, "لطفاً ابتدا یک پلن انتخاب کنید.")
        return

    caption = f"رسید پرداخت از {message.from_user.first_name}\nپلن: {user_choices[message.from_user.id]}"
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅ تأیید", callback_data=f"approve_{message.from_user.id}"),
        types.InlineKeyboardButton("❌ رد", callback_data="reject")
    )
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    bot.send_message(ADMIN_ID, caption, reply_markup=markup)

# تایید / رد پرداخت توسط ادمین
@bot.callback_query_handler(func=lambda call: call.data.startswith("approve_") or call.data == "reject")
def handle_admin_decision(call):
    if call.from_user.id != ADMIN_ID:
        return

    if call.data == "reject":
        bot.send_message(call.message.chat.id, "پرداخت رد شد.")
        return

    user_id = int(call.data.split("_")[1])
    config = get_next_config()
    if config:
        bot.send_message(user_id, f"✅ پرداخت شما تایید شد!\n\nاینم کانفیگ شما:\n{config}")
        bot.send_message(call.message.chat.id, f"کانفیگ برای کاربر {user_id} ارسال شد.")
    else:
        bot.send_message(user_id, "❌ کانفیگی موجود نیست، لطفاً بعداً تلاش کنید.")
        bot.send_message(call.message.chat.id, "کانفیگ موجود نبود.")

# اجرای ربات
bot.infinity_polling()
