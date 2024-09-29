from bson.objectid import ObjectId
import math

def replace_nans(restaurant):

    for key, value in restaurant.items():
        if isinstance(value, float) and (math.isnan(value) or value in [float('inf'), float('-inf')]):
            restaurant[key] = "-" 
    return restaurant

def get_restaurants(collection):
    restaurants = list(collection.find())

    for restaurant in restaurants:
        restaurant['_id'] = str(restaurant['_id'])
        restaurant = replace_nans(restaurant) 
    
    return restaurants


def create_restaurant(restaurant, collection):
    result = collection.insert_one(restaurant.dict())
    return str(result.inserted_id)

def get_restaurant_by_id(restaurant_id: str, collection):
    return collection.find_one({"_id": ObjectId(restaurant_id)})

def update_restaurant(restaurant_id: str, updated_data: dict, collection):
    result = collection.update_one(
        {"_id": ObjectId(restaurant_id)},
        {"$set": updated_data}
    )
    return result.modified_count

def delete_restaurant(restaurant_id: str, collection):
    result = collection.delete_one({"_id": ObjectId(restaurant_id)})
    return result.deleted_count

def get_top_restaurants(collection):

    top_restaurants = list(collection.find().sort([
        ("NOTA_REVIEW", -1),
        ("QTD_REVIEW", -1) 
    ]).limit(3)) 
    
    for restaurant in top_restaurants:
        restaurant['_id'] = str(restaurant['_id'])
    
    return top_restaurants

def get_top_restaurants(collection):
    top_restaurants = list(collection.find({}, {"NOME": 1, "ENDERECO": 1, "_id": 0}).sort([
                    ("NOTA_REVIEW", -1), 
                    ("QTD_REVIEW", -1)
                ]).limit(3))
    
    return top_restaurants