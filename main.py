import random
from logging import basicConfig, getLogger, INFO

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from keyboard import level_keyboard, stop_game
from state import LevelState

basicConfig(level=INFO)
log = getLogger()

storage = MemoryStorage()

BOT_TOKEN = "7327681875:AAFqR0oWnHwFs71oMfvhdM4r6WrgAIN5up4"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot=bot, storage=storage)
counter = 0
counter_false = 0
counter_true = 0


@dp.message_handler(commands="start")
async def start_bot(message: types.Message):
    await message.answer("Botga xush kelibsiz, bu botda matematik savollar beriladi. Daraja tanlang!",
                         reply_markup=level_keyboard())
    await LevelState.question.set()


@dp.message_handler(Text(equals='Stop the Game🛑'), state=LevelState.question)
async def start_bot(message: types.Message, state: FSMContext):
    global counter, counter_true, counter_false
    async with state.proxy() as data:
        await message.answer("Game stopped", reply_markup=level_keyboard())
        data['level'] = None
        await message.answer(
            f"Jami savollar:{counter}\nTo'g'ri javob:{counter_true}\nNoto'g'ri javob:{counter_false}")
        counter, counter_false, counter_true = 0, 0, 0
        await state.finish()


@dp.message_handler(state=LevelState.question)
async def handle_question(message: types.Message, state: FSMContext):
    global counter, counter_true, counter_false
    if message.text == "Level 1️⃣":
        question = f"{random.randint(1, 11)} {random.choice(['+', '-', '*'])} {random.randint(1, 11)}"
        await message.answer(f"{question} = ?", reply_markup=stop_game())
        counter += 1

    elif message.text == "Level 2️⃣":
        question = f"{random.randint(1, 50)} {random.choice(['+', '-', '*'])} {random.randint(1, 50)}"
        await message.answer(f"{question} = ?", reply_markup=stop_game())
        counter += 1

    elif message.text == "Level 3️⃣":
        question = f"{random.randint(1, 100)} {random.choice(['+', '-', '*', '/'])} {random.randint(1, 100)}"
        await message.answer(f"{question} = ?", reply_markup=stop_game())
        counter += 1

    elif message.text == "Level 4️⃣":
        question = f"{random.randint(1, 200)} {random.choice(['+', '-', '*', '/'])} {random.randint(1, 150)}"
        await message.answer(f"{question} = ?", reply_markup=stop_game())
        counter += 1

    async with state.proxy() as data:
        data['computer_answer'] = eval(question)
        data['level'] = message.text

    await LevelState.next()


@dp.message_handler(state=LevelState.answer)
async def handle_question(message: types.Message, state: FSMContext):
    global counter, counter_true, counter_false

    async with state.proxy() as data:

        if message.text == 'Stop the Game🛑':
            await message.answer("Game stopped", reply_markup=level_keyboard())
            data['level'] = None
            await message.answer(
                f"Jami savollar:{counter}\nTo'g'ri javob:{counter_true}\nNoto'g'ri javob:{counter_false}"
                f"\nJavob berilmaganlar:{counter - (counter_false + counter_true)}")
            counter, counter_false, counter_true = 0, 0, 0
            await LevelState.question.set()

        if float(message.text) == float(data["computer_answer"]) and not message.text == 'Stop the Game🛑':
            await message.answer("✅")
            counter_true += 1
        else:
            await message.answer("❌")
            counter_false += 1
            await message.answer(f"To'g'ri javob:{data['computer_answer']}")

        if data['level'] == "Level 1️⃣":
            question = f"{random.randint(1, 11)} {random.choice(['+', '-', '*'])} {random.randint(1, 11)}"
            await message.answer(f"{question} = ?", reply_markup=stop_game())
            counter += 1
        elif data['level'] == "Level 2️⃣":
            question = f"{random.randint(1, 18)} {random.choice(['+', '-', '*'])} {random.randint(1, 11)}"
            await message.answer(f"{question} = ?", reply_markup=stop_game())
            counter += 1
        elif data['level'] == "Level 3️⃣":
            question = f"{random.randint(1, 18)} {random.choice(['+', '-', '*', '/'])} {random.randint(1, 18)}"
            await message.answer(f"{question} = ?", reply_markup=stop_game())
            counter += 1
        elif data['level'] == "Level 4️⃣":
            question = f"{random.randint(1, 40)} {random.choice(['+', '-', '*', '/'])} {random.randint(1, 40)}"
            await message.answer(f"{question} = ?", reply_markup=stop_game())
            counter += 1

        data['computer_answer'] = eval(question)


if __name__ == '__main__':
    executor.start_polling(dp)
