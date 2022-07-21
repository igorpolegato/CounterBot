from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ParseMode

from data import *

from datetime import datetime
import threading

app = Client(bot_name,
            api_id=api_id,
            api_hash=api_hash,
            bot_token=bot_token)


with app:
    pass

lock = threading.Lock()

#================= FUNÇÕES ===============#

@app.on_message(filters.private & filters.command("contar"))
def Contar(bot, mensagem):
    msgs = app.get_messages(-1001711893062, genRange(2, 2))

    for msg in msgs:
        print(msg)

def genRange(mn, mx):
    l = []

    while mn <= mx:
        l.append(mn)
        mn += 1
    
    return l

if __name__ == "__main__":
    app.run()