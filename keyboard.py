from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def level_keyboard():
    rkm = ReplyKeyboardMarkup(resize_keyboard=True)
    rkm.row(KeyboardButton(text="Level 1️⃣"), KeyboardButton(text="Level 2️⃣"))
    rkm.row(KeyboardButton(text="Level 3️⃣"), KeyboardButton(text="Level 4️⃣"))
    return rkm


def stop_game():
    rkm = ReplyKeyboardMarkup(resize_keyboard=True)
    rkm.row("Stop the Game🛑")
    return rkm
