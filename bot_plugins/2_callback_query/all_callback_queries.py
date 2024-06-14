
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
print("control inside get_book_by_id.py")
database_object.connect()
load_dotenv()
BOT_DATA_PRIV_CHANNEL= int(os.getenv("BOT_DATA_PRIV_CHANNEL"))


#filter get_book_by_id
def get_book_by_id(_, __ , query):
    return query.data and query.data.startswith("get_book_by_id")

filter_starts_with_get_book_by_id = filters.create(get_book_by_id)



# Callback query handler
@Client.on_callback_query(filter_starts_with_get_book_by_id)
async def callback_query_handler(client:Client, callback_query: CallbackQuery):
    data = callback_query.data
    chat_id = callback_query.message.chat.id

    rep_msg = await client.send_message(chat_id, "Sending...")
    # await asyncio.sleep(0.5)
    try:
        id:str = data.split("get_book_by_id")[-1]
        try:
            await callback_query.answer(f"Sending book")
        except:
            pass
        
        #check id in mongodb
        tele_msg_id = database_object.find_row(id)
        #if id exists in mongodb
        if tele_msg_id:
            try:
                msgs = await client.get_messages(BOT_DATA_PRIV_CHANNEL, [tele_msg_id])
                msg:Message = msgs[0]

                #by @<something> is already present in caption
                # This regex pattern matches " by @<something>" at the end of the string
                pattern = r"(by|By) @\w+$"
                # Using re.sub to replace the pattern with an empty string
                # print(msg)
                msg.caption = re.sub(pattern, '', msg.caption)

                msg.caption= msg.caption +  f"By @{client.me.username}"
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
        file_name = file_name + "\nBy @"+ client.me.username

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
                await client.send_chat_action(chat_id,ChatAction.UPLOAD_DOCUMENT)
                file:BytesIO = await download_file_from_url(url, rep_msg)
                if file == None:
                    continue
                # print(type(file))
                # print(len(file))
                await client.send_chat_action(chat_id,ChatAction.UPLOAD_DOCUMENT)
                book_msg = await client.send_document(chat_id, file, caption = file_name)
                try:
                    book_msg = await book_msg.copy(BOT_DATA_PRIV_CHANNEL)
                except Exception as e:
                    await handle_errors.send_error_to_me(f"Error occured in copying message to priv channel error: {e}", client)
                    
                try:
                    database_object.insert_row(id, book_msg.id)
                except Exception as e:
                    await handle_errors.send_error_to_me(f"Error occured in inserting to database error: {e}", client)
                del file
                return
                
            except Exception as e:
                await handle_errors.send_error_to_me(f"error here in sending downloading file error: {e}", client)
        
        await rep_msg.edit("Error occured. Please search again!")
        try:
            await callback_query.answer(f"Error. Please try searching again")
        except:
            pass
    except Exception as e:
        await handle_errors.send_error_to_me(f"error2 here in sending downloading file error: {e}", client)
        await rep_msg.edit("Error occured. Please search again")
        await callback_query.answer(f"Error. Please try searching again")
