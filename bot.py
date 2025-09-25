import telebot
from telebot import types

# === ДАННЫЕ ===
TOKEN = "8442027340:AAFQAytkamQfTivxHl9iqMu3qAp7Pb25CI0"
ADMIN_ID = 7132770317  # твой Telegram ID (узнай у @userinfobot)

bot = telebot.TeleBot(TOKEN)
waiting_for_message = set()

# === ГЛАВНОЕ МЕНЮ ===
def main_menu(chat_id, msg_id=None):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✍️ Отзывы", callback_data="reviews"),
        types.InlineKeyboardButton("🚫 Спам блок", callback_data="spamblock")
    )
    markup.add(
        types.InlineKeyboardButton("🤖 Услуги", callback_data="services"),
        types.InlineKeyboardButton("💎 NFT", callback_data="nft")
    )
    markup.add(types.InlineKeyboardButton("🌐 Наш сайт", callback_data="site"))

    text = "📍 Главное меню:\nВыберите раздел 👇"

    if msg_id:
        bot.edit_message_text(text, chat_id, msg_id, reply_markup=markup)
    else:
        bot.send_message(chat_id, text, reply_markup=markup)

# === СТАРТ ===
@bot.message_handler(commands=['start'])
def start(message):
    main_menu(message.chat.id)

# === КНОПКИ ===
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    msg_id = call.message.message_id

    if call.data == "reviews":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back"))
        bot.edit_message_text(
            "✨ Ваше доверие — моя награда! ✨\n\n"
            "📜 Реальные отзывы о моей работе 💎\n\n"
            "👉 Смотри: https://t.me/mefik_repa",
            chat_id,
            msg_id,
            reply_markup=markup
        )

    elif call.data == "spamblock":
        waiting_for_message.add(chat_id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back"))
        bot.edit_message_text(
            "🚫 У тебя спам-блок? Не беда!\n"
            "✍️ Напиши сюда сообщение, и я его лично получу ✅",
            chat_id,
            msg_id,
            reply_markup=markup
        )

    elif call.data == "services":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Заказать ✅", url="tg://resolve?domain=new_swatal"))
        markup.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back"))
        bot.edit_message_text(
            "🤖 Я делаю ботов под клиента:\n\n"
            "🔹 Индивидуальные функции\n"
            "🔹 Красивый интерфейс\n"
            "🔹 Поддержка 24/7\n\n"
            "✍️ В ЛС напишите:\n"
            "`#бот пишите ваши пожелания`",
            chat_id,
            msg_id,
            parse_mode="Markdown",
            reply_markup=markup
        )

    elif call.data == "nft":
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("🛒 Купить", url="tg://resolve?domain=new_swatal"),
            types.InlineKeyboardButton("💰 Продать", url="tg://resolve?domain=new_swatal")
        )
        markup.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back"))
        bot.edit_message_text(
            "💎 NFT — это будущее цифровой ценности.\n\n"
            "🔥 Почему я?\n"
            "1️⃣ Честные сделки\n"
            "2️⃣ Опыт и доверие\n"
            "3️⃣ Удобный процесс\n\n"
            "✍️ В ЛС напишите:\n"
            "`#нфт пишите цену и добавьте ссылку на гиф`",
            chat_id,
            msg_id,
            parse_mode="Markdown",
            reply_markup=markup
        )

    elif call.data == "site":
        markup = types.InlineKeyboardMarkup()
    
        markup.add(types.InlineKeyboardButton("📩 Связь", url="tg://resolve?domain=new_swatal"))
        markup.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back"))
        bot.edit_message_text(
            "🌐 **Наш OSINT сайт**\n\n"
            "🔍 Все ветви OSINT-инструментов\n"
            "📂 Удобная структура\n"
            "⚡ Множество тулз\n"
            "🛠 Постоянные обновления\n\n"
            
            "💎 Можно купить доступ к топ-тулзам — свяжитесь с владельцем.",
            chat_id,
            msg_id,
            parse_mode="Markdown",
            reply_markup=markup
        )

    elif call.data == "back":
        main_menu(chat_id, msg_id)

# === СПАМ-БЛОК ===
@bot.message_handler(func=lambda m: m.chat.id in waiting_for_message, content_types=['text'])
def forward_message(message):
    waiting_for_message.remove(message.chat.id)
    bot.send_message(
        ADMIN_ID,
        f"📩 Новое сообщение от @{message.from_user.username or 'Без ника'}\n"
        f"ID: {message.from_user.id}\n"
        f"Сообщение: {message.text}"
    )
    bot.send_message(message.chat.id, "✅ Твоё сообщение отправлено админу.")

print("Бот запущен...")
bot.infinity_polling()
