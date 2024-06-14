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
database_object = database.Database()
from utilities import handle_errors
from dotenv import load_dotenv
import os
print("control inside bot.py")
database_object.connect()
load_dotenv()
bot= Client("bot", api_id=int(os.getenv('AB')),
            api_hash=os.getenv('CD'), 
            bot_token=os.getenv('TOKEN'),
            in_memory=False,
            max_concurrent_transmissions = 50)


# Start command handler
@bot.on_message(filters.command('start'))
async def start(client, message):
    await message.reply('''Hello! Send me a book name:)
```Examples
<i>Atomic Habits</i>
<i>Ikigai</i>```
''')



# Callback query handler
@bot.on_callback_query()
async def callback_query_handler(client:Client, callback_query: CallbackQuery):
    data = callback_query.data
    chat_id = callback_query.message.chat.id

    if data.startswith("get_book_by_id"):
        rep_msg = await bot.send_message(chat_id, "Sending...")
        # await asyncio.sleep(0.5)
        try:
            id:str = data.split("get_book_by_id")[-1]
            await callback_query.answer(f"Sending book")
            
            #check id in mongodb
            tele_msg_id = database_object.find_row(id)
            #if id exists in mongodb
            if tele_msg_id:
                try:
                    msgs = await client.get_messages(int(os.getenv("BOT_DATA_PRIV_CHANNEL")), [tele_msg_id])
                    msg:Message = msgs[0]

                    #by @<something> is already present in caption
                    # This regex pattern matches " by @<something>" at the end of the string
                    pattern = r"(by|By) @\w+$"
                    # Using re.sub to replace the pattern with an empty string
                    # print(msg)
                    msg.caption = re.sub(pattern, '', msg.caption)

                    msg.caption= msg.caption +  f"By @{BOT_USERNAME}"
                    # print(msg.caption)
                    msg.caption_entities = None
                    # print(msg)

                    await msg.copy(chat_id)
                    print("message sent using copy method. mongodb")
                    return
                except Exception as e:
                    await handle_errors.send_error_to_me("Errro at 33 error: "+str(e), client)

            #if doesnt exist in mongodb
            file_name=await get_filename_by_id(id)
            if not file_name:
                await rep_msg.edit("You are using one of the previous messages. Please search again!")
                return
            file_name = file_name + "\nBy @"+ BOT_USERNAME

            list_urls = await get_download_url_by_id(id)
            
            #use telegram server to upload file
            # for url in list_urls:
            #     try:
            #         print("trying url ", url)
            #         await bot.send_chat_action(chat_id,ChatAction.UPLOAD_DOCUMENT )
            #         book_msg= await bot.send_document(chat_id, url, caption = file_name)
            #         book_msg = await book_msg.copy(int(os.getenv("BOT_DATA_PRIV_CHANNEL")))
            #         database_object.insert_row(id, book_msg.id)
            #         return
            #     except exceptions.bad_request_400.WebpageCurlFailed:
            #         print("bad_request_400.WebpageCurlFailed")
            #     except exceptions.bad_request_400.MediaEmpty:
            #         print("bad_request_400.MediaEmpty")
            #     except Exception as e:
            #         print(e)


            #download file here, then send to telegram
            for url in list_urls:
                #download that file here and then send
                try:
                    print(url)
                    await bot.send_chat_action(chat_id,ChatAction.UPLOAD_DOCUMENT)
                    file:BytesIO = await download_file_from_url(url)
                    if file == None:
                        continue
                    # print(type(file))
                    # print(len(file))
                    await bot.send_chat_action(chat_id,ChatAction.UPLOAD_DOCUMENT)
                    book_msg = await bot.send_document(chat_id, file, caption = file_name)
                    try:
                        book_msg = await book_msg.copy(int(os.getenv("BOT_DATA_PRIV_CHANNEL")))
                        database_object.insert_row(id, book_msg.id)
                    except Exception as e:
                        await handle_errors.send_error_to_me(f"Error occured in inserting to database or copying message to priv channel error: {e}", client)
                    del file
                    return
                    
                except Exception as e:
                    await handle_errors.send_error_to_me(f"error here in sending downloading file error: {e}", client)
            
            await rep_msg.edit("Error occured. Please search again")
            await callback_query.answer(f"Error. Please try searching again")
        except Exception as e:
            await handle_errors.send_error_to_me(f"error2 here in sending downloading file error: {e}", client)
            await rep_msg.edit("Error occured. Please search again")
            await callback_query.answer(f"Error. Please try searching again")

        



    




@bot.on_message(filters.text & filters.private & filters.incoming)
async def search(client, message:Message):
    await message.reply_chat_action(action=ChatAction.TYPING)
    query= message.text
    await asyncio.sleep(0.5)
    if len(query)<3:
        await message.reply("The search query is too short. Try again")
        return
    sent_msg:Message = await message.reply(f'Searching for <i>{query}</i>...')
    try:
        books= await search_libgen(query)
    except Exception as e:
        if e == "Empty":
            await sent_msg.edit(text= f"No results found for <i>{query}</i>")
        elif e == "Error":
            await sent_msg.edit(text= f"Error occured for <i>{query}</i>. Please try again")
        return
    
    
    list_of_markups= [] 
    for book in books:
        list_of_markups.append(
            [InlineKeyboardButton(f"[{book['Extension'].upper()}] {book['Title']} by {book['Author']}", callback_data="get_book_by_id"+book['ID'])]
        )
    result_markup= InlineKeyboardMarkup(list_of_markups)
    
    await sent_msg.edit(text= f"Found {len(books)} results for <i>{query}</i>",
                        reply_markup=result_markup)

        






bot.start()  # Automatically start() and idle()
print('started')
bot_user_object= bot.me
BOT_USERNAME= bot_user_object.username
print(bot_user_object, BOT_USERNAME)
a = bot.get_chat(int(os.getenv("BOT_DATA_PRIV_CHANNEL")))
print(a)

print(bot.export_session_string())
idle()