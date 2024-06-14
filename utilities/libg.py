import asyncio
from libgen_api import LibgenSearch
from utilities.handle_errors import send_error_to_me
from utilities.download_file import download_file_from_url
import traceback
s = LibgenSearch()
cached_queries={}

async def search_libgen(query, page=0):
    if query in cached_queries:
        return cached_queries[query][page*10: (page+1)*10]
    
    try:
        books = s.search_title(query)  #at max 25 results are returned
        cached_queries[query] = books
    except Exception as e:
        await send_error_to_me("Error for query {query}\n", traceback.print_exc())
        raise Exception("Error")

    if len(books) == 0:
        #no books found
        raise Exception("Empty")
    else:
        return books[page*10: (page+1)*10]

async def get_download_url_by_id(book_id:str):
    for query in reversed(cached_queries):
        for book in cached_queries[query]:
            if book["ID"] == book_id:
                book_data_dict= book
                download_links = s.resolve_download_links(book_data_dict)
                # print(download_links)
#                 file_name = f'''Title: {book_data_dict['Title']}
# Author: {book_data_dict['Author']}
# Pages: {book_data_dict['Pages']}
# Pubisher: {book_data_dict['Publisher']}
# Year: {book_data_dict['Year']}
# Language: {book_data_dict['Language']}
# File Type: {book_data_dict['Extension']}
# Size : {book_data_dict['Size']}'''
                download_links_list=[]
                # if 'Cloudflare' in download_links:
                #     download_links_list.append(download_links['Cloudflare'])
                # if 'IPFS.io' in download_links:
                #     download_links_list.append(download_links['IPFS.io'])
                
                for index in download_links:
                    # if index not in ['Cloudflare', 'IPFS.io']:
                    download_links_list.append(download_links[index])
                
                return download_links_list



async def get_filename_by_id(book_id:str):
    for query in reversed(cached_queries):
        for book in cached_queries[query]:
            if book["ID"] == book_id:
                book_data_dict= book
                file_name = f'''Title: {book_data_dict['Title']}
Author: {book_data_dict['Author']}
Pages: {book_data_dict['Pages']}
Pubisher: {book_data_dict['Publisher']}
Year: {book_data_dict['Year']}
Language: {book_data_dict['Language']}
File Type: {book_data_dict['Extension']}
Size : {book_data_dict['Size']}'''
                return file_name






    

# Example usage
async def main():
    books = await search_libgen("machine learning")
    for book in books:
        # print(book)
        pass

if __name__== "__main__":
    asyncio.run(main())
