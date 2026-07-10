from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
import spam_protection as sp


class SpamProtectionMiddleware(BaseMiddleware):
    """Middleware для защиты от спама"""

    async def __call__(self, handler, event, data):
        # Пропускаем callback-запросы без проверки
        if isinstance(event, CallbackQuery):
            return await handler(event, data)

        user_id = event.from_user.id

        # Админ никогда не блокируется
        import db as _db
        if user_id == _db.get_admin_id():
            return await handler(event, data)

        if sp.is_spamming(user_id):
            block_time = sp.get_block_time(user_id)
            await event.answer(f"⚠️ Вы заблокированы на {block_time} секунд за большое количество сообщений.")
            return

        return await handler(event, data)
