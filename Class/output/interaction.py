import telepot
from telepot.loop import MessageLoop
import time

from Class.output.chatgpt_api import handle
from Class.output.telegram import send_telegram_message

from Class.inputs.keys_database import *

bot = telepot.Bot(telegram_token)

def handle_message(msg):

    content_type, chat_type, chat_id = telepot.glance(msg)
    
    if content_type == 'text':
        user_message = msg['text']
        print(f"mensagem recebida de {chat_id}: {user_message}")
        
        response_message = handle(user_message)
        
        send_telegram_message(telegram_token, chat_id, response_message)
    else:
        send_telegram_message(telegram_token, chat_id, "envie apenas mensagens de texto")

MessageLoop(bot, handle_message).run_as_thread()
print('Escutando..')

while True:
    time.sleep(10)
