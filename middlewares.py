from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
import db
import admin_text as at

class AdminCheckMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if isinstance(event, (Message, CallbackQuery)):
            user_id = event.from_user.id
        else:
            return await handler(event, data)

        admin_id = db.get_admin_id()
        if user_id != admin_id:
            if isinstance(event, Message):
                await event.answer(at.ADMIN_NO_PERMISSIONS)
            elif isinstance(event, CallbackQuery):
                await event.answer(at.ADMIN_NO_PERMISSIONS, show_alert=True)
            return
        return await handler(event, data)

class BanCheckMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if isinstance(event, (Message, CallbackQuery)):
            user_id = event.from_user.id
        else:
            return await handler(event, data)

        # Адм не блокируем
        if user_id == db.get_admin_id():
            return await handler(event, data)

        if db.is_banned(user_id):
            if isinstance(event, Message):
                await event.answer("⛔ Вы заблокированы в этом боте.")
            elif isinstance(event, CallbackQuery):
                await event.answer("⛔ Вы заблокированы.", show_alert=True)
            return
        return await handler(event, data)