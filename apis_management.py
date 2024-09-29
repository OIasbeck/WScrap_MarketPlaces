from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import Optional

from datetime import datetime

from Class.inputs.get_conections import Get_connection
from Class.inputs.crude_functions_api import *

client = Get_connection.conn()
db = client['scrapping_google']
collection = db['restaurants']

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