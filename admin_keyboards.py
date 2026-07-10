from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                            InlineKeyboardMarkup, InlineKeyboardButton)
from keyboard import client_menu
import db

#админ-меню
admin_menu = ReplyKeyboardMarkup(keyboard=[
  [KeyboardButton(text='📝 Шаблоны'),
   KeyboardButton(text='📊 Статистика')],
  [KeyboardButton(text='👤 Сменить админа'),KeyboardButton(text='💰 Изменить цены')],
  [KeyboardButton(text='📬 Клиентское меню')] #Для справки
],
  resize_keyboard=True,
  input_field_placeholder="Выберите пункт меню...")

#меню шаблонов
templates_menu = ReplyKeyboardMarkup(keyboard=[
  [KeyboardButton(text='➕ Создать шаблон')],
  [KeyboardButton(text='📤 Отправить шаблон')],
  [KeyboardButton(text='🗑️ Удалить шаблон')],
  [KeyboardButton(text='⬅️ Назад в админ-меню')]
], resize_keyboard=True)

def get_templates_inline_keyboard():
    '''Создает клавиатуру с шаблонами для отправки клиентам'''
    templates = db.get_templates()
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for key, tpl in templates.items():
        keyboard.inline_keyboard.append([
          InlineKeyboardButton(text=tpl['title'], callback_data=key)
        ])
    keyboard.inline_keyboard.append([
      InlineKeyboardButton(text="❌ Отмена", callback_data="tpl_cancel")
    ])
    return keyboard

def get_templates_delete_keyboard():
    '''Клавиатура выбора шаблона для удаления'''
    templates = db.get_templates()
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for key, tpl in templates.items():
        keyboard.inline_keyboard.append([
          InlineKeyboardButton(text=tpl['title'], callback_data=f"del_{key}")
        ])
    keyboard.inline_keyboard.append([
      InlineKeyboardButton(text="❌ Отмена", callback_data="del_cancel")
    ])
    return keyboard

def get_delete_confirm_keyboard(key: str):
    '''Клавиатура подтверждения удаления'''
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Да, удалить", callback_data=f"del_confirm_{key}"),
            InlineKeyboardButton(text="❌ Отмена",      callback_data="del_cancel"),
        ]
    ])
