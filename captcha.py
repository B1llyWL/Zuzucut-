import random, db
from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command, Filter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import keyboard as kb

captcha_router = Router()

class CaptchaStates(StatesGroup):
    waiting_answer = State()

#Хранилище решенных капч
solved_captchas = set()

class IsNotAdmin(Filter):
    """Пропускает только не-админов"""
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id != db.get_admin_id()

def generate_captcha():
  """Генерирует простую математическую капчу"""
  a, b = random.randint(1, 10), random.randint(1, 10)
  return f"{a}+{b}=?", a+b

@captcha_router.message(Command('start'), IsNotAdmin())
async def start(message: Message, state: FSMContext):
  if message.from_user.id in solved_captchas:
    return
  question, answer = generate_captcha()
  await state.update_data(answer=answer)
  await state.set_state(CaptchaStates.waiting_answer)
  await message.answer(f"Решите капчу: {question}")

@captcha_router.message(CaptchaStates.waiting_answer)
async def check_captcha(message: Message, state: FSMContext):
  try:
    user_answer = int(message.text)
    data = await state.get_data()
    correct_answer = data.get('answer')

    if user_answer == correct_answer:
      solved_captchas.add(message.from_user.id)
      await state.clear()

      db.save_client(message.from_user.id, message.from_user.username or  '', message.from_user.first_name or '')

      await message.answer("Капча решена! Добро пожаловать!",reply_markup=kb.client_menu)
    else:
      await message.answer("Неверно. Попробуйте ещё раз.")
  except ValueError:
     await message.answer("Пожалуйста, введите число.")
