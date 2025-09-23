from aiogram import Bot

from config import Config, load_config
from tables.sqlite import Database

bot: Bot = Bot(token="7677566733:AAEo3s6XPG1W7HbkPm-TYxI2sG4eyFU-WzI")

db  = Database()

