from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import Optional

from datetime import datetime

from Class.inputs.get_conections import Get_connection
from Class.inputs.crude_functions_api import *
from Class.inputs.keys_all import *

client = Get_connection.conn_mongo()
db = client['scrapping_google']
collection = db['restaurants']

r = Get_connection.conn_redis()


# Get_connection.conn_mongo()
# df = pd.DataFrame(list(collection.find()))

# df.columns

# import numpy as np
# df = df.replace(np.nan, '').fillna('')

# for index, row in df.iterrows():
#     key = f"restaurant:{row['ID_BUSSINES']}:details"
#     restaurant_data = {
#         "nome": row['NOME'],
#         "endereco": row['ENDERECO'],
#         "nota_review": row['NOTA_REVIEW'],
#         "qtd_review": row['QTD_REVIEW'],
#         "hr_funcionamento": row['HR_FUNCIONAMENTO'],
#         "telefone": row['TELEFONE'],
#         "maior_movimento": row['MAIOR_MOVIMENTO'],
#         "acessibilidade": '--'.join(row['DETALHES'].get('Acessibilidade', 'Não especificado')),
#         "latitude": row['LATITUDE'],
#         "longitude": row['LONGITUDE']
#     }
#     r.hmset(key, restaurant_data)
#     print(f"Hash {key} inserido no Redis com dados: {restaurant_data}")


# for index, row in df.iterrows():

#     cidade = row['ENDERECO'].split(",")[-1].strip()
#     unique_identifier = f"{row['NOME']}-{cidade}"

#     r.pfadd("unique_restaurants", unique_identifier)
#     print(f"Restaurante {row['NOME']} na cidade {cidade} adicionado ao HyperLogLog.")


# unique_count = r.pfcount("unique_restaurants")
# print(f"numero aproximado de restaurantes unico {unique_count}")

# from redisbloom.client import Client

# r = Client(
#   host='redis-19915.c17.us-east-1-4.ec2.redns.redis-cloud.com',
#   port=19915,
#   password=password_redis)

# r.bfCreate('acessibilidade_bloom', 0.01, 10000)

# for index, row in df.iterrows():
#     acessibilidade_features = '--'.join(row['DETALHES'].get('Acessibilidade', 'Não especificado')).split('--')
#     for feature in acessibilidade_features:
#         feature = feature.strip().lower()
#         r.bfAdd('acessibilidade_bloom', feature)
#         print(f"caracterstica '{feature}' adicionada")


# caracteristica_para_verificar = "tem assento com acessibilidade para pessoas em cadeira de roda"
# caracteristica_para_verificar = caracteristica_para_verificar.strip().lower()

# exists = r.bfExists('acessibilidade_bloom', caracteristica_para_verificar)

# if exists:
#     print(f"a característica '{caracteristica_para_verificar}' e oferecida por algum restaurante")
# else:
#     print(f"a característica '{caracteristica_para_verificar}' nao e oferecida por nenhum restaurante registrado")


app = FastAPI()

class Restaurant(BaseModel):
    id_busness: Optional[str] = None
    DAT_ATT: Optional[str] = None
    NOME: Optional[str] = None
    ENDERECO: Optional[str] = None
    TELEFONE: Optional[str] = None
    WEB_SITE: Optional[str] = None
    QTD_REVIEW: Optional[str] = None
    NOTA_REVIEW: Optional[str] = None


@app.get("/")
def read_root():
    return {"message": "API de restaurantes MongoDB"}

@app.post("/restaurants/")
def create_restaurant_endpoint(restaurant: Restaurant):
    restaurant_id = create_restaurant(restaurant, collection)
    return {"inserted_id": restaurant_id}

@app.get("/restaurants/")
def get_all_restaurants():
    restaurants = get_restaurants(collection)
    return {"restaurants": restaurants}

@app.get("/restaurants/{restaurant_id}")
def get_restaurant_by_id_endpoint(restaurant_id: str):
    restaurant = get_restaurant_by_id(restaurant_id, collection)
    if restaurant:
        return restaurant

@app.put("/restaurants/{restaurant_id}")
def update_restaurant_endpoint(restaurant_id: str, restaurant: Restaurant):
    update_count = update_restaurant(restaurant_id, restaurant.dict(), collection)
    if update_count:
        return {"message": f"{update_count} documento(s) atualizado(s)"}

@app.delete("/restaurants/{restaurant_id}")
def delete_restaurant_endpoint(restaurant_id: str):
    delete_count = delete_restaurant(restaurant_id, collection)
    if delete_count:
        return {"message": f"{delete_count} documento(s) deletado(s)"}

@app.get("/restaurants/top/")
def get_top_restaurants_endpoint():
    top_restaurants = get_top_restaurants(collection)
    if top_restaurants:
        return {"top_restaurants": top_restaurants}
    

@app.get("/restaurants/count/")
def get_unique_restaurants_count_endpoint():
    unique_count = get_unique_restaurants_count(r)
    return {"unique_restaurants_count": unique_count}