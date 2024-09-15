from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import re
from unicodedata import normalize
import time

def xpath(driver,
           path: str,
           all: bool = False):

    if all != False:
        ## Retorna uma lista de elementos que correspondem ao path, se nao existir, retorna uma lista vazia
        try:return driver.find_elements(By.XPATH, path)
        except: return None

    else:
        try:return driver.find_element(By.XPATH, path)
        except:return None


def css(driver,
           path: str,
           all: bool = False):

    if all != False:
        ## Retorna uma lista de elementos que correspondem ao path, se nao existir, retorna uma lista vazia
        try:return driver.find_elements(By.CSS_SELECTOR, path)
        except:return None
    else:
        try:return driver.find_element(By.CSS_SELECTOR, path)
        except:return None


def id(driver,
           path: str,
           all: bool = False):

    if all != False:
        ## Retorna uma lista de elementos que correspondem ao path, se nao existir, retorna uma lista vazia
        try:return driver.find_elements(By.ID, path)
        except:return None
        
    else:
        try:return driver.find_element(By.ID, path)
        except:return None


def text(driver,
           path: str,
           all: bool = False):
    
    if all != False:
        ## Retorna uma lista de elementos que correspondem ao path, se nao existir, retorna uma lista vazia
        try:return driver.find_elements(By.LINK_TEXT, path)
        except:return None
        
    else:
        try:return driver.find_element(By.LINK_TEXT, path) 
        except:return None


def class_name(driver,
           path: str,
           all: bool = False):

    if all != False:
        ## Retorna uma lista de elementos que correspondem ao path, se nao existir, retorna uma lista vazia
        try:return driver.find_elements(By.CLASS_NAME, path)
        except:return None
    
    else:
        try:return driver.find_element(By.CLASS_NAME, path)
        except:return None
    

def page_source(driver): return driver.page_source

def page_html(driver): return driver.current_url

def send_value(driver, string: str) -> None: driver.send_keys(string)


def scrow_up(driver,
                qtd: int = None) -> None:
    
    actions = ActionChains(driver)

    if qtd == None:
        actions.send_keys(Keys.PAGE_UP).perform()
        time.sleep(0.7)

    for _ in range(qtd):
        actions.send_keys(Keys.PAGE_UP).perform()
        time.sleep(0.7)


def scrow_down(driver,
                qtd: int = None) -> None:
    
    actions = ActionChains(driver)

    if qtd == None:
        actions.send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(0.7)

    else:
        for _ in range(qtd):
            actions.send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(0.7)

def enter(driver,
            qtd: int = None) -> None:
    
    actions = ActionChains(driver)

    if qtd == None:
        actions.send_keys(Keys.ENTER).perform()
        time.sleep(0.7)

    else:
        for _ in range(qtd):
            actions.send_keys(Keys.ENTER).perform()
            time.sleep(0.7)

    
def search_field(driver,
                    value):
    
    search = xpath(driver, '//input[@id="searchboxinput"]')
    search.clear()
    
    send_value(search, value)

def move_click(driver,
               value):
    
    ActionChains(driver).move_to_element(value).click().perform()


class FindPlaces:

    def __init__(self) -> None:
        
        self.path_places = '//a[contains(@href, "https://www.google.com/maps/place")]'
        self.final_text = 'PbZDve'
        self.search = '//input[@id="searchboxinput"]'


    def search_field(self,
                     driver,
                     value):
        
        search = xpath(driver, self.search)

        send_value(search, value)


    def list_places(self, 
                    driver):
        try:
            listings = xpath(driver,
                                self.path_places,
                                all = True)
            
        except Exception as error:
            print(f'Nao foi possivel listar os comercios, vide error: {error}')
            raise Exception
        
        return listings


    def load_places(self, 
                   driver) -> None:
        
        listings = self.list_places(driver)

        elementos_botao = xpath(driver, '//button[@data-idom-class="Rj2Mlf OLiIxf PDpWxe LQeN7 s73B3c MyHLpd wphPJc Q8G3mf"]')
        
        try:
            if elementos_botao:
                try: elemento_botao = elementos_botao[0]
                except: elemento_botao = elementos_botao
                move_click(driver, elemento_botao)
                time.sleep(2)
                move_click(driver, elemento_botao)
                
            else:
                raise Exception
            
        except:
            print('Tentando segunda opção')
            elementos_botao = xpath(driver, '//*[@id="app"]/div[15]/div/div[1]/div/div/div[2]')
            ActionChains(driver).move_to_element(elementos_botao)
            time.sleep(1)

        scrow_down(driver)
        
        previous_listings = len(listings)

        keepScrolling = True
        while keepScrolling == True:
            
            scrow_down(driver, qtd = 3)
            
            current_listings = len(self.list_places(driver))
                            
            if current_listings != previous_listings:
                previous_listings = current_listings

            else:
                scrow_up(driver, qtd = 2)

                scrow_down(driver, qtd = 3)
                
                current_listings = len(self.list_places(driver))
                
                if current_listings != previous_listings:
                    previous_listings = current_listings
                else:
                    print(f"QTD Comercios captados {current_listings}")
                    keepScrolling = False
            
            scrow_down(driver)
            try: final = class_name(driver, self.final_text).text
            except:final = ''

            if final == 'Você chegou ao final da lista.':
                print(f"QTD Comercios captados {current_listings}")
                keepScrolling = False 


class PreProcessing:

    def string_process(input_str, column):
        
        if (column == 'details') or (column == 'endereco'):
            sem_acentos = normalize('NFKD', input_str).encode('ASCII', 'ignore').decode('utf-8')

            sem_cedilha = re.sub(r'ç', 'c', sem_acentos, flags=re.IGNORECASE)
            
            tratada = re.sub(r'[^a-zA-Z0-9\s]', '', sem_cedilha)
            
            return tratada.lower().replace('\n', ' ')

        elif column == 'funcionamento':
            return str(input_str).replace('\\n', '')
        
        elif column == 'numero':
            return ''.join(c for c in input_str if c.isdigit())
        
        elif (column == 'latitude') or (column == 'longitude'):
            return int(str(input_str).replace('.', ''))