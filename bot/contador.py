from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ParseMode

from data import *

from datetime import datetime
import threading
import re

app = Client(bot_name,
            api_id=api_id,
            api_hash=api_hash,
            bot_token=bot_token)


with app:
    pass

lock = threading.Lock()
CONTAR = []
DATAS = {}

#================= FUNÇÕES ===============#
@app.on_message(filters.private & filters.command("start"))
def start(bot, mensagem):
    user_id = mensagem.chat.id

    if perm(user_id):
        app.send_message(mensagem.chat.id, "Olá!\nPara contar as mensagens envie\n/contar!")
    else:
        app.send_message(user_id, "Você não tem permissão para utilizar os comandos do bot!")

@app.on_message(filters.private & filters.command("contar"))
def initialize(bot, mensagem):
    user_id = mensagem.chat.id

    if perm(user_id):
        if "ini" not in CONTAR:
            CONTAR.append("ini")
        if "final" not in CONTAR:
            CONTAR.append("final")

        app.send_message(user_id, "Envie a data inicial no seguinte formato:\n\ndd/mm/yyyy")
    else:
        app.send_message(user_id, "Você não possui permissão para utilizar este bot!")

@app.on_message(filters.private)
def interact(bot, mensagem):
    user_id = mensagem.chat.id
    text = mensagem.text

    if "ini" in CONTAR:
        if re.match("[0-9]{2}\/[0-9]{2}\/[0-9]{4}", text):
            day, month, year = map(int, text.split("/"))
            DATAS['ini'] = datetime(year, month, day).date()

            CONTAR.remove("ini")
            app.send_message(user_id, "Envie a data final no seguinte formato:\n\ndd/mm/yyyy")
        else:
            app.send_message(user_id, "Formato inválido!")
            app.send_message(user_id, "Envie a data inicial no seguinte formato:\n\ndd/mm/yyyy")

    elif "final" in CONTAR:
        if re.match("[0-9]{2}\/[0-9]{2}\/[0-9]{4}", text):
            day, month, year = map(int, text.split("/"))
            DATAS['final'] = datetime(year, month, day).date()

            CONTAR.remove("final")
            app.send_message(user_id, "Contando mensagem, aguarde...")
            contar(user_id)
        else:
            app.send_message(user_id, "Formato inválido!")
            app.send_message(user_id, "Envie a data final no seguinte formato:\n\ndd/mm/yyyy")


def contar(user_id):
    count = {}
    msgs = []
    n = 0
    print(f"Intervalo definido entre {min_range} e {max_range}\n")
    for i in genRange(min_range, max_range):
        msgs.append(app.get_messages(gp_id, i))
        if i % 100 == 0:
            print(str(n) + " mensagens analizadas!\nFaltam " + str(max_range - i) + "\n")
            n += 100
    text = "Essas foram a quantidade de mensagens que cada usuário enviou neste período:\n\n"
    for msg in msgs:
        author = msg.author_signature
        
        if msg.text is None:
            txt = msg.caption
        else:
            txt = msg.text

        if author is not None:
            date = msg.date.date()
            if DATAS['ini'] <= date <= DATAS['final']:
                try:
                    if not any(l in txt for l in lk_ignore):
                        if author not in count.keys():
                            count[author] = 1
                        else:
                            count[author] += 1
                except Exception:
                    if txt is None:
                        if author not in count.keys():
                            count[author] = 1
                        else:
                            count[author] += 1

    if len(count) == 0:
        text = "Não houve nenhuma mensagem neste período"
    else:
        for k, v in count.items():
            text += f"{k}: {v}\n"
    
    app.send_message(user_id, text)

def perm(user_id):
    return user_id in perm_users

def genRange(mn, mx):
    l = []

    while mn <= mx:
        l.append(mn)
        mn += 1
    
    return l



if __name__ == "__main__":
    print("+---------------------+\n"
          "|  CountBot Iniciado  |\n"
          "+---------------------+\n")
    app.run()
