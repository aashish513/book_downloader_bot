import aiohttp


import aiohttp
import re
import os
from urllib.parse import urlparse, unquote
from io import BytesIO

async def download_file_from_url(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    # Extract the file name from the Content-Disposition header
                    cd = response.headers.get('content-disposition')
                    if cd:
                        filename = re.findall('filename="(.+)"', cd)
                        print("filename content disposition", filename)
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
                    # Read the file content
                    print(file_name)
                    file_content = await response.read()
                    
                    # Create a BytesIO object and set its name
                    file_bytes = BytesIO(file_content)
                    print(file_bytes)
                    file_bytes.name = file_name
                    print("returning bytesio object")
                    if file_bytes == None:
                        raise Exception("Failed to download from url 28")
                    return file_bytes
    except Exception as e:
        print(f"Failed to download from {url}: {e}")
        raise

