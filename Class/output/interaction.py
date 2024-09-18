import telepot
from telepot.loop import MessageLoop
import time
import os

from chatgpt_api import handle
from output.telegram import send_telegram_message

from inputs.keys_database import *

TELEGRAM_BOT_TOKEN = os.getenv(telegram_token)  # Substitua pelo seu token ou use variáveis de ambiente

bot = telepot.Bot(TELEGRAM_BOT_TOKEN)

def handle_message(msg):
    """
    Função chamada sempre que uma mensagem é recebida pelo bot.
    """
    content_type, chat_type, chat_id = telepot.glance(msg)
    
    if content_type == 'text':
        user_message = msg['text']
        print(f"Mensagem recebida de {chat_id}: {user_message}")
        
        # Chama a função 'handle' para processar a mensagem do usuário
        response_message = handle(user_message)
        
        send_telegram_message(TELEGRAM_BOT_TOKEN, chat_id, response_message)
    else:
        send_telegram_message(TELEGRAM_BOT_TOKEN, chat_id, "Por favor, envie apenas mensagens de texto.")

MessageLoop(bot, handle_message).run_as_thread()
print('O bot está escutando...')

while True:
    time.sleep(10)
