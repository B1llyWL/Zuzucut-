from aiogram import F, Router, types
from aiogram.types import Message, InputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

import logging, db
import admin_keyboard as akb
import keyboard as kb

# Настройка логирования
logging.basicConfig(level=logging.INFO)

router = Router()

@router.message(Command('start'))
async def cmd_start(message: Message, state: FSMContext):
    admin_id = db.get_admin_id()
    if message.from_user.id == admin_id:
        await state.clear()
        await message.answer("🔹 Добро пожаловать в админ-панель!", reply_markup=akb.admin_menu)
        return
    await message.answer(
        "Привет! Рада тебя видеть! 😊 Я занимаюсь созданием уникальных артов и скетчей. "
        "Если у тебя есть идея, могу помочь её реализовать. О чем ты думаешь?",
        reply_markup=kb.main
    )

@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('Напиши что-нибудь и это автоматически перешлется Зузу.')

@router.message(Command('contact'))
async def cmd_contact(message: Message):
    await message.answer('Художница🖌️- @Enotkruty, создатель бота 💻- @Billy_W')

@router.message(Command('bot'))
async def cmd_bot(message: Message):
    await message.answer(
        "🤖 <b>Информация о боте</b>\n\n"
        "Этот бот работает на бесплатном хостинге. \n"
        "⚠️ <b>Важно:</b> В редких случаях возможны технические задержки или временные недоступности сервиса.\n\n"
        "Если бот не отвечает:\n"
        "1. Подождите минуту.\n"
        "2. Отправьте команду /start или нажмите на кнопку еще раз.\n\n"
        "🛡️ <b>Защита от спама:</b>\n"
        "Чтобы бот работал стабильно для всех, включена защита от перегрузок.\n"
        "Пожалуйста, не отправляйте слишком много сообщений подряд (лимит: 20 сообщений в минуту).\n\n"
        "Спасибо за понимание! ❤️\n\n"
        "Исходный код: https://github.com/B1llyWL/Zuzucut",
        parse_mode = 'HTML'
        )

@router.message(F.text == 'Как можно заказать арт?')
async def order_art(message: Message):
    await message.answer('Заказать очень просто! Через команду /register')

@router.message(F.text == 'Оплата')
async def payment(message: Message):
    await message.answer('Оплата происходит исключительно в рублях и в Сбербанк.')

@router.message(F.text == 'Цена')
async def price(message: Message):
    prices_text = db.get_prices()
    await message.answer(prices_text)

@router.message(F.text == 'Примеры работ')
async def example_arts(message: Message):
    await message.answer('Конечно! У меня есть портфолио с последними проектами. Если тебе нужно что-то конкретное, дай знать — я помогу найти примеры, которые могут тебя вдохновить. Tgc: https://t.me/Zuzucut')

@router.message(F.text == 'Срок')
async def term_of_work(message: Message):
    await message.answer('Обычно это занимает от 2 недель до месяца, в зависимости от сложности. После того как обсудим детали, я смогу сказать более точно. А у тебя есть конкретные сроки на примете?')

@router.message(F.text == 'Отзывы от клиентов')
async def customer_reviews(message: Message):
    await message.answer('Да, конечно! Я собираю отзывы от клиентов. Если интересно, можешь почитать тут https://t.me/Zuzucut, что люди говорят о моей работе. Если у тебя есть еще вопросы, всегда рада помочь!')
