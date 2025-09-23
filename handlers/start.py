from aiogram import Router, F
from aiogram.types import CallbackQuery
from loader import bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from keyboards.keyboards import signup
from aiogram.filters.command import Command
from states.signup import Form
from loader import db
from keyboards.keyboards import phone_num



start_router: Router = Router()



@start_router.message(Command("start"))
async def start_msg(message: Message):
    try:
        db.add_user(id = message.from_user.id, name=message.from_user.full_name, language=message.from_user.language_code)
    except Exception as e:
        print("User allaqachon bor")

    await message.answer_video("BAACAgIAAxkBAAMSaMUi6cB1tOW27rrM-ccUOiRsZ8YAAvdzAALt9nlJ0e5q_aAHuIo2BA")
    await message.answer(
        """
        Xush kelibsiz! 👋

📊 Hisobchi AI – bu shaxsiy moliyalaringizni avtomatik boshqaruvchi AI yordamchi.

    💡 Nimalar qila oladi?:
    - Sizni ovozingiz orqali tushuna oladi 💬
    - Kirim-chiqimlaringizni tahlil qiladi 📊
    - Xarajatlaringizni toifalarga ajratadi 🏷
    - Moliyaviy intizomni shakllantirishga yordam beradi ✅

Botdan foydalanib, Ofertamiz (https://behad.uz/xisobchioferta.html) shartlariga rozilik bildirasiz

⏩ Bo'tdan foydlanish uchun avval royxatdan o'ting 👇
""",
reply_markup=signup
        )

help: Router = Router()


@help.message(Command("help"))
async def process_any_message(message: Message):
    await message.answer_video("BAACAgIAAxkBAAMjaMUk8-2eXFiK3Jc4ywIwllLVhGUAAlV4AAKxVehJxIQh9lYNcdA2BA")
    await message.answer(
"""
📊 Hisobchi AI – bu shaxsiy moliyalaringizni avtomatik boshqaruvchi AI yordamchi.

    💡 Nimalar qila oladi?:
    - Sizni ovozingiz orqali tushuna oladi 💬
    - Kirim-chiqimlaringizni tahlil qiladi 📊
    - Xarajatlaringizni toifalarga ajratadi 🏷
    - Moliyaviy intizomni shakllantirishga yordam beradi ✅

""", 
    )

signup_router: Router = Router()


@signup_router.callback_query(F.data == "signup")
async def first_state_func(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Form.phone)
    await bot.send_message(
        chat_id=callback.from_user.id,
        text="Pastdagi tugmani bosing va telefon raqamingizni yuboring: ",
        reply_markup=phone_num
    )

@signup_router.message(Form.phone)
async def phone_state_func(message: Message, state: FSMContext):
    if not message.contact:
        await message.answer("Iltimos, telefon raqamingizni yuborish tugmasini bosing!")
        return
        
    await state.set_state(Form.first_name)
    await bot.send_message(chat_id=message.from_user.id, text="Ismingizni kiriting: ")
    phonenum = message.contact.phone_number
    await state.update_data(phone=phonenum)


@signup_router.message(Form.first_name)
async def finish_signup(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    data = await state.get_data()

    await message.answer("Ro'yxatdan o'tganingiz uchun rahmat! Endi botdan foydalanishingiz mumkin. Agar bot ishlatish haqida yordam kerak bo'lsa /help ni bosing.")

    matn = "Yangi akkaunt: \n\n"
    matn += f"Ism: {data['first_name']}\n"
    matn += f"Telefon raqam: {data['phone']}\n"

    await bot.send_message(chat_id="-1003073215342", text=matn)

    await state.clear()
