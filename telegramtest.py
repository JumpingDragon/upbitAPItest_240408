# pip install python-telegram-bot

import telegram
import asyncio

bot = telegram.Bot(token="<Enter your token gotten from @BotFather>")
chat_id = "<Enter your chat id gotten from 'https://api.telegram.org/bot<token>/getUpdates>"

asyncio.run(bot.sendMessage(chat_id=chat_id, text="안녕하세요, 테스트합니다. 3,2,1"))
