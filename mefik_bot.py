import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor

# Берём токен из переменной окружения
TOKEN = os.environ.get("8374373060:AAEtM7aXDDH8Q77F8xk44L3bEyXqNh-ySz8")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Главное меню после /start
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(KeyboardButton("1️⃣ Заказать услугу"))
main_menu.add(KeyboardButton("2️⃣ Реферальная программа"))
main_menu.add(KeyboardButton("3️⃣ Связаться с владельцем"))
main_menu.add(KeyboardButton("4️⃣ Отзывы"))

# Подменю выбора услуги
services_menu = InlineKeyboardMarkup(row_width=1)
services_menu.add(
    InlineKeyboardButton("Спам-бот", callback_data="spam_bot"),
    InlineKeyboardButton("Индивидуальный бот", callback_data="custom_bot"),
    InlineKeyboardButton("Бот для ответов", callback_data="reply_bot")
)

# Подменю после выбора бота
bot_info_menu = InlineKeyboardMarkup(row_width=1)
bot_info_menu.add(
    InlineKeyboardButton("О боте", callback_data="bot_info"),
    InlineKeyboardButton("Цена", callback_data="bot_price"),
    InlineKeyboardButton("Сделать заказ", callback_data="bot_order")
)
bot_info = {
    "spam_bot": {
        "description": "Автоматизирует массовую рассылку сообщений. Полезен для тестов или уведомлений.",
        "price": "$2"
    },
    "custom_bot": {
        "description": "Создаётся под ваши нужды, индивидуальный функционал и команды.",
        "price": "$5"
    },
    "reply_bot": {
        "description": "Бот для автоматических ответов на сообщения и комментарии.",
        "price": "$2"
    }
}

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    welcome_text = (
        "Приветствуем!\n"
        "Мы предоставляем полный спектр услуг по разработке Telegram-ботов: от концепции до внедрения и поддержки.\n"
        "Наши решения позволяют автоматизировать бизнес-процессы, улучшить коммуникацию с клиентами и увеличить эффективность работы команды.\n"
        "Свяжитесь с разработчиком для консультации или заказа индивидуального проекта."
    )
    await message.answer(welcome_text, reply_markup=main_menu)

@dp.message_handler(lambda message: message.text == "1️⃣ Заказать услугу")
async def order_service(message: types.Message):
    await message.answer("Выберите тип бота:", reply_markup=services_menu)

@dp.message_handler(lambda message: message.text == "2️⃣ Реферальная программа")
async def referral(message: types.Message):
    text = (
        "Почему именно наш сервис?\n"
        "Мы делаем качественные боты, которые реально помогают бизнесу.\n"
        "За каждого приведённого друга вы получаете скидку 5%!"
    )
    back = ReplyKeyboardMarkup(resize_keyboard=True)
    back.add(KeyboardButton("⬅️ Назад"))
    await message.answer(text, reply_markup=back)

@dp.message_handler(lambda message: message.text == "3️⃣ Связаться с владельцем")
async def contact_owner(message: types.Message):
    text = (
        "Свяжитесь с владельцем:\n"
        "Ответ в течение 5 часов.\n"
        "Спамить запрещено.\n"
        "Юзер: @mefik_out"
    )
    back = ReplyKeyboardMarkup(resize_keyboard=True)
    back.add(KeyboardButton("⬅️ Назад"))
    await message.answer(text, reply_markup=back)

@dp.message_handler(lambda message: message.text == "4️⃣ Отзывы")
async def reviews(message: types.Message):
    await message.answer("Ссылка на отзывы: https://t.me/mefik_otzv")

# Callback для inline кнопок
@dp.callback_query_handler()
async def callbacks(call: types.CallbackQuery):
    data = call.data
    if data in bot_info:
        await call.message.edit_text(
            f"{bot_info[data]['description']}",
            reply_markup=bot_info_menu
        )
    elif data == "bot_info":
        await call.message.answer("Детальная информация о выбранном боте.")
    elif data == "bot_price":
        await call.message.answer("Цена бота указана ниже на кнопках.")
    elif data == "bot_order":
        await call.message.answer("Для заказа напишите разработчику @mefik_out")

# Запуск бота
if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
