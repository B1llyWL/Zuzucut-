from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                            InlineKeyboardMarkup, InlineKeyboardButton)

client_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Как можно заказать арт?'),
                                      KeyboardButton(text='Оплата')],
                                     [KeyboardButton(text='Цена'),
                                      KeyboardButton(text='Примеры работ')],
                                     [KeyboardButton(text='Срок'),
                                      KeyboardButton(text='Отзывы от клиентов')]],
                            resize_keyboard=True,
                            input_field_placeholder="Выберите пункт меню...")
