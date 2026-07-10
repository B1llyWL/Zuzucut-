import random,db,logging
from aiogram import F, Router, types
from aiogram.types import Message
from aiogram.filters import Command, Filter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import keyboard as kb

captcha_router = Router()
logger = logging.getLogger(__name__)

class CaptchaStates(StatesGroup):
    waiting_answer = State()

# Хранилище решённых капч (в памяти)
solved_captchas = set()

class IsNotAdmin(Filter):
    """Пропускает только не-админов"""
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id != db.get_admin_id()

def generate_captcha():
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    return f"{a}+{b}=?", a + b

@captcha_router.message(Command('start'), IsNotAdmin())
async def start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    logger.info(f"Captcha start for user {user_id}")
    if user_id in solved_captchas:
        logger.info(f"User {user_id} already solved captcha, skipping")
        return
    question, answer = generate_captcha()
    await state.update_data(answer=answer)
    await state.set_state(CaptchaStates.waiting_answer)
    await message.answer(f"Решите капчу: {question}")
    logger.info(f"Sent captcha to user {user_id}: {question}")

@captcha_router.message(CaptchaStates.waiting_answer)
async def check_captcha(message: Message, state: FSMContext):
    user_id = message.from_user.id
    logger.info(f"Checking captcha answer from user {user_id}")
    try:
        user_answer = int(message.text)
        data = await state.get_data()
        correct_answer = data.get('answer')
        if user_answer == correct_answer:
            solved_captchas.add(user_id)
            await state.clear()
            try:
                db.save_client(user_id, message.from_user.username or '', message.from_user.first_name or '')
            except Exception as e:
                logger.error(f"Error saving client: {e}")
            await message.answer("Капча решена! Добро пожаловать!", reply_markup=kb.client_menu)
            logger.info(f"Captcha solved for user {user_id}")
        else:
            await message.answer("Неверно. Попробуйте ещё раз.")
    except ValueError:
        await message.answer("Пожалуйста, введите число.")
    except Exception as e:
        logger.error(f"Unexpected error in check_captcha: {e}")
        await message.answer("Произошла ошибка. Попробуйте позже.")
