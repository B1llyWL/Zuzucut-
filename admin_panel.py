from aiogram import F, Router, Bot
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import db, sqlite3
import admin_keyboard as akb
import admin_text as at
import spam_protection as sp
from middlewares import AdminCheckMiddleware

admin_panel_router = Router()

# MIDDLEWARE
admin_panel_router.message.middleware(AdminCheckMiddleware())
admin_panel_router.callback_query.middleware(AdminCheckMiddleware())


class AdminStates(StatesGroup):
    waiting_new_admin_id = State()
    waiting_new_prices_text = State()


@admin_panel_router.message(Command('admin'))
async def show_admin_help(message: Message):
    """Показать подсказку"""
    await message.answer(at.ADMIN_HELP, reply_markup=akb.admin_menu, parse_mode="Markdown")


@admin_panel_router.message(Command('form'))
async def show_form_info(message: Message):
    """Показать структуру анкеты клиента"""
    await message.answer(at.ADMIN_FORM_INFO, reply_markup=akb.admin_menu, parse_mode="Markdown")


@admin_panel_router.message(Command('start'))
async def start_cmd(message: Message):
    """Приветствие для админа"""
    await message.answer(at.ADMIN_WELCOME, reply_markup=akb.admin_menu)

@admin_panel_router.message(F.text == '📬 Клиентское меню')
async def show_client_menu(message: Message):
    """Показать клиентское меню"""
    await message.answer(at.ADMIN_CLIENT_MENU_INFO, reply_markup=akb.client_menu, parse_mode='Markdown')


@admin_panel_router.message(F.text == '📝 Шаблоны')
async def templates_menu(message: Message):
    """Меню шаблонов"""
    await message.answer("📝 Управление шаблонами:", reply_markup=akb.templates_menu)


@admin_panel_router.message(F.text == '📊 Статистика')
async def show_stats(message: Message):
    """Показать статистику"""
    try:
        conn = sqlite3.connect(db.DB_PATH)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM clients")
        count = c.fetchone()[0]
        conn.close()
    except:
        count = 0

    await message.answer(
        at.ADMIN_STATS.format(count=count, admin_id=db.get_admin_id()),
        parse_mode='Markdown',
        reply_markup=akb.admin_menu
    )


@admin_panel_router.message(F.text == '👤 Сменить админа')
async def change_admin(message: Message, state: FSMContext):
    """Смена администратора"""
    await state.set_state(AdminStates.waiting_new_admin_id)
    await message.answer(at.ADMIN_TRANSFER_START, parse_mode='Markdown')


@admin_panel_router.message(AdminStates.waiting_new_admin_id)
async def process_new_admin(message: Message, state: FSMContext, bot: Bot):
    """Обработка нового ID администратора"""
    try:
        new_id = int(message.text)
        db.set_admin_id(new_id)
        await message.answer(
            at.ADMIN_TRANSFER_SUCCESS.format(new_id=new_id),
            parse_mode='Markdown'
        )
        try:
            await bot.send_message(new_id, at.ADMIN_TRANSFER_NOTIFY)
        except Exception as e:
            print(f"❌ Ошибка отправки уведомления новому админу: {e}")
        await state.clear()
    except ValueError:
        await message.answer(at.ADMIN_INVALID_ID)


@admin_panel_router.message(F.text == '⬅️ Назад в админ-меню')
async def back_to_admin_menu(message: Message):
    """Возврат в админ-меню"""
    await message.answer("🔧 Админ-панель:", reply_markup=akb.admin_menu)


@admin_panel_router.message(Command('set_admin'))
async def set_admin_cmd(message: Message):
    """Команда /set_admin <telegram_id>"""
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

@admin_panel_router.message(Command('unblock'))
async def unblock_user_cmd(message: Message):
    """Команда /unblock <telegram_id>"""
    args = message.text.split()
    if len(args) != 2:
        await message.answer("Используйте: /unblock <telegram_id>")
        return
    try:
        user_id = int(args[1])
        sp.unblock_user(user_id)
        await message.answer(f"✅ Пользователь {user_id} разблокирован.")
    except ValueError:
        await message.answer("ID должен быть числом.")

@admin_panel_router.message(Command('info'))
async def info_cmd(message: Message):
    """Команда-напоминалка"""
    await message.answer(
    "Бота необходимо перезапускать 1 раз в месяц. Таковы условия бесплатного тарифа.\n"
    "Чтобы перезапустить бота зайди на сервер, кликни на вкладку <<Web>> и нажми на зеленую кнопку <<Reload Zuzucut.pythonanywhere.com>>",
    reply_markup=akb.admin_menu, parse_mode="Markdown"
    )

@admin_panel_router.message(F.text == '💰 Изменить цены')
async def change_prices(message: Message, state: FSMContext):
    """Изменение цен"""
    await state.set_state(AdminStates.waiting_new_prices_text)
    current_prices = db.get_prices()
    cancel_kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=at.ADMIN_PRICES_CANCEL_BUTTON)]],
        resize_keyboard=True
    )
    await message.answer(
        at.ADMIN_PRICES_START + f"\n\n📋 **Текущие цены:**\n\n{current_prices}",
        parse_mode='Markdown',
        reply_markup=cancel_kb
    )


@admin_panel_router.message(AdminStates.waiting_new_prices_text, F.text == at.ADMIN_PRICES_CANCEL_BUTTON)
async def change_prices_cancel(message: Message, state: FSMContext):
    """Отмена изменения цен"""
    await state.clear()
    await message.answer(at.ADMIN_PRICES_CANCEL, reply_markup=akb.admin_menu)


@admin_panel_router.message(AdminStates.waiting_new_prices_text)
async def process_new_prices(message: Message, state: FSMContext):
    """Обработка нового текста цен"""
    new_prices = message.text
    db.set_prices(new_prices)
    await state.clear()
    await message.answer(
        at.ADMIN_PRICES_SUCCESS + f"\n\n📋 **Новые цены:**\n\n{new_prices}",
        parse_mode='Markdown',
        reply_markup=akb.admin_menu
    )
