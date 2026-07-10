import os, sys, hashlib, db
from flask import Flask, request
from aiogram import types, Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.session.aiohttp import AiohttpSession as _AiohttpSession
from middlewares import BanCheckMiddleware
from spam_middleware import SpamProtectionMiddleware
from config import TOKEN
import asyncio

db.init_db()

from captcha import captcha_router
from handlers import router
from register import register_router
from admin_panel import admin_panel_router
from templates_handlers import template_router
from client_forward import client_forward_router

# Создаём глобальный цикл событий
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# MIDDLEWARE
dp.message.middleware(BanCheckMiddleware())
dp.message.middleware(SpamProtectionMiddleware())

# Подключаем роутеры (один раз)
dp.include_router(captcha_router)
dp.include_router(router)
dp.include_router(register_router)
dp.include_router(admin_panel_router)
dp.include_router(template_router)
dp.include_router(client_forward_router)

# Создаём бота с прокси (прокси задаётся в wsgi.py)
proxy = os.getenv('https_proxy')
session = _AiohttpSession(proxy=proxy) if proxy else _AiohttpSession()
bot = Bot(token=TOKEN, session=session)

app = Flask(__name__)
WEBHOOK_SECRET = hashlib.sha256(TOKEN.encode()).hexdigest()[:32] if TOKEN else ""

@app.route('/webhook', methods=['POST'])
def webhook():
    update = types.Update(**request.json)
    print(f"✅ ВЕБХУК РАБОТАЕТ. ID: {update.update_id}")
    if update.message:
        print(f"   Текст: {update.message.text}")
    elif update.callback_query:
        print(f"   Callback: {update.callback_query.data}")
    sys.stdout.flush()

    try:
        # Используем глобальный цикл для обработки обновления
        loop.run_until_complete(dp.feed_update(bot, update))
    except Exception as e:
        print(f"❌ Ошибка обработки: {e}")
        sys.stdout.flush()
    return "OK", 200

@app.route('/')
def index():
    return "Zuzucut is running!"