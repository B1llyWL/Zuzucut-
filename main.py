import asyncio, os, db
from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat
from config import TOKEN

os.environ['http_proxy'] = 'http://proxy.server:3128'
os.environ['https_proxy'] = 'http://proxy.server:3128'

async def set_commands():
    """Установить меню команд для клиентов и администратора."""
    if not TOKEN:
        print("❌ Токен не установлен! Проверьте переменную BOT_TOKEN.")
        return

    proxy = os.getenv('https_proxy')
    session = AiohttpSession(proxy=proxy) if proxy else AiohttpSession()
    bot = Bot(token=TOKEN, session=session)
    try:

        client_commands = [
            BotCommand(command="start",    description="Старт"),
            BotCommand(command="register", description="Заказать"),
            BotCommand(command="help",     description="Помощь"),
            BotCommand(command="contact",  description="Контакты"),
            BotCommand(command="bot",  description="О боте"),
        ]
        await bot.set_my_commands(client_commands, scope=BotCommandScopeDefault())

        admin_id = db.get_admin_id()
        if admin_id:
            admin_commands = [
                BotCommand(command="start",     description="Старт"),
                BotCommand(command="admin",     description="Подсказка по панели"),
                BotCommand(command="set_admin", description="Сменить админа"),
                BotCommand(command="templates", description="Меню шаблонов"),
                BotCommand(command="form",      description="Как выглядит анкета клиента"),
                BotCommand(command="unblock",   description="Разблокировать пользователя"),
                BotCommand(command="info",      description="Напоминалка о боте"),
            ]
            await bot.set_my_commands(
                admin_commands,
                scope=BotCommandScopeChat(chat_id=admin_id)
            )
            print(f"✅ Команды для администратора {admin_id} установлены")
        else:
            print("⚠️ Администратор не найден в БД, установлены только общие команды.")
        print("✅ Команды успешно установлены.")
    except Exception as e:
        print(f"❌ Ошибка установки команд: {e}")
    finally:
        await session.close()

if __name__ == '__main__':
    print("Инициализация БД...")
    db.init_db()
    print("Установка команд бота...")
    asyncio.run(set_commands())
    print("Готово. Бот работает через вебхук.")