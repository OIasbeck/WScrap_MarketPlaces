import telepot
from telepot.loop import MessageLoop
import openai
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import os

from inputs.keys_database import *

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

openai.api_key = OPENAI_API_KEY

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

user_conversations = {}

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    
    if content_type == 'text':
        user_message = msg['text']
        print(f"Mensagem recebida de {chat_id}: {user_message}")

        # Inicializa o histórico do usuário se não existir
        if chat_id not in user_conversations:
            user_conversations[chat_id] = []

        # Adiciona a mensagem do usuário ao histórico
        user_conversations[chat_id].append({"role": "user", "content": user_message})

        # Envia a conversa para a API do ChatGPT
        try:
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=user_conversations[chat_id]
            )

            assistant_reply = response['choices'][0]['message']['content']

            # Adiciona a resposta do assistente ao histórico
            user_conversations[chat_id].append({"role": "assistant", "content": assistant_reply})

            # Envia a resposta de volta para o usuário
            bot.sendMessage(chat_id, assistant_reply)

        except Exception as e:
            print(f"Erro ao processar a mensagem: {e}")
            bot.sendMessage(chat_id, "Desculpe, ocorreu um erro ao processar sua mensagem.")

    else:
        bot.sendMessage(chat_id, "Por favor, envie apenas mensagens de texto.")
