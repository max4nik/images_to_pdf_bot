import re

from aiogram import Bot, Dispatcher, executor, types
import os

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from images_to_pdf import Converter
from helper import Helper
from states.filename_state import FilenameEnterState
from keyboards import main_keyboard, finish_keyboard

bot = Bot(token=os.environ.get('token'))
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

c = Converter
h = Helper

filename = ''
iterator = 0
is_images = False
isActive = False


@dp.message_handler(commands=['start'])
async def greeting(message: types.message.Message):
    await message.answer('Hello!\n I`ll help you with converting images to pdf! Send /convert or press Convert button '
                         'to start magic', reply_markup=main_keyboard)


@dp.message_handler(commands=['help'])
async def get_help(message: types.message.Message):
    await message.answer('Send /convert or press Convert button to convert your images to pdf')


@dp.message_handler(commands=['convert'])
async def convert_images_to_pdf(message: types.message.Message, state: FSMContext):
    await message.answer(
        'OK! At first I want you to type name for your file.', reply_markup=ReplyKeyboardRemove())
    await FilenameEnterState.first()


@dp.message_handler(text='Convert')
async def convert_images_to_pdf(message: types.message.Message, state: FSMContext):
    await message.answer(
        'OK! At first I want you to type name for your file.', reply_markup=ReplyKeyboardRemove())
    await FilenameEnterState.first()


@dp.message_handler(content_types=['photo'])
async def save_photos(message):
    global iterator
    global is_images

    iterator += 1
    if is_images is False:
        os.chdir('images')
        is_images = True
    await message.photo[-1].download(str(iterator) + '.jpg')
    print('saved ' + str(iterator) + '.jpg')
    os.chdir('..')
    is_images = False


@dp.message_handler(text='Get PDF')
async def send_pdf(message: types.message.Message):
    global filename
    global iterator
    global is_images
    if iterator == 0:
        await message.answer('You haven\'t sent any photos yet.\n\nRemember to send only photos, not files')
        return
    iterator = 0
    c.save_images_to_pdf(filename=filename, image_dir='images', pdf_dir='pdf')
    with open(filename + '.pdf', 'rb') as pdf:
        await message.answer_document(pdf, reply_markup=ReplyKeyboardRemove())
    os.chdir('..')
    h.delete_files_in_folder('images')
    h.delete_files_in_folder('pdf')
    print('finished')


@dp.message_handler(state=FilenameEnterState.ENTER_FILENAME)
async def set_filename(message: types.message.Message, state: FSMContext):
    global filename
    filename = message.text
    if not re.fullmatch(r'^[\w\-. ]+', filename):
        await message.answer('Wrong filename. Enter please valid one')
        return
    await message.answer('Sounds great!\n Now send me photos (not files!) you want to add to your pdf.\n And then '
                         'press Get PDF',
                         reply_markup=finish_keyboard)
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
