import os
import random

from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, MessageAutoDeleteTimerChanged

from states import LevelState
from keyboards import levels_btn, stop_btn, start_btn

router = Router()

def get_min_max_number(level):
    # funksiyani qolgan lever uchun xam moslash kerak
    if level == "Level 1️⃣":
        return 1, 11
    elif level == "Level 2️⃣":
        return 10, 101

@router.message(CommandStart())
async def start_command(message: Message):

    image = FSInputFile(os.path.join(os.path.dirname(__file__), "images", "math_img.png"))
    from_user = message.from_user
    first_name = from_user.first_name
    last_name = from_user.last_name
    full_name = f"{first_name} {last_name if last_name else ''}"
    await message.answer(f"Salom {full_name}")
    await message.answer_photo(photo=image, caption=f"Xush kelibsiz {full_name}bilag'on, "
                                                    f"sizga bir nechta savollar berib "
                                                    f"bilimingizni tekshirib beramiz!", reply_markup=levels_btn)

@router.message(F.text == "🎲Boshlash")
async def start_game(message: Message):
    await message.answer("O'yin qaytadan boshlandi!", reply_markup=levels_btn)

@router.message(F.text == "Level 1️⃣")
async def level_1(message: Message, state: FSMContext):
    question = (f"{random.randint(1, 11)} {random.choice(['+', '-', '*'])}"
                f" {random.randint(1, 11)}")
    answer = eval(question)
    await state.update_data(answer=answer, question=question, level="Level 1️⃣",
                            correct=0, incorrect=0)
    await message.answer(text=f"SAVOL: {question} = ?", reply_markup=stop_btn)
    await state.set_state(LevelState.javob)



@router.message(StateFilter(LevelState.javob))
async def process_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    correct_answer = data.get("answer")
    correct = data.get("correct", 0)
    incorrect = data.get("incorrect", 0)
    level = data.get("level")
    if message.text == "🛑STOP":
        text = (f"{level}\n"
                f"Savollar soni: {correct + incorrect}\n"
                f"✅To'g'ri javoblar: {correct}\n"
                f"❌Noto'g'ri javoblar: {incorrect}\n")
        await message.answer(text, reply_markup=start_btn)
        await state.clear()
        return
    try:
        user_answer = int(message.text)
        if user_answer == correct_answer:
            correct += 1
            await message.answer("✅Javob to'g'ri!")
        else:
            incorrect += 1
            await message.answer(f"❌Javob noto'g'ri!\n✅To'g'ri javob: {correct_answer}")
    except ValueError:
        await message.answer("Iltimos raqam kiriting")

    min_number, max_number = get_min_max_number(level)
    question = (f"{random.randint(min_number, max_number)}"
                f"{random.choice(['+', '-', '*'])}"
                f"{random.randint(min_number, max_number)}")
    answer = eval(question)
    await state.update_data(answer=answer, question=question, correct=correct, incorrect=incorrect)
    await message.answer(text=f"SAVOL: {question} = ?", reply_markup=stop_btn)
