from aiogram import F, Router, Bot
from aiogram.types import Message
from aiogram.filters import Command
import db, re

admin_router = Router()


@admin_router.message(Command('set_admin'))
async def set_admin_cmd(message: Message, bot: Bot):
    """Команда /set_admin <telegram_id> — смена администратора"""
    current_admin = db.get_admin_id()
    if current_admin != message.from_user.id:
        await message.answer("⛔ У вас нет прав.")
        return
    args = message.text.split()
    if len(args) != 2:
        await message.answer("Используйте: /set_admin <telegram_id>")
        return
    try:
        new_id = int(args[1])
        db.set_admin_id(new_id)
        await message.answer(f"✅ Администратор изменён на {new_id}")
    except ValueError:
        await message.answer("ID должен быть числом.")


@admin_router.message(F.text & ~F.text.startswith('/'))
async def handle_text_from_client(message: Message, bot: Bot):
    """Пересылает текстовые сообщения от клиентов админу"""

    # === ДИАГНОСТИКА ===
    print(f"📨 [ADMIN HANDLER] Получено сообщение!")
    print(f"   От: {message.from_user.id} ({message.from_user.full_name})")
    print(f"   Текст: {message.text}")

    # Игнор текстовых команд(кнопок из меню)
    menu = {
        'Цена',
        'Срок',
        'Оплата',
        'Примеры работ',
        'Отзывы от клиентов',
        'Как можно заказать арт?',
    }

    if message.text in menu:
        print(f"   ❌ Это команда меню - пропускаем")
        return

    admin_id = db.get_admin_id()

    print(f"   👤 Admin ID из БД: {admin_id}")
    print(f"   🔍 Тип admin_id: {type(admin_id)}")

    if message.from_user.id == admin_id:
        print(f"   ⚠️ Сообщение от самого админа - игнорируем")
        return

    if not admin_id or admin_id == 0:
        print(f"   ❌ Администратор не назначен!")
        await message.answer("Администратор ещё не назначен. Попробуйте позже.")
        return

    try:
        print(f"   📤 Отправляем сообщение админу {admin_id}...")
        await bot.send_message(admin_id, f"От {message.from_user.id}:\n{message.text}")
        print(f"   ✅ Сообщение успешно отправлено!")
    except Exception as e:
        print(f"   ❌ ОШИБКА отправки: {e}")
        print(f"   ❌ Тип ошибки: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        await message.answer("⚠️ Не удалось отправить сообщение админу.")
        return

    await message.answer("✅ Ваше сообщение отправлено Зузу!")

@admin_router.message(F.photo)
async def handle_photo_from_client(message: Message, bot: Bot):
    """Пересылает фото от клиентов админу"""
    admin_id = db.get_admin_id()
    if message.from_user.id == admin_id:
        return
    if not admin_id or admin_id == 0:
        await message.answer("Администратор ещё не назначен.")
        return
    caption = f"Фото от {message.from_user.id}"
    if message.caption:
        caption += f"\n{message.caption}"
    await bot.send_photo(admin_id, message.photo[-1].file_id, caption=caption)
    await message.answer("✅ Ваше фото отправлено Зузу!")


@admin_router.message(F.reply_to_message)
async def admin_reply_to_client(message: Message, bot: Bot):
    """Ответ админа клиенту через reply"""
    admin_id = db.get_admin_id()
    if message.from_user.id != admin_id:
        return

    replied_text = message.reply_to_message.text or message.reply_to_message.caption or ""
    if not replied_text.startswith("От"):
        await message.answer("Ответьте на сообщение, которое я прислал вам от клиента.")
        return

    match = re.search(r"От\s+(\d+)", replied_text)
    if not match:
        await message.answer("Не удалось найти ID клиента в этом сообщении.")
        return
    client_id = int(match.group(1))

    if message.text:
        await bot.send_message(client_id, f"✉️ Ответ Зузу:\n{message.text}")
    elif message.photo:
        cap = f"✉️ Ответ Зузу:\n{message.caption or ''}"
        await bot.send_photo(client_id, message.photo[-1].file_id, caption=cap)
    else:
        await message.answer("Я могу переслать только текст или фото.")
        return
    await message.reply("✅ Ответ отправлен клиенту!")

