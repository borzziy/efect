import logging

from aiogram import Dispatcher, types, Bot, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from btns import *
from utils import *
from database import *
from states import *
import os


BOT_TOKEN = "6370464277:AAHZlPzWYdJVBqVnYQv0byuHeljKscJBUEQ"
admins = [971389287]

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, parse_mode="html")
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)


async def command_menu(dp: Dispatcher):
    await create_tables()
    await dp.bot.set_my_commands(   
        [
            types.BotCommand('start', 'Ishga tushirish'),
        ]
    )


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await add_user(
        user_id=message.from_user.id,
        username=message.from_user.username
    )
    btn = await start_command_btn()
    await message.answer("Привет Я бот фильтр", reply_markup=btn)


@dp.message_handler(commands=["stat"])
async def get_user_stat_handler(message: types.Message):
    if message.from_user.id in admins:
        counts = await get_all_users()
        await message.answer(f"Людей в боте: {counts}")


@dp.message_handler(text=["🎬Дать рисунку фильтр"])
async def effect_to_image_handler(message: types.Message):
    btn = await filters_btn(filters)
    await message.answer("выберите фильтр", reply_markup=btn) 


@dp.message_handler(text=["Назад"])
async def back_handler(message: types.Message):
    await start_command(message)


@dp.message_handler(state=UsersStates.get_image, content_types=['photo', 'text'])
async def get_image_handler(message: types.Message, state: FSMContext):
    content = message.content_type

    if content == "text":
        await effect_to_image_handler(message)
    else:
        filename = f"rasim _{message.from_id}.jpg"
        await message.photo[-1].download(destination_file=filename)
        await message.answer("rasm qabul qilindi!")

        data = await state.get_data()
        await filter_user_image(filename, data['filter'])
        await message.answer_photo(
            photo=types.InputFile(filename),
            caption = f"rasimiz tayor:))"
        )
        os.remove(filename)
        await start_command(message)
    await state.finish()


@dp.message_handler(content_types=["text"])
async def selected_filter_handler(message: types.Message, state: FSMContext):
    text = message.text

    if text in filters:
        await state.update_data(filter=text)
        btn = await cancel_btn()
        await message.answer("Отправьте рисунок:", reply_markup=btn)
        await UsersStates.get_image.set()




@dp.message_handler(text="👤Админ")
async def selected_filter_handler(message: types.Message):
    await message.answer("admin ga prosta tak yozmela @tolkinovicc ")



if __name__ == "__main__":
    executor.start_polling(dp, on_startup=command_menu)
