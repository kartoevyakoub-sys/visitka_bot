import os
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, Update, InlineKeyboardMarkup
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Токен будем прятать в настройках Vercel, чтобы не светить в коде
BOT_TOKEN = ("9037503874:AAGKKDmWb4jO3hj4bDFJKI4s6ZOeXIzr5N4")
MY_USERNAME = "aeeeqk"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
app = FastAPI()

def get_main_menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="💻 Разработка (Боты / Сайты)", callback_data="show_dev")
    kb.button(text="🛠 Помощь с ПК (Удаленно)", callback_data="show_pc")
    kb.button(text="🎨 Графический дизайн", callback_data="show_design")
    kb.button(text="👤 Мои работы и Отзывы", url="https://t.me/+4HX3Qi92GnAyNTM6") 
    kb.button(text="💬 Написать мне лично", url=f"https://t.me/{MY_USERNAME}")
    return kb.adjust(1, 1, 1, 2).as_markup()

def get_service_menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="💬 Обсудить задачу", url=f"https://t.me/{MY_USERNAME}")
    kb.button(text="🔙 Назад в меню", callback_data="back_to_main")
    return kb.adjust(1).as_markup()

@dp.message(CommandStart())
async def start(message: Message):
    text = (
        "Привет! Я Павел — частный IT-специалист и разработчик.\n\n"
        "Выполняю задачи быстро, работаю на результат. Выберите интересующее направление ниже, "
        "чтобы узнать подробности, или сразу пишите мне в личные сообщения."
    )
    await message.answer(text, reply_markup=get_main_menu())

@dp.callback_query(F.data == "back_to_main")
async def back_to_main(call: CallbackQuery):
    await call.message.edit_text("Выберите интересующее направление:", reply_markup=get_main_menu())

@dp.callback_query(F.data == "show_dev")
async def show_dev(call: CallbackQuery):
    text = (
        "<b>💻 Программирование и Разработка</b>\n\n"
        "• Создание Telegram-ботов (aiogram, интеграция API, базы данных).\n"
        "• Разработка лендингов и сайтов-визиток под ключ.\n"
        "• Скрипты автоматизации и парсинг данных (Python).\n\n"
        "<i>Нажмите кнопку ниже, чтобы перейти в диалог.</i>"
    )
    await call.message.edit_text(text, parse_mode="HTML", reply_markup=get_service_menu())

@dp.callback_query(F.data == "show_pc")
async def show_pc(call: CallbackQuery):
    text = (
        "<b>🛠 Удаленная помощь с ПК</b>\n\n"
        "• Удаленная настройка и решение проблем через AnyDesk / RuDesk.\n"
        "• Установка и оптимизация Windows, драйверов и программ.\n"
        "• Чистка системы от вирусов и ускорение работы.\n\n"
        "<i>Готов подключиться прямо сейчас. Жмите кнопку для связи.</i>"
    )
    await call.message.edit_text(text, parse_mode="HTML", reply_markup=get_service_menu())

@dp.callback_query(F.data == "show_design")
async def show_design(call: CallbackQuery):
    text = (
        "<b>🎨 Графический дизайн</b>\n\n"
        "• Создание логотипов и фирменного стиля.\n"
        "• Оформление рекламных баннеров и соцсетей.\n"
        "• Дизайн карточек для маркетплейсов и визиток.\n\n"
        "<i>Работаю в Photoshop. Напишите мне, чтобы обсудить визуал.</i>"
    )
    await call.message.edit_text(text, parse_mode="HTML", reply_markup=get_service_menu())

# --- ТОЧКА ВХОДА ДЛЯ VERCEL ---
@app.post("/webhook")
async def webhook_handler(request: Request):
    update_data = await request.json()
    update = Update(**update_data)
    await dp.feed_update(bot, update)
    return {"status": "ok"}
