import json

from Class.inputs.keys_all import *
from Class.inputs.keys_database import api_gpt
from crude_functions import *

from openai import OpenAI
import nltk
from nltk.corpus import stopwords

client = OpenAI(
    api_key = api_gpt,
)

nltk.download('stopwords')
stopwords_pt = set(stopwords.words('portuguese'))

chat_context = []

def remove_stopwords(text, stopwords_set):
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in stopwords_set]
    return ' '.join(filtered_words)

def interpret_user_message(user_message):
    system_prompt = (
        "Você é um assistente que interpreta solicitações de usuários "
        "para consultas e operações CRUD em um banco de dados de restaurantes. "
        "Responda no formato JSON com os campos 'intent' e 'parameters'. "
        "Os tipos no campo intent podem ser: recommendation, smalltalk, update, select, delete. "
        "Se o usuário estiver pedindo para realizar operações no banco de dados como atualizar ou consultar um restaurante, defina o intent como update, select, ou delete conforme apropriado. "
        "Os 'parameters' devem conter os campos necessários para realizar a operação, como 'nome', 'id', 'campo' (para updates), e 'valor'. "
        "Se o usuário estiver apenas conversando, defina 'intent' como 'smalltalk'. "
        "Se o usuário estiver pedindo recomendações de restaurantes, defina 'intent' como 'recommendation'. "
        "Não inclua explicações adicionais."
    )
    
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    )
    
    assistant_reply = response.choices[0].message.content.strip()
    return assistant_reply

def process_intent(intent_data, collection, user_message):
    intent = intent_data.get('intent')
    parameters = intent_data.get('parameters', {})

    if intent == 'recommendation':

        num_restaurantes = 20
        data = []
        cursor = collection.find({}, {'_id': 0}).limit(num_restaurantes)
        for restaurant in cursor:
            nome = restaurant.get('NOME', '')
            nota = restaurant.get('NOTA_REVIEW', '')
            endereco = restaurant.get('ENDERECO', '')
            hr_funcionamento = restaurant.get('HR_FUNCIONAMENTO', {})
            maior_movimento = restaurant.get('MAIOR_MOVIMENTO', '')
            telefone = restaurant.get('TELEFONE', '')
            detalhes = restaurant.get('DETALHES', {})
            
            nome = remove_stopwords(nome, stopwords_pt)
            endereco = remove_stopwords(endereco, stopwords_pt)
            
            detalhes_texto = ''
            for key, value in detalhes.items():
                key_clean = remove_stopwords(str(key), stopwords_pt)
                value_clean = remove_stopwords(str(value), stopwords_pt)
                detalhes_texto += f"{key_clean}: {value_clean}, "
            detalhes_texto = detalhes_texto.rstrip(', ')
            
            resumo = f"Nome (campo NOME): {nome}, Nota (campo NOTA_REVIEW): {nota}, Endereço (campo ENDERECO): {endereco}, Horario Funcionamento (campo HR_FUNCIONAMENTO): {hr_funcionamento}, Horario de Maior Movimento Horario Funcionamento (campo MAIOR_MOVIMENTO): {maior_movimento}, Telefone (campo TELEFONE): {telefone}, Detalhes (campo DETALHES): {detalhes_texto}"
            data.append(resumo)
        data_str = "\n".join(data)

        system_prompt = (
            "Você é um assistente que ajuda os usuários a encontrar restaurantes com base em seus critérios. "
            "Use os dados fornecidos para responder à solicitação do usuário. "
            "Apenas responda a pergunta, não envie textos longos, responda em tópicos de preferência. "
            "Responda apenas a solicitação do usuário."
            "Não recomende mais de 2 restaurantes, a menos que o usuário solicite."
            "Não exiba detalhes dos restaurantes, apenas se o usuário pedir."
        )

        chat_context.append({"role": "user", "content": user_message})
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Dados dos restaurantes: {data_str}"}
        ] + chat_context[-6:]
        
        response = client.chat.completions.create(
            model='gpt-4-1106-preview',
            messages=messages
        )
        assistant_reply = response.choices[0].message.content.strip()

        chat_context.append({"role": "assistant", "content": assistant_reply})
        
        return assistant_reply
    
    elif intent == 'smalltalk':
        chat_context.append({"role": "user", "content": user_message})
        
        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=chat_context[-6:]
        )
        assistant_reply = response.choices[0].message.content.strip()

        chat_context.append({"role": "assistant", "content": assistant_reply})
        
        return assistant_reply

    elif intent == 'update':
        identifier = parameters.get('id') or parameters.get('nome')
        field = parameters.get('campo')
        new_value = parameters.get('valor')
        result = update_restaurant(identifier, field, new_value)
        return f"Restaurante {identifier} foi atualizado com sucesso!" if result else "Erro ao atualizar o restaurante."

    elif intent == 'select':
        identifier = parameters.get('id') or parameters.get('nome')
        result = select_restaurant(identifier)
        return f"Restaurante encontrado: {result}" if result else "Restaurante não encontrado."

    elif intent == 'delete':
        identifier = parameters.get('id') or parameters.get('nome')
        result = delete_restaurant(identifier)
        return f"Restaurante {identifier} foi deletado com sucesso" if result else "Erro ao deletar o restaurante."

    else:
        return "Desculpe, não consegui processar sua solicitação."

    
def handle_request(user_message, collection):

    try:
        assistant_reply = interpret_user_message(user_message)
        print(f'RETORNO INTENCAO {assistant_reply}')
        try:
            intent_data = json.loads(assistant_reply)
        except json.JSONDecodeError:
            return "desculpe, não consegui entender :c"
        
        response_message = process_intent(intent_data, collection, user_message)
        return response_message
    
    except Exception as e:
        print(f"Erro na função handle_request:\n\n{e}")
        return "ocorreu um erro aqui, foi mal :c"