from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import db

register_router = Router()

class Register(StatesGroup):
  name = State()
  username = State()
  type_art = State()
  background_art = State()
  term_of_work = State()
  additional_factors_art = State()
  your_comments = State()
  reference_images = State()

@register_router.message(Command('register'))
async def register(message: Message, state: FSMContext):
    await state.set_state(Register.name)
    await message.answer('1. Введи свое имя.')

@register_router.message(Register.name)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Register.username)
    await message.answer('2. Введи свой юзернейм, чтобы Зузу скинула вам работу, когда она будет готова.')

@register_router.message(Register.username)
async def register_username(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await state.set_state(Register.type_art)
    await message.answer('3. Полноценная работа/Скетч(набросок)?')

@register_router.message(Register.type_art)
async def register_type_art(message: Message, state: FSMContext):
    await state.update_data(type_art=message.text)
    await state.set_state(Register.background_art)
    await message.answer('4. Фон:\n 0. без фона\n 1. с простой заливкой\n 2. без сильной проработанности/рендеринга\n 3. коллаж')

@register_router.message(Register.background_art)
async def register_background_art(message: Message, state: FSMContext):
    await state.update_data(background_art=message.text)
    await state.set_state(Register.term_of_work)
    await message.answer('5. Срок: (+30% за срочность; дедлайн: от 2 недель до месяца)')

@register_router.message(Register.term_of_work)
async def register_term_of_work(message: Message, state: FSMContext):
    await state.update_data(term_of_work=message.text)
    await state.set_state(Register.additional_factors_art)
    await message.answer('6. Дополнительные факторы:\n 0. отсутствуют/добавлю в свои комментарии\n 1. второй персонаж\n 2. излишняя детализация\n 3. сложный ракурс')

@register_router.message(Register.additional_factors_art)
async def register_additional_factors_art(message: Message, state: FSMContext):
    await state.update_data(additional_factors_art=message.text)
    await state.set_state(Register.your_comments)
    await message.answer('7. Свои комментарии.')

@register_router.message(Register.your_comments)
async def register_your_comments(message: Message, state: FSMContext):
    await state.update_data(your_comments=message.text)
    await state.set_state(Register.reference_images)
    await message.answer(
        '8. 📎 Прикрепи референсы (фото/картинки), если есть.\n\n'
        'Можешь отправить несколько фото.\n'
        'Когда закончишь — напиши "Готово" или "Пропустить", если референсов нет.'
    )

# Хэндлер для обработки фото
@register_router.message(Register.reference_images, F.photo)
async def register_reference_image(message: Message, state: FSMContext):
    data = await state.get_data()
    images = data.get('reference_images', [])

    photo = message.photo[-1]
    images.append(photo.file_id)

    await state.update_data(reference_images=images)

    await message.answer(
        f'✅ Фото сохранено! (всего: {len(images)})\n\n'
        'Отправь ещё фото или напиши "Готово", когда закончишь.'
    )

@register_router.message(Register.reference_images, F.text.lower().in_(['готово', 'пропустить', 'skip', 'done']))
async def register_reference_done(message: Message, state: FSMContext):
    data = await state.get_data()
    images = data.get('reference_images', [])

    response = f'📌\n'
    response += f'Имя: {data["name"]}\n'
    response += f'Юзернейм: {data["username"]}\n'
    response += f'Тип: {data["type_art"]}\n'
    response += f'Фон: {data["background_art"]}\n'
    response += f'Cрок: {data["term_of_work"]}\n'
    response += f'Дополнительные факторы: {data["additional_factors_art"]}\n'
    response += f'Свои комментарии: {data["your_comments"]}\n'

    if images:
        response += f'📎 Референсы: {len(images)} фото'
    else:
        response += '📎 Референсы: нет'

    await message.answer(response)
    # Отправка анкетки админчику
    admin_id = db.get_admin_id()
    if admin_id:
        try:
            await message.bot.send_message(admin_id, f"🆕 Новая заявка!\n\n{response}")

            # Если есть референсы, отправляем их админу
            if images:
                await message.answer('📸 Референсы отправлены.')
                for img_id in images:
                    await message.bot.send_photo(admin_id, img_id, caption=f"Референс от {data['username']}")
        except Exception as e:
            print(f"❌ Ошибка отправки админу: {e}")

    await state.clear()

# Хэндлер для обработки текста в состоянии reference_images
@register_router.message(Register.reference_images, F.text)
async def register_reference_invalid(message: Message):
    await message.answer(
        '📎 Пожалуйста, отправь фото или напиши "Готово" / "Пропустить"'
    )