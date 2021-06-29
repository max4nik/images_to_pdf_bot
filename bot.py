from aiogram import Bot, Dispatcher, executor, types
import os
from images_to_pdf import Converter
from helper import Helper
from secret import token

bot = Bot(token=token)
dp = Dispatcher(bot)

c = Converter
h = Helper

filename = ''
iterator = 0
is_images = False
isActive = False


@dp.message_handler(commands=['start'])
async def greeting(message: types.message.Message):
    await message.answer('Hello!\n I`ll help you with converting images to pdf! Send /convert to start magic💫')


@dp.message_handler(commands=['help'])
async def get_help(message: types.message.Message):
    await message.answer('Send /convert to convert your images to .pdf')


@dp.message_handler(commands=['convert'])
async def convert_images_to_pdf(message: types.message.Message):
    await message.answer(
        'OK! At first I want you to type name for your file.\nDon`t forget about \'.pdf\' in the end :)')


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


@dp.message_handler(commands=['get_pdf'])
async def send_pdf(message: types.message.Message):
    global filename
    global iterator
    global is_images

    iterator = 0
    c.save_images_to_pdf(filename=filename, image_dir='images', pdf_dir='pdf')
    with open(filename + '.pdf', 'rb') as pdf:
        await message.answer_document(pdf)
    os.chdir('..')
    h.delete_files_in_folder('images')
    h.delete_files_in_folder('pdf')
    print('finished')


@dp.message_handler(regexp='.+[.pdf]')
async def set_filename(message: types.message.Message):
    global filename

    filename = str(message.text[:-4])
    await message.answer('Sounds great!\n Now send me photos you want to add to your pdf.\n And then type /get_pdf')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
