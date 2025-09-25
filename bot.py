import os
import telebot
from telebot import types
from flask import Flask

# === Конфигурация ===
TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = 7132770317

if not TOKEN:
    raise ValueError("❌ BOT_TOKEN не найден. Добавь его в Environment на Render!")

bot = telebot.TeleBot(TOKEN)
waiting_for_message = set()

# === Flask для Render ===
app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Bot is alive!"

# === Главное меню ===
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

# === /start ===
@bot.message_handler(commands=['start'])
def start(message):
    main_menu(message.chat.id)

# === callback кнопки ===
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    msg_id = call.message.message_id

    if call.data == "reviews":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back"))
        bot.edit_message_text(
            "✨ Ваше доверие — моя награда! ✨\n\n"
            "📜 Реальные отзывы: https://t.me/mefik_repa",
            chat_id, msg_id, reply_markup=markup
        )

    elif call.data == "spamblock":
        waiting_for_message.add(chat_id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back"))
        bot.edit_message_text(
            "🚫 У тебя спам-блок? Не беда!\n✍️ Напиши сюда сообщение, и я его получу ✅",
            chat_id, msg_id, reply_markup=markup
        )

    elif call.data == "services":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Заказать ✅", url="tg://resolve?domain=new_swatal"))
        markup.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back"))
        bot.edit_message_text(
            "🤖 Я делаю ботов под клиента:\n\n"
            "🔹 Индивидуальные функции\n🔹 Красивый интерфейс\n🔹 Поддержка 24/7\n\n"
            "✍️ В ЛС напишите:\n`#бот пишите ваши пожелания`",
            chat_id, msg_id, parse_mode="Markdown", reply_markup=markup
        )

    elif call.data == "nft":
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("🛒 Купить", url="tg://resolve?domain=new_swatal"),
            types.InlineKeyboardButton("💰 Продать", url="tg://resolve?domain=new_swatal")
        )
        markup.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back"))
        bot.edit_message_text(
            "💎 NFT — будущее цифровой ценности.\n\n🔥 Почему я?\n"
            "1️⃣ Честные сделки\n2️⃣ Опыт и доверие\n3️⃣ Удобный процесс\n\n"
            "✍️ В ЛС напишите:\n`#нфт пишите цену и добавьте ссылку на гиф`",
            chat_id, msg_id, parse_mode="Markdown", reply_markup=markup
        )

    elif call.data == "site":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔗 Перейти на сайт", url="https://mefik-osint.github.io/osint-ot-mefa/"))
        markup.add(types.InlineKeyboardButton("📩 Связь", url="tg://resolve?domain=new_swatal"))
        markup.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back"))
        bot.edit_message_text(
            "🌐 **Наш OSINT сайт**\n\n"
            "🔍 Все ветви OSINT-инструментов\n📂 Удобная структура\n⚡ Множество тулз\n🛠 Обновления\n\n"
            "👉 https://mefik-osint.github.io/osint-ot-mefa/\n\n"
            "💎 Можно купить доступ к топ-тулзам — свяжитесь с владельцем.\n"
            "📌 (вы можете попросить обзор сайта перед покупкой)",
            chat_id, msg_id, parse_mode="Markdown", reply_markup=markup
        )

    elif call.data == "back":
        main_menu(chat_id, msg_id)

# === Спам-блок ===
@bot.message_handler(func=lambda m: m.chat.id in waiting_for_message, content_types=['text'])
def forward_message(message):
    waiting_for_message.remove(message.chat.id)
    bot.send_message(
        ADMIN_ID,
        f"📩 Новое сообщение от @{message.from_user.username or 'Без ника'}\nID: {message.from_user.id}\nСообщение: {message.text}"
    )
    bot.send_message(message.chat.id, "✅ Твоё сообщение отправлено админу.")

# === Запуск ===
if __name__ == "__main__":
    import threading

    def run_bot():
        bot.infinity_polling()

    threading.Thread(target=run_bot).start()

    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
