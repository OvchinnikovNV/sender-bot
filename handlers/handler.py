import os
from telebot import TeleBot
from dotenv import load_dotenv

from handlers import start_handler
from handlers import help_handler
from handlers import text_handler
from handlers import photo_handler
from handlers import video_handler


load_dotenv()

bot = TeleBot(os.getenv('TG_TOKEN'))

start_handler.handle(bot)
help_handler.handle(bot)
text_handler.handle(bot)
photo_handler.handle(bot)
video_handler.handle(bot)
