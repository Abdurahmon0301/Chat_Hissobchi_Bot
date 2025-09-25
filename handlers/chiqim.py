from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters.command import Command
from loader import db, bot
import io
from google import genai
from google.genai import types
import mimetypes
from aiogram.types import InputFile
import io
import tempfile
import os
client = genai.Client(api_key="AIzaSyBm2OiscJQ7AVv_2J6582HVeGhypwkAwKE")

from utils.gemini import Geminiutils

chiqim_router: Router = Router()

gemini = Geminiutils()


from aiogram import Router, F
from aiogram.types import Message
from loader import bot
from utils.gemini import Geminiutils
import tempfile, os

chiqim_router = Router()
gemini = Geminiutils()

@chiqim_router.message(F.voice | (F.text & ~F.text.startswith("/")))
async def handle_message(message: Message):
    try:
        chiqimtext = None

        if message.voice:  # ovozli habar
            file_id = message.voice.file_id
            file = await bot.get_file(file_id)

            with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as temp_file:
                await bot.download_file(file.file_path, destination=temp_file)
                temp_file_path = temp_file.name

            try:
                chiqimtext = gemini.get_text(temp_file_path)
            finally:
                os.unlink(temp_file_path)

        elif message.text:  # oddiy matn
            chiqimtext = message.text

        if chiqimtext:
            await message.reply(f"{chiqimtext}")
            print(gemini.add_transaction(chiqimtext))

    except Exception as e:
        print(f"errors: {e}")
        await message.reply(f"error: {e}")
