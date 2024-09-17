from Class.inputs import get_conections as inputs
from Class.devlopment import(
                            maestro as dev,
                            selenium_aux as aux
                            )

from Class.output import organize_data

import pandas as pd

##### POR ENDERECO ######
# obj_driver = inputs.Driver(url="https://www.google.com/maps/")

# driver = obj_driver.inicialize_driver()

# lista_end = [
#             # 'av floriano peixoto 2431  nossa sra aparecida uberlandia  mg 38400700'
#              'Av. Inglaterra, 45 - Tibery, Uberlândia - MG, 38405-050'
#             # 'Av. Noruega, 230 - Tibery, Uberlândia - MG, 38408-002'
# ]

# dfs = []
# for endereco in lista_end:

#     print(f'---> Pesquisando o endereco: {endereco}...')
#     driver = obj_driver.prepare_scrapping(driver, locate=endereco)

#     print(f'--> Iniciando Scrapping...')
#     dataframe = dev.Process().scrapping_bussines(driver, wait = 0.8)

#     obj_preprocess = organize_data.PreProcessing(dataframe)
#     obj_preprocess.new_features()
#     obj_preprocess.adjusting_columns()
#     dataframe = obj_preprocess.return_()

#     dfs.append(dataframe)

# dataframe = pd.concat(dfs).reset_index(drop = True)


##### ALL ######
obj_driver = inputs.Driver(
    url = "https://www.google.com/maps/search/restaurantes+em+Uberl%C3%A2ndia,+MG/@-18.9083338,-48.269227,15z?entry=ttu")

driver = obj_driver.inicialize_driver(show_page=True)

obj_manipulation = aux.FindPlaces()
obj_manipulation.load_places(driver)

qtd_locais = obj_manipulation.list_places(driver)



obj_manipulation.list_places(driver)[1].click()


qtd_locais[0].click()



dfs = []    

for posicao in range(len(qtd_locais)):
    
    try:aux.xpath(driver, "//button[@aria-label='Voltar']").click()
    except: pass

    if aux.id(driver, 'QA0Szd'):
        pass
    
    aux.move_click(driver, qtd_locais[posicao])
    
    print(f'--> Iniciando Scrapping...')
    dataframe = dev.Process().scrapping_bussines(driver, wait = 1.2)
    
    obj_preprocess = organize_data.PreProcessing(dataframe)
    obj_preprocess.new_features()
    obj_preprocess.adjusting_columns()
    dataframe = obj_preprocess.return_()

    dfs.append(dataframe)
    
    aux.scrow_down(driver, qtd = 2)

dataframe = pd.concat(dfs).reset_index(drop = True)


df = dataframe.copy()

obj_prep = organize_data.PreProcessing(df)
obj_prep.dataset_todict()
df = obj_prep.return_()

client = inputs.Get_connection()
db = client['scrapping_google']
collection = db['restaurants']

try:
    result = collection.insert_many(df)
    print(f'dados inseridos com sucesso ids: {result.inserted_ids}')
except Exception as e:
    print(f'nao foi possivel inserir, vide error: {e}')

