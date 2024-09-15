import pandas as pd
from datetime import datetime

import numpy as np
import ast

from Class.inputs import get_conections as inputs

class PreProcessing:

    def __init__(self, dataframe) -> None:
        self.dataframe = dataframe

    def convert_to_dict(x):
        if isinstance(x, str):
            try:
                return ast.literal_eval(x)
            except:
                return None
        return x

    def dataset_todict(self):
        
        try:
            self.dataframe = self.dataframe.where(pd.notnull(self.dataframe), None)
            
            self.dataframe['DETALHES'] = self.dataframe['DETALHES'].apply(self.convert_to_dict)
        
        except Exception as e:
            print(f'Houve um erro na tratativa do dataframe, vide error: {e}')
        
        try:
            self.dataframe = self.dataframe.to_dict(orient='records')

        except Exception as e:
            print(f"Houve um erro na transformação para dicionário, vide error: {e}")

    def return_(self): return self.dataframe


class Management:
    def __init__(self, client, db_name, collection_name):

        self.client = client
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_document(self, data):

        try:
            result = self.collection.insert_one(data)
            return result.inserted_id
        except Exception as e:
            print(f'Erro ao inserir documento: {e}')
            return None

    def find_documents(self, query=None, projection=None):
        try:
            cursor = self.collection.find(query or {}, projection)
            return list(cursor)
        except Exception as e:
            print(f'Erro ao buscar documentos: {e}')
            return []

    def update_documents(self, query, new_values):
        try:
            result = self.collection.update_many(query, {'$set': new_values})
            return result.modified_count
        except Exception as e:
            print(f'Erro ao atualizar documentos: {e}')
            return 0

    def delete_documents(self, query):

        try:
            result = self.collection.delete_many(query)
            return result.deleted_count
        except Exception as e:
            print(f'Erro ao deletar documentos: {e}')
            return 0
