from openai import OpenAI
import os

from Class.inputs.keys_database import api_gpt

client = OpenAI(
    api_key = api_gpt,
)

def handle(user_message):

    try:
        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        assistant_reply = response.choices[0].message.content
        return assistant_reply.strip()
    except Exception as e:
        print(f"Erro na função handle:\n\n{e}")
        return "Desculpe, ocorreu um erro ao processar sua mensagem."
