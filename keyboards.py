from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

convert = KeyboardButton('Convert')
main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).row(convert)


finish = KeyboardButton('Get PDF')
finish_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).row(finish)
