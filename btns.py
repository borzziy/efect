from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

async def start_command_btn():
    btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

    btn.add(
        KeyboardButton(text="🎬Дать рисунку фильтр"),
        KeyboardButton(text="👤Админ")
    )
    return btn

async def filters_btn(filters: list):
    btn = ReplyKeyboardMarkup(resize_keyboard=True)
    
    btn.add(
        *[KeyboardButton(text=item) for item in filters]
    )
    btn.add(
        KeyboardButton(text="Назад")
    )
    return btn

async def cancel_btn():
    btn = ReplyKeyboardMarkup(resize_keyboard=True)

    btn.add(
        KeyboardButton(text="🔙 Отменa")
    )
    return btn