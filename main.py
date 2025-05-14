import telebot from telebot import types

TOKEN = '8090137916:AAGIxEJJ0YyUkzFwXyxbJ_9iEkmCutT-CNo' ADMIN_ID = 128473145 CARD_NUMBER = '6104-3376-8005-5348' CARD_OWNER = 'محمد کریم پور' CONFIG_FILE = 'configs.txt'

bot = telebot.TeleBot(TOKEN)

plans = { '۱۰ گیگ - ۳۰ روزه 🚀': ('50,000 تومان', '10GB'), '۲۵ گیگ - ۳۰ روزه ⚡️': ('80,000 تومان', '25GB'), '۴۰ گیگ - ۳۰ روزه 🔥': ('105,000 تومان', '40GB'), '۷۵ گیگ - ۳۰ روزه 🧨': ('180,000 تومان', '75GB'), '۱۰۰ گیگ - ۳۰ روزه 💣': ('240,000 تومان', '100GB') }

حالت حافظه ساده برای نگهداری انتخاب کاربر

user_data = {}

@bot.message_handler(commands=['start']) def send_welcome(message): markup = types.ReplyKeyboardMarkup(resize_keyboard=True) for plan in plans: markup.add(plan) bot.send_message(message.chat.id, 'سلام! خوش اومدی به ربات فروش VPN ما! انتخاب کن:', reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in plans) def send_payment_info(message): price, volume = plans[message.text] user_data[message.chat.id] = message.text  # ذخیره پلن انتخابی text = f"پلن انتخابی: {message.text}\nهزینه: {price}\n\nلطفاً مبلغ رو به شماره کارت زیر واریز کن و رسیدشو بفرست:\n\n{CARD_NUMBER}\nبه نام: {CARD_OWNER}" bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(content_types=['photo']) def handle_photo(message): if message.photo: caption = user_data.get(message.chat.id, 'پلن نامشخص') bot.send_message(message.chat.id, 'رسید دریافت شد. منتظر تایید باش! ✅') bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=f"رسید کاربر: {message.from_user.first_name} ({message.chat.id})\nپلن: {caption}", reply_markup=confirm_keyboard(message.chat.id))

کیبورد تایید/رد برای ادمین

def confirm_keyboard(user_id): markup = types.InlineKeyboardMarkup() markup.add(types.InlineKeyboardButton("✅ تایید", callback_data=f"approve:{user_id}")) markup.add(types.InlineKeyboardButton("❌ رد", callback_data=f"reject:{user_id}")) return markup

@bot.callback_query_handler(func=lambda call: call.data.startswith("approve") or call.data.startswith("reject")) def handle_decision(call): action, user_id = call.data.split(":") user_id = int(user_id)

if call.from_user.id != ADMIN_ID:
    bot.answer_callback_query(call.id, "شما ادمین نیستید!")
    return

if action == 'approve':
    try:
        with open(CONFIG_FILE, 'r') as f:
            configs = f.readlines()
        if configs:
            config = configs.pop(0).strip()
            with open(CONFIG_FILE, 'w') as f:
                f.writelines(configs)
            bot.send_message(user_id, f"کانفیگ شما آماده‌ست!\n\n{config}")
            bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption="✅ تایید شد و کانفیگ ارسال شد.")
        else:
            bot.send_message(user_id, 'فعلاً کانفیگی موجود نیست. لطفاً بعداً امتحان کن.')
            bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption="✅ رسید تایید شد ولی کانفیگی موجود نبود.")
    except Exception as e:
        bot.send_message(ADMIN_ID, f'خطا در ارسال کانفیگ: {e}')
else:
    bot.send_message(user_id, '❌ رسید شما رد شد. لطفاً مجدداً اقدام کنید.')
    bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption="❌ رسید رد شد.")

while True: try: bot.infinity_polling() except Exception as e: print("Bot crashed:", e) time.sleep(5)

