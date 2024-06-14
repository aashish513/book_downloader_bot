from pyrogram import Client, filters


@Client.on_message(filters.command('start'))
async def start(client, message):
    await message.reply('''Hello! Send me a book name:)
```Examples
<i>Atomic Habits</i>
<i>Ikigai</i>```
''')