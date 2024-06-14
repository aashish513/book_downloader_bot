import asyncio
from io import BytesIO
import re

from pyrogram import Client, filters, idle
from pyrogram.types import Message
from utilities.libg import search_libgen, get_download_url_by_id, get_filename_by_id
from pyrogram.types import (
    ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery)
from pyrogram.enums import ChatAction
from pyrogram.errors import exceptions
from utilities.download_file import download_file_from_url
from utilities import database
# database_object = database.Database()
from utilities import handle_errors
from dotenv import load_dotenv
import os
print("control inside bot.py")
# database_object.connect()
load_dotenv()


bot= Client("bot", api_id=int(os.getenv('AB')),
            api_hash=os.getenv('CD'), 
            bot_token=os.getenv('TOKEN'),
            in_memory=False,
            max_concurrent_transmissions = 50,
            plugins=dict(root="bot_plugins"))





bot.start()  # Automatically start() and idle()
print('started')
a = bot.get_chat(int(os.getenv("BOT_DATA_PRIV_CHANNEL")))
print(a)
idle()