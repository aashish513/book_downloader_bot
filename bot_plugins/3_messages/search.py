import random
from pyrogram import Client, filters, idle
from pyrogram.types import Message
from utilities.libg import search_libgen, get_download_url_by_id, get_filename_by_id
from pyrogram.types import (
    ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery)
from pyrogram.enums import ChatAction
from pyrogram.errors import exceptions
import asyncio



@Client.on_message(filters.text & filters.private & filters.incoming)
async def search(client, message:Message):
    query= message.text
    # await asyncio.sleep(0.5)
    if len(query)<3:
        await message.reply("The search query is too short. Try again")
        return
    
    search_stickers=['CAACAgIAAxkBAAEr_lZmbC179jzSDg_9Nn5lneU5zuXp0AACogEAAladvQpBnnI7eRH13TUE', 'CAACAgIAAxkBAAEr_mJmbC349UK8y1SO-8lsAAHl13xs5pgAAlUAA6_GURpk5_zwJekQvzUE']
    try:
        await message.reply_sticker(random.choice(search_stickers))
        await message.reply_chat_action(action=ChatAction.TYPING)
        await asyncio.sleep(1)
    except:
        pass
    sent_msg:Message = await message.reply(f'Searching far and wide for <i>{query}</i>...', quote=True)
    try:
        books= await search_libgen(query)
    except Exception as e:
        if e == "Empty":
            await sent_msg.edit(text= f"No results found for <i>{query}</i>")
        elif e == "Error":
            await sent_msg.edit(text= f"Error occured for <i>{query}</i>. Please try again")
        else:
            await sent_msg.edit(text= f"No results found for <i>{query}</i>. Please check for typo!")
        return
    
    
    list_of_markups= [] 
    for book in books:
        list_of_markups.append(
            [InlineKeyboardButton(f"[{book['Extension'].upper()}] {book['Title']} by {book['Author']}", callback_data="get_book_by_id"+book['ID'])]
        )
    result_markup= InlineKeyboardMarkup(list_of_markups)
    
    await sent_msg.edit(text= f"Found {len(books)} results for <i>{query}</i>",
                        reply_markup=result_markup)

        