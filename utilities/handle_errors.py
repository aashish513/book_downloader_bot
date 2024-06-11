from pyrogram import Client
from dotenv import load_dotenv
import os


load_dotenv()

debug_errors= True
async def send_error_to_me(error:str, pyrogram_client:Client):
    if debug_errors:
        print(error)
    
    
    while True:
        err = error[:4000]
        # print("333330", err)
        if len(err) == 0:
            break
        error= error[4000:]
        await pyrogram_client.send_message(int(os.getenv("BOT_DATA_PRIV_CHANNEL")), err)
    