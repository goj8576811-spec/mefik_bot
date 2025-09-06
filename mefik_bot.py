import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

# Загружаем токен из переменных окружения (Render → Environment Variables)
TOKEN = os.getenv("8374373060:AAEtM7aXDDH8Q77F8xk44L3bEyXqNh-ySz8")

# Настройки вебхука
WEBHOOK_HOST = os.getenv("RENDER_EXTERNAL_URL")  # Render сам подставит URL
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Кнопки
main_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📌 Услуги", callback_data="services")],
    [InlineKeyboardButton(text="💬 Связаться", url="https://t.me/mefik_otzv")],
])

services_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🤖 Разработка бота", callback_data="bot_dev")],
    [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")]
])


@dp.message(F.text == "/start")
async def start_cmd(message: Message):
    await message.answer(
        "👋 Приветствуем!\n\n"
        "Мы предоставляем полный спектр услуг по разработке Telegram-ботов: "
        "от концепции до внедрения и поддержки.\n\n"
        "Наши решения позволяют автоматизировать бизнес-процессы, улучшить коммуникацию "
        "с клиентами и увеличить эффективность работы команды.\n\n"
        "Свяжитесь с разработчиком для консультации или заказа индивидуального проекта.",
        reply_markup=main_kb
    )


@dp.callback_query(F.data == "services")
async def show_services(callback):
    await callback.message.edit_text(
        "📌 Выберите услугу:", reply_markup=services_kb
    )


@dp.callback_query(F.data == "bot_dev")
async def bot_dev(callback):
    await callback.message.edit_text(
        "🤖 Мы создаём Telegram-ботов под любые задачи!\n\n"
        "📌 Автоматизация бизнеса\n"
        "📌 Приём заказов\n"
        "📌 Чаты, игры и многое другое\n\n"
        "Нажмите «Связаться» чтобы обсудить детали.",
        reply_markup=services_kb
    )


@dp.callback_query(F.data == "back")
async def go_back(callback):
    await callback.message.edit_text(
        "Главное меню:", reply_markup=main_kb
    )


async def on_startup(app: web.Application):
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(app: web.Application):
    await bot.delete_webhook()


def main():
    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    web.run_app(app, port=int(os.getenv("PORT", 8080)))


if __name__ == "__main__":
    main()
