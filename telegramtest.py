# pip install python-telegram-bot

import telegram
import asyncio

bot = telegram.Bot(token="7091855340:AAHTZwEh7HZJMeDjlcAofUzcMUzmni5TVvI")
chat_id = "6362648014"

asyncio.run(bot.sendMessage(chat_id=chat_id, text="안녕하세요, 테스트합니다. 3,2,1"))
