from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import db, re
import admin_keyboard as akb
from middlewares import AdminCheckMiddleware

template_router = Router()

# MIDDLEWARE
template_router.message.middleware(AdminCheckMiddleware())
template_router.callback_query.middleware(AdminCheckMiddleware())


class TemplateStates(StatesGroup):
    creating_title = State()
    creating_text = State()
    sending_var = State()
    sending_client_id = State()


@template_router.message(Command('templates'))
async def templates_menu(message: Message, bot: Bot):
    """Показать меню шаблонов"""
    await message.answer("📝 Управление шаблонами:", reply_markup=akb.templates_menu)


@template_router.message(F.text == '➕ Создать шаблон')
async def create_template_start(message: Message, state: FSMContext, bot: Bot):
    """Начать создание шаблона"""
    await state.set_state(TemplateStates.creating_title)
    await message.answer("Введите название шаблона (например: 'Приветствие'):")


@template_router.message(TemplateStates.creating_title)
async def create_template_title(message: Message, state: FSMContext):
    """Сохранить название шаблона"""
    await state.update_data(title=message.text)
    await state.set_state(TemplateStates.creating_text)
    await message.answer(
        "Теперь введите текст шаблона.\n\n"
        "Используйте {{ имя_переменной }} для переменных.\n"
        "Пример: Здравствуй, {{ name }}! Вот ваш заказ."
    )


@template_router.message(TemplateStates.creating_text)
async def create_template_text(message: Message, state: FSMContext):
    """Сохранить текст шаблона"""
    data = await state.get_data()
    templates = db.get_templates()
    key = f"tpl_{len(templates) + 1}"
    templates[key] = {
        'title': data['title'],
        'text': message.text
    }
    db.save_templates(templates)
    await message.answer(f"✅ Шаблон '{data['title']}' сохранён!")
    await state.clear()


@template_router.message(F.text == '📤 Отправить шаблон')
async def send_template_start(message: Message, state: FSMContext, bot: Bot):
    """Начать отправку шаблона"""
    templates = db.get_templates()
    if not templates:
        await message.answer("Шаблонов пока нет. Сначала создайте один.")
        return
    await state.set_state(TemplateStates.sending_var)
    await message.answer("Выберите шаблон:", reply_markup=akb.get_templates_inline_keyboard())


@template_router.message(F.text == '🗑️ Удалить шаблон')
async def delete_template_start(message: Message, state: FSMContext, bot: Bot):
    """Выбор шаблона для удаления"""
    templates = db.get_templates()
    if not templates:
        await message.answer("Шаблонов пока нет.")
        return
    await message.answer("Выберите шаблон для удаления:", reply_markup=akb.get_templates_delete_keyboard())


@template_router.callback_query(F.data.startswith('del_'))
async def process_delete_callback(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """Обработка удаления шаблона"""
    data = callback.data

    # Отмена на любом шаге
    if data == 'del_cancel':
        await callback.message.edit_text("❌ Удаление отменено.")
        await callback.answer()
        return

    # Подтверждённое удаление
    if data.startswith('del_confirm_'):
        key = data.removeprefix('del_confirm_')
        templates = db.get_templates()
        if key not in templates:
            await callback.answer("❌ Шаблон не найден", show_alert=True)
            return
        title = templates[key]['title']
        del templates[key]
        db.save_templates(templates)
        await callback.message.edit_text(f"🗑️ Шаблон «{title}» удалён.")
        await callback.answer()
        return

    # Первый шаг — показать подтверждение
    key = data.removeprefix('del_')
    templates = db.get_templates()
    if key not in templates:
        await callback.answer("❌ Шаблон не найден", show_alert=True)
        return
    title = templates[key]['title']
    await callback.message.edit_text(
        f"❓ Вы уверены, что хотите удалить «{title}»?",
        reply_markup=akb.get_delete_confirm_keyboard(key)
    )
    await callback.answer()


@template_router.callback_query(F.data.startswith('tpl_'))
async def process_template_callback(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """Обработка выбора шаблона"""
    if callback.data == 'tpl_cancel':
        await callback.message.edit_text("❌ Отменено.")
        await state.clear()
        await callback.answer()
        return

    key = callback.data
    templates = db.get_templates()

    if key not in templates:
        await callback.answer("❌ Шаблон не найден", show_alert=True)
        return

    tpl = templates[key]
    variables = re.findall(r'\{\{\s*(\w+)\s*\}\}', tpl['text'])

    await state.update_data(
        tpl_key=key,
        tpl_title=tpl['title'],
        tpl_text=tpl['text'],
        variables=variables
    )

    if variables:
        await state.set_state(TemplateStates.sending_var)
        await callback.message.edit_text(
            f"📤 {tpl['title']}\n\n"
            f"Введите значение для переменной '{variables[0]}':"
        )
    else:
        await state.set_state(TemplateStates.sending_client_id)
        await callback.message.edit_text(
            f"📤 {tpl['title']}\n\n"
            f"Введите ID клиента для отправки:"
        )

    await callback.answer()


@template_router.message(TemplateStates.sending_var)
async def process_template_var(message: Message, state: FSMContext):
    """Обработка значения переменной"""
    data = await state.get_data()
    variables = data.get('variables', [])
    current_var = variables[0]

    pattern = r'\{\{\s*' + re.escape(current_var) + r'\s*\}\}'
    new_text = re.sub(pattern, message.text, data['tpl_text'])

    remaining_vars = variables[1:]
    await state.update_data(tpl_text=new_text, variables=remaining_vars)

    if remaining_vars:
        await message.answer(f"Принято. Введите значение для '{remaining_vars[0]}':")
    else:
        await state.set_state(TemplateStates.sending_client_id)
        await message.answer("✅ Отлично! Теперь введите ID клиента:")


@template_router.message(TemplateStates.sending_client_id)
async def send_template_to_client(message: Message, state: FSMContext, bot: Bot):
    """Отправка шаблона клиенту"""
    try:
        client_id = int(message.text)
        data = await state.get_data()
        await bot.send_message(client_id, data['tpl_text'])
        await message.answer(f"✅ Шаблон '{data['tpl_title']}' отправлен клиенту {client_id}!")
        await state.clear()
    except ValueError:
        await message.answer("❌ ID должен быть числом. Попробуйте ещё раз.")