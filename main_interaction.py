import telepot
from telepot.loop import MessageLoop
import time

from Class.output.interaction_bot.request_handler import handle_request
from Class.output.interaction_bot.telegram import send_telegram_message

from Class.inputs.keys_database import *
from Class.inputs.get_conections import Get_connection

bot = telepot.Bot(telegram_token)

client = Get_connection.conn() # ------------>>
db = client['scrapping_google']
collection = db['restaurants']


def handle_message(msg):

    content_type, chat_type, chat_id = telepot.glance(msg)
    print(f"content Type: {content_type}, chat Type: {chat_type}, chat ID: {chat_id}")
    
    if content_type == 'text':
        user_message = msg['text']
        print(f"mensagem recebida de {chat_id}: {user_message}")
        
        response_message = handle_request(user_message, collection)
        
        send_telegram_message(telegram_token, chat_id, response_message)
    else:
        send_telegram_message(telegram_token, chat_id, "Por favor, envie apenas mensagens de texto.")

MessageLoop(bot, handle_message).run_as_thread()
print('Manda bala')

while True:
    time.sleep(10)

