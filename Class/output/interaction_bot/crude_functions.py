def select_restaurant(collection, identifier):

    if isinstance(identifier, int):
        restaurant = collection.find_one({"ID_BUSSINES": identifier})
    else:
        restaurant = collection.find_one({"NOME": identifier})
    
    if restaurant:
        return restaurant
    else:
        print("Restaurante nao encontrado.")
        return None


def update_restaurant(collection, identifier, field_name, new_value):

    if isinstance(identifier, int):
        result = collection.update_one({"ID_BUSSINES": identifier}, {"$set": {field_name: new_value}})
    else:
        result = collection.update_one({"NOME": identifier}, {"$set": {field_name: new_value}})
    
    if result.modified_count > 0:
        return True
    else:
        print("Nenhuma atualizacao foi feita")
        return False


def delete_restaurant(collection, identifier):

    if isinstance(identifier, int):
        result = collection.delete_one({"ID_BUSSINES": identifier})
    else: 
        result = collection.delete_one({"NOME": identifier})
    
    if result.deleted_count > 0:
        return True
    else:
        print("Restaurante nao encontrado para deletar")
        return False
