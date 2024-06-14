import aiohttp


import aiohttp
import re
import os
from urllib.parse import urlparse, unquote
from io import BytesIO
from pyrogram.types import Message
import math


def generate_progress_bar(progress):
    red='🟥'
    white='⬜️'

    total_boxes= 10
    red_boxes_number = math.floor(progress/10)
    return red*red_boxes_number + white*(total_boxes-red_boxes_number)


async def download_file_from_url(url, message: Message):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    # Extract the file name from the Content-Disposition header
                    cd = response.headers.get('content-disposition')
                    if cd:
                        filename = re.findall('filename="(.+)"', cd)
                        if filename:
                            file_name = filename[0]
                        else:
                            # Fallback to URL-based filename if Content-Disposition is malformed
                            parsed_url = urlparse(url)
                            file_name = os.path.basename(parsed_url.path)
                    else:
                        # Fallback to URL-based filename if Content-Disposition is missing
                        parsed_url = urlparse(url)
                        file_name = os.path.basename(parsed_url.path)

                    file_name = unquote(str(file_name))
                    # Read the file content in chunks
                    total_size = int(response.headers.get('content-length', 0))
                    downloaded_size = 0
                    file_content = bytearray()

                    last_progress=-20
                    half_mb= 1024*512
                    async for chunk in response.content.iter_chunked(half_mb):
                        if not chunk:
                            break
                        file_content.extend(chunk)
                        downloaded_size += len(chunk)
                        progress = (downloaded_size / total_size) * 100 if total_size else 0
                        if progress != last_progress and progress-last_progress>=11:
                            last_progress = progress
                            try:
                                await message.edit(f"Downloading {generate_progress_bar(progress)}\n{int(progress)}%")
                            except:
                                pass
                    
                    try:
                        await message.edit(f"Uploading...")
                    except:
                        pass

                    # Create a BytesIO object and set its name
                    file_bytes = BytesIO(file_content)
                    file_bytes.name = file_name
                    return file_bytes
    except Exception as e:
        print(f"Failed to download from {url}: {e}")
        raise Exception("byme Failed to download from the url")